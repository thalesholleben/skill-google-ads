"""
N-gram analysis for Google Ads search terms.

Input:  CSV exported from Google Ads > Keywords > Search Terms report
        Required columns: Search term, Clicks, Impressions, Cost, Conversions
        Optional: Conv. value, CPC

Output: ngram_report.csv with 1-gram, 2-gram and 3-gram aggregates
        sorted by cost descending within each n-gram group

Usage:
    python n_gram_analysis.py search_terms.csv
    python n_gram_analysis.py search_terms.csv --min-cost 5 --out my_report.csv
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    sys.exit("pandas is required: pip install pandas")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _ngrams(tokens: list[str], n: int) -> list[str]:
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def _find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Return first column name that matches any candidate (case-insensitive)."""
    lower_map = {c.lower().strip(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in lower_map:
            return lower_map[cand.lower()]
    return None


# ---------------------------------------------------------------------------
# core
# ---------------------------------------------------------------------------

def load_search_terms(path: str) -> pd.DataFrame:
    raw = pd.read_csv(path, thousands=",", encoding="utf-8-sig")

    col_map = {
        "term":    ["search term", "search terms", "query", "term"],
        "clicks":  ["clicks"],
        "impr":    ["impressions", "impr."],
        "cost":    ["cost", "spend"],
        "conv":    ["conversions", "conv.", "converted clicks"],
        "value":   ["conv. value", "conversion value", "revenue"],
        "cpc":     ["avg. cpc", "cpc", "avg cpc"],
    }

    resolved = {}
    for key, candidates in col_map.items():
        col = _find_column(raw, candidates)
        if col:
            resolved[key] = col

    if "term" not in resolved:
        sys.exit(
            f"Could not find 'Search term' column. Found columns: {list(raw.columns)}"
        )

    df = raw.rename(columns={v: k for k, v in resolved.items()})

    for num_col in ["clicks", "impr", "cost", "conv", "value", "cpc"]:
        if num_col in df.columns:
            df[num_col] = (
                df[num_col]
                .astype(str)
                .str.replace(r"[,$%]", "", regex=True)
                .str.strip()
                .replace("--", "0")
                .replace("", "0")
                .astype(float)
            )

    df["term"] = df["term"].astype(str)
    df = df[df["term"].str.lower() != "search term"]
    return df


def build_ngram_table(df: pd.DataFrame, n: int, min_cost: float) -> pd.DataFrame:
    agg = defaultdict(lambda: defaultdict(float))

    for _, row in df.iterrows():
        tokens = _normalize(str(row["term"])).split()
        seen = set()
        for gram in _ngrams(tokens, n):
            if gram not in seen:
                seen.add(gram)
                agg[gram]["clicks"] += row.get("clicks", 0)
                agg[gram]["impr"]   += row.get("impr", 0)
                agg[gram]["cost"]   += row.get("cost", 0)
                agg[gram]["conv"]   += row.get("conv", 0)
                agg[gram]["value"]  += row.get("value", 0)
                agg[gram]["count"]  += 1

    rows = []
    for gram, vals in agg.items():
        if vals["cost"] < min_cost:
            continue
        clicks = vals["clicks"]
        impr   = vals["impr"]
        cost   = vals["cost"]
        conv   = vals["conv"]

        ctr    = clicks / impr  * 100 if impr  > 0 else 0
        cvr    = conv   / clicks * 100 if clicks > 0 else 0
        cpa    = cost   / conv        if conv   > 0 else None
        roas   = vals["value"] / cost if cost   > 0 else None
        cpc    = cost   / clicks      if clicks > 0 else None

        rows.append({
            "n":         n,
            "gram":      gram,
            "queries":   int(vals["count"]),
            "clicks":    int(clicks),
            "impr":      int(impr),
            "cost":      round(cost, 2),
            "conv":      round(conv, 2),
            "ctr_%":     round(ctr, 2),
            "cvr_%":     round(cvr, 2),
            "cpc":       round(cpc, 2) if cpc is not None else None,
            "cpa":       round(cpa, 2) if cpa is not None else None,
            "roas":      round(roas, 2) if roas is not None else None,
        })

    result = pd.DataFrame(rows)
    if result.empty:
        return result
    return result.sort_values("cost", ascending=False).reset_index(drop=True)


def flag_actions(df: pd.DataFrame) -> pd.DataFrame:
    """Add a suggested_action column based on performance heuristics."""
    if df.empty:
        return df

    df = df.copy()
    actions = []

    med_cpa = df.loc[df["cpa"].notna(), "cpa"].median() if df["cpa"].notna().any() else None
    med_cvr = df.loc[df["cvr_%"] > 0, "cvr_%"].median() if (df["cvr_%"] > 0).any() else None

    for _, row in df.iterrows():
        cpa = row["cpa"]
        cvr = row["cvr_%"]
        cost = row["cost"]
        conv = row["conv"]

        if conv >= 3 and med_cpa and cpa <= med_cpa * 0.7:
            action = "PROMOTE — add as exact/phrase keyword"
        elif cost >= 20 and conv == 0:
            action = "REVIEW — high spend, zero conversions → consider negative"
        elif conv >= 2 and med_cpa and cpa >= med_cpa * 1.5:
            action = "OPTIMIZE — high CPA; check landing page or match type"
        elif cost >= 10 and cvr == 0:
            action = "NEGATIVE — zero CVR with meaningful spend"
        elif conv >= 5:
            action = "SCALE — strong performer, increase budget/bids"
        else:
            action = "MONITOR"

        actions.append(action)

    df["suggested_action"] = actions
    return df


def run(input_path: str, min_cost: float, output_path: str):
    print(f"Loading: {input_path}")
    df = load_search_terms(input_path)
    print(f"  {len(df)} search term rows loaded")

    frames = []
    for n in [1, 2, 3]:
        tbl = build_ngram_table(df, n, min_cost)
        tbl = flag_actions(tbl)
        frames.append(tbl)
        print(f"  {n}-gram: {len(tbl)} grams above min cost US$ {min_cost}")

    combined = pd.concat(frames, ignore_index=True)
    combined.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\nSaved: {output_path}")

    print("\n--- TOP 10 TERMS TO REVIEW (high spend, 0 conversions) ---")
    waste = combined[
        (combined["conv"] == 0) &
        (combined["cost"] >= 15) &
        (combined["n"] >= 2)
    ].sort_values("cost", ascending=False).head(10)

    if waste.empty:
        print("  None found above US$ 15 threshold.")
    else:
        for _, r in waste.iterrows():
            print(f"  [{r['n']}-gram] \"{r['gram']}\" — US$ {r['cost']} spent, 0 conv")

    print("\n--- TOP 10 TERMS TO PROMOTE (good CPA, 3+ conversions) ---")
    promote = combined[
        combined["suggested_action"].str.startswith("PROMOTE")
    ].sort_values("conv", ascending=False).head(10)

    if promote.empty:
        print("  None found matching criteria.")
    else:
        for _, r in promote.iterrows():
            cpa_str = f"CPA US$ {r['cpa']}" if r["cpa"] else "no CPA"
            print(f"  [{r['n']}-gram] \"{r['gram']}\" — {r['conv']} conv, {cpa_str}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="N-gram analysis for Google Ads search terms")
    parser.add_argument("input", help="Path to search terms CSV from Google Ads")
    parser.add_argument(
        "--min-cost", type=float, default=3.0,
        help="Minimum cost (USD) to include a gram in the report (default: 3.0)"
    )
    parser.add_argument(
        "--out", default="ngram_report.csv",
        help="Output CSV filename (default: ngram_report.csv)"
    )
    args = parser.parse_args()
    run(args.input, args.min_cost, args.out)
