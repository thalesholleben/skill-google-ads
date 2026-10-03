#!/usr/bin/env python3
"""N-gram analysis of Google Ads search terms, standard library only.

Inputs (by file extension):
- CSV exported from Google Ads (search terms report), English or Portuguese UI, with the export preamble,
  comma or semicolon separators, decimal comma and currency symbols in values;
- JSON from the Google Ads API (search_term_view or campaign_search_term_view rows, as `{"results": [...]}`,
  a list of rows, or the batches of searchStream). A paginated response (nextPageToken) is refused: join the
  pages first.

Each term is split into 1, 2 and 3 word grams (Unicode normalization: accents stay, punctuation goes;
`--strip-accents` merges spellings). A gram adds up what every term containing it adds up.

The cut guard follows references/08-low-volume.md: the unit is the converted click, so the base needs
`--actions-per-click` (conservative p) or `--click-cvr`. Without them the suggestion is NO BASE and the script
does not suggest any cut by performance. With a base:
- zero conversions and clicks >= the minimum for P(0) < 5% -> REVIEW INTENT (a review trigger, not a cut);
- zero conversions below the minimum -> LOW DATA (N clicks missing);
- 3+ conversions and CPA up to 70% of the base CPA -> PROMOTE? (candidate for its own keyword).
No suggestion becomes a negative on its own: the intent gate decides, and negatives.py checks what a negative
would block.

    python n_gram_analysis.py search_terms.csv
    python n_gram_analysis.py search_terms.csv --min-cost 10 --out my_report.csv
    python n_gram_analysis.py search_terms.csv --actions-per-click 2 --base-clicks 410 --base-conversions 9 --base-cost 2150
    python n_gram_analysis.py search_terms.json --actions-per-click 1

Exit codes: 0 report written, 2 invalid input (missing file, malformed number or JSON, paginated JSON, invalid
option), never a traceback.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.dont_write_bytecode = True  # the sibling import must not leave __pycache__ inside the skill
sys.path.insert(0, str(Path(__file__).resolve().parent))
from stats import NoBase, click_p, min_clicks  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

TOTAL = re.compile(r"^total\s*:", re.I)  # the "Total: ..." rows of the export; "total gym" is a real term
COLUMNS = {
    "term": ["search term", "search terms", "termo de pesquisa", "termos de pesquisa", "termo de busca"],
    "clicks": ["clicks", "cliques"],
    "impr": ["impr.", "impressions", "impr", "impressões", "impressoes"],
    "cost": ["cost", "custo"],
    "conv": ["conversions", "conv.", "conversões", "conversoes"],
    "value": ["conv. value", "conversion value", "conv value", "valor conv.", "valor da conv.", "valor da conversão"],
}
PORTUGUESE = {"termo de pesquisa", "termos de pesquisa", "termo de busca", "cliques", "custo"}
LABELS = ("REVIEW INTENT", "LOW DATA", "PROMOTE?", "NO BASE")


class InvalidInput(ValueError):
    """Input the script cannot read safely: exit 2, never a traceback."""


def normalize(text: str, strip_accents: bool = False) -> list[str]:
    """Lowercase, punctuation becomes a space, accents stay (or go with strip_accents). Returns the words."""
    text = unicodedata.normalize("NFC", text.lower())
    if strip_accents:
        text = "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))
    return re.sub(r"[^\w]+|_", " ", text).split()


def grams(words: list[str], n: int) -> set[str]:
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def contains_word(term: str, word: str) -> bool:
    """Whole-word match: 'art' does not match 'smart watch'."""
    target = normalize(word)
    words = normalize(term)
    return any(words[i:i + len(target)] == target for i in range(len(words) - len(target) + 1))


# --------------------------------------------------------------------------- reading

# Only what a Google Ads export writes: empty or "--" (zero), a number with separators, a currency in front ("$",
# "US$", "R$", "€", "£") and "%" at the end. Text, NaN and minus signs never become zero.
EXPORT_NUMBER = re.compile(r"^(?:[A-Za-z]{0,3}\$|[€£])?\s*\d[\d.,]*\s*%?$")


def _number(value: str, decimal_comma: bool) -> float:
    raw = str(value if value is not None else "").replace("\u00a0", " ").strip()
    if raw in ("", "-", "--"):
        return 0.0
    if not EXPORT_NUMBER.match(raw):
        raise InvalidInput(f"malformed number: {value!r}")
    v = re.sub(r"[^\d,.]", "", raw)
    v = v.replace(".", "").replace(",", ".") if decimal_comma else v.replace(",", "")
    try:
        number = float(v)
    except ValueError as err:
        raise InvalidInput(f"malformed number: {value!r}") from err
    if not math.isfinite(number) or number < 0:
        raise InvalidInput(f"unexpected number: {value!r}")
    return number


def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        raise InvalidInput(f"file not found: {path}")
    raw = path.read_bytes()
    text = None
    for encoding in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        raise InvalidInput(f"unrecognized encoding: {path}")
    lines = text.splitlines()
    known = {c for names in COLUMNS.values() for c in names}
    start = None
    for i, line in enumerate(lines):
        cells = [c.strip().strip('"').lower() for c in re.split(r"[,;\t]", line)]
        if any(c in COLUMNS["term"] for c in cells) and sum(c in known for c in cells) >= 2:
            start = i
            break
    if start is None:
        raise InvalidInput(f"search terms header not found in {path} (look for 'Search term')")
    header = lines[start]
    sep = ";" if header.count(";") > header.count(",") else "\t" if "\t" in header else ","
    reader = csv.reader(io.StringIO("\n".join(lines[start:])), delimiter=sep)
    names = [c.strip().lower() for c in next(reader)]
    decimal_comma = any(n in PORTUGUESE for n in names)
    idx = {}
    for key, options in COLUMNS.items():
        for j, n in enumerate(names):
            if n in options:
                idx[key] = j
                break
    missing = [c for c in ("term", "clicks", "cost", "conv") if c not in idx]
    if missing:
        raise InvalidInput(f"missing CSV columns: {', '.join(missing)}; found: {names}")
    terms = []
    for line_no, cells in enumerate(reader, start=start + 2):
        if not any(c.strip() for c in cells):
            continue  # blank line
        if TOTAL.match(cells[0].strip()) or (len(cells) > idx["term"] and TOTAL.match(cells[idx["term"]].strip())):
            continue
        if len(cells) <= max(idx.values()):
            raise InvalidInput(f"{path}, line {line_no}: {len(cells)} columns where the header needs "
                               f"{max(idx.values()) + 1} (truncated record)")
        term = cells[idx["term"]].strip()
        if not term:
            raise InvalidInput(f"{path}, line {line_no}: empty search term in a data row")
        try:
            terms.append({
                "term": term,
                "clicks": _number(cells[idx["clicks"]], decimal_comma),
                "impr": _number(cells[idx["impr"]], decimal_comma) if "impr" in idx else 0.0,
                "cost": _number(cells[idx["cost"]], decimal_comma),
                "conv": _number(cells[idx["conv"]], decimal_comma),
                "value": _number(cells[idx["value"]], decimal_comma) if "value" in idx else 0.0,
            })
        except InvalidInput as err:
            raise InvalidInput(f"{path}, line {line_no}: {err}") from err
    return terms


def api_rows(data) -> list:
    """Rows from `{"results": [...]}`, a list of rows, or searchStream batches."""
    if isinstance(data, dict):
        if data.get("nextPageToken"):
            raise InvalidInput("paginated response (nextPageToken): join all pages first")
        if "results" not in data:
            raise InvalidInput("JSON without 'results'")
        data = data["results"]
    if not isinstance(data, list):
        raise InvalidInput("the JSON must be a list of rows or an object with 'results'")
    rows = []
    for item in data:
        if isinstance(item, dict) and "results" in item and "metrics" not in item:
            if item.get("nextPageToken"):
                raise InvalidInput("paginated batch (nextPageToken) in the JSON")
            if not isinstance(item["results"], list):
                raise InvalidInput("batch whose 'results' is not a list")
            rows.extend(item["results"])
        else:
            rows.append(item)
    return rows


def _metric(m: dict, key: str) -> float:
    value = m.get(key, 0)
    try:
        number = float(value or 0)
    except (TypeError, ValueError) as err:
        raise InvalidInput(f"malformed metric {key}: {value!r}") from err
    if not math.isfinite(number) or number < 0:
        raise InvalidInput(f"unexpected metric {key}: {value!r}")
    return number


def read_json(path: Path) -> list[dict]:
    """Terms from search_term_view or campaign_search_term_view read through the API (cost in micros)."""
    if not path.is_file():
        raise InvalidInput(f"file not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (ValueError, UnicodeDecodeError) as err:
        raise InvalidInput(f"invalid JSON in {path}: {err}") from err
    terms = []
    for i, row in enumerate(api_rows(data)):
        if not isinstance(row, dict):
            raise InvalidInput(f"JSON row {i} is not an object")
        view = row.get("searchTermView") or row.get("campaignSearchTermView") or {}
        term = view.get("searchTerm") if isinstance(view, dict) else None
        if not isinstance(term, str) or not term.strip():
            raise InvalidInput(f"JSON row {i} without searchTermView.searchTerm")
        m = row.get("metrics") or {}
        if not isinstance(m, dict):
            raise InvalidInput(f"JSON row {i} with malformed 'metrics'")
        terms.append({"term": term.strip(), "clicks": _metric(m, "clicks"), "impr": _metric(m, "impressions"),
                      "cost": _metric(m, "costMicros") / 1_000_000, "conv": _metric(m, "conversions"),
                      "value": _metric(m, "conversionsValue")})
    return terms


def read_terms(path: Path) -> list[dict]:
    """CSV export or API JSON, by extension."""
    return read_json(path) if path.suffix.lower() == ".json" else read_csv(path)


# --------------------------------------------------------------------------- analysis

def table(terms: list[dict], n: int, strip_accents: bool) -> dict[str, dict]:
    agg: dict[str, dict] = defaultdict(lambda: defaultdict(float))
    for t in terms:
        for g in grams(normalize(t["term"], strip_accents), n):
            a = agg[g]
            a["queries"] += 1
            for field in ("clicks", "impr", "cost", "conv", "value"):
                a[field] += t[field]
    return agg


def suggest(a: dict, p: float | None, no_base_reason: str, base_cpa: float | None, risk: float) -> tuple[str, str]:
    conv, clicks = a["conv"], a["clicks"]
    if conv >= 3 and base_cpa and a["cost"] / conv <= 0.7 * base_cpa:
        return "PROMOTE?", f"CPA {a['cost'] / conv:.2f} <= 70% of base CPA {base_cpa:.2f}"
    if conv <= 0 and clicks > 0:
        if p is None:
            return "NO BASE", no_base_reason
        minimum = min_clicks(p, risk)
        if clicks >= minimum:
            return "REVIEW INTENT", f"{clicks:.0f} clicks without conversion; minimum {minimum} for P(0) < {risk:.0%}"
        return "LOW DATA", f"{minimum - clicks:.0f} clicks short of the minimum of {minimum}"
    return "", ""


def analyze(terms: list[dict], base: dict, actions_per_click: int | None, click_cvr: float | None,
            risk: float = 0.05, strip_accents: bool = False, min_cost: float = 0.0) -> dict:
    try:
        p = click_p(base["conv"], base["clicks"], actions_per_click, click_cvr)
        reason = ""
    except NoBase as err:
        p, reason = None, str(err)
    base_cpa = base["cost"] / base["conv"] if base["conv"] > 0 else None
    rows = []
    for n in (1, 2, 3):
        for g, a in table(terms, n, strip_accents).items():
            if a["cost"] < min_cost:
                continue
            label, why = suggest(a, p, reason, base_cpa, risk)
            rows.append({
                "n": n, "gram": g, "queries": int(a["queries"]), "clicks": round(a["clicks"], 2),
                "impr": round(a["impr"], 2), "cost": round(a["cost"], 2), "conv": round(a["conv"], 4),
                "conv_value": round(a["value"], 2),
                "ctr_pct": round(100 * a["clicks"] / a["impr"], 2) if a["impr"] else None,
                "conv_per_click": round(a["conv"] / a["clicks"], 4) if a["clicks"] else None,
                "cpc": round(a["cost"] / a["clicks"], 2) if a["clicks"] else None,
                "cpa": round(a["cost"] / a["conv"], 2) if a["conv"] > 0 else None,
                "roas": round(a["value"] / a["cost"], 2) if a["cost"] and a["value"] else None,
                "suggestion": label, "reason": why,
            })
    rows.sort(key=lambda r: (r["n"], -r["cost"]))
    coverage = None
    if base.get("visible_cost") is not None and base.get("cost"):
        coverage = {"cost": round(base["visible_cost"] / base["cost"], 4),
                    "clicks": round(base["visible_clicks"] / base["clicks"], 4) if base["clicks"] else None}
    return {"base": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in base.items()},
            "click_p": p, "no_base": reason or None, "base_cpa": base_cpa, "coverage": coverage, "rows": rows}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="N-gram analysis of search terms with a statistical guard.")
    ap.add_argument("input", help="search terms CSV exported from Google Ads, or API JSON")
    ap.add_argument("--actions-per-click", type=int, help="k: primary actions counted 'One' (conservative p)")
    ap.add_argument("--click-cvr", type=float, help="converted-click p measured outside the platform")
    ap.add_argument("--base-clicks", type=float, help="total campaign clicks in the period (includes hidden terms)")
    ap.add_argument("--base-conversions", type=float, help="total conversions in the period")
    ap.add_argument("--base-cost", type=float, help="total cost in the period (turns on coverage)")
    ap.add_argument("--risk", type=float, default=0.05)
    ap.add_argument("--min-cost", type=float, default=0.0, help="skip grams with lower cost (account currency)")
    ap.add_argument("--strip-accents", action="store_true")
    ap.add_argument("--out", default="ngram_report.csv")
    ap.add_argument("--json", action="store_true", help="print the summary as JSON")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exit_:
        return 0 if exit_.code == 0 else 2

    numbers = {"--risk": args.risk, "--min-cost": args.min_cost, "--click-cvr": args.click_cvr,
               "--base-clicks": args.base_clicks, "--base-conversions": args.base_conversions,
               "--base-cost": args.base_cost}
    for name, value in numbers.items():
        if value is not None and (not math.isfinite(value) or value < 0):
            print(f"ERROR: {name} must be finite and >= 0 (got {value})", file=sys.stderr)
            return 2
    if not 0 < args.risk < 1:
        print(f"ERROR: --risk must be between 0 and 1 (got {args.risk})", file=sys.stderr)
        return 2
    if args.actions_per_click is not None and args.actions_per_click < 1:
        print("ERROR: --actions-per-click must be 1 or more", file=sys.stderr)
        return 2
    try:
        terms = read_terms(Path(args.input))
    except InvalidInput as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 2
    visible = {c: sum(t[c] for t in terms) for c in ("clicks", "conv", "cost")}
    # Without the campaign totals (--base-*), the base is only the visible part and coverage is unknown.
    base = {"clicks": args.base_clicks if args.base_clicks is not None else visible["clicks"],
            "conv": args.base_conversions if args.base_conversions is not None else visible["conv"],
            "cost": args.base_cost if args.base_cost else visible["cost"],
            "visible_cost": visible["cost"] if args.base_cost else None,
            "visible_clicks": visible["clicks"]}

    r = analyze(terms, base, args.actions_per_click, args.click_cvr, args.risk, args.strip_accents, args.min_cost)

    fields = ["n", "gram", "queries", "clicks", "impr", "cost", "conv", "conv_value", "ctr_pct", "conv_per_click",
              "cpc", "cpa", "roas", "suggestion", "reason"]
    try:
        with open(args.out, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(r["rows"])
    except OSError as err:
        print(f"ERROR: could not write {args.out}: {err}", file=sys.stderr)
        return 2

    summary = {k: v for k, v in r.items() if k != "rows"}
    summary["terms_read"] = len(terms)
    summary["output"] = args.out
    for label in LABELS:
        summary[label] = sum(1 for x in r["rows"] if x["suggestion"] == label)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, default=str))
        return 0

    print(f"terms read: {len(terms)}  |  output: {args.out}")
    if not terms:
        print("no terms in the input: nothing to analyze")
    cov = r["coverage"]
    if cov:
        clicks_cov = f", {cov['clicks']:.0%} of clicks" if cov["clicks"] is not None else ""
        print(f"coverage of visible terms: {cov['cost']:.0%} of cost{clicks_cov}")
    else:
        print("coverage: unknown (no --base-cost); intent percentages apply only to the visible part")
    b = r["base"]
    print(f"base: {b['clicks']:.0f} clicks, {b['conv']:.2f} conversions" +
          (f", converted-click p {r['click_p']:.4f}, minimum {min_clicks(r['click_p'], args.risk)} clicks"
           if r["click_p"] else f"  |  NO BASE: {r['no_base']}"))
    for label in ("REVIEW INTENT", "PROMOTE?"):
        top = [x for x in r["rows"] if x["suggestion"] == label][:10]
        print(f"\n{label} ({summary[label]}):")
        for x in top:
            print(f"  [{x['n']}] {x['gram']}: {x['clicks']:.0f} clicks, cost {x['cost']:.2f}, "
                  f"conv {x['conv']:.2f}  ({x['reason']})")
        if not top:
            print("  none")
    print(f"\nLOW DATA: {summary['LOW DATA']}  |  NO BASE: {summary['NO BASE']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
