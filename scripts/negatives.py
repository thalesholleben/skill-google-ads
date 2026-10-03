#!/usr/bin/env python3
"""Overblocking test for negative keywords: what a candidate negative would block in your terms and keywords.

Run it before adding a negative. One-word negatives are the classic way to silence buyers: `free` blocks
"free estimate", `cheap` blocks "cheap flights deal" for a travel agency, and a phrase with zero conversions in
the last 90 days can still block terms that converted earlier in the account's life. The script does not decide
intent: it shows what the negative would catch and fails the ones that block a converted term or an active
keyword.

Official negative keyword rules (support.google.com/google-ads/answer/2453972, checked Oct 1, 2026):
- case does not matter; accents do ("cafe" and "café" are different negatives); "&" and "and" differ;
- no close variants, synonyms, singular or plural;
- broad and phrase only look at the first 16 words of the search;
- broad: the search has all the words, in any order; phrase: the sequence; exact: the whole search is identical
  (no extra word, even after the 16th);
- symbols and operators in a negative: periods and "+" are ignored (a trailing "+", as in C++, sometimes is not);
  "site:..." and the OR operator are dropped; a word preceded by "-" is ignored ("dark -chocolate" works as
  "dark"); `, ! @ % ^ ( ) = { } ; ~ < > ? \\ |` and the backtick are rejected by Google;
- Google also blocks misspellings of the negative, which this script does not model (real blocking can be a bit
  wider than shown).

Where the rule is not explicit (a period, "+", hyphen or apostrophe inside a word), the script tests both readings
(joined and split) and fails the candidate if either one blocks: the error stays on the side of reporting a block.
Asterisks and other operators with ":" have no documented meaning: the candidate is refused (exit 2), never
approved.

Candidates use the UI syntax: `[exact]`, `"phrase"` or broad without marks. Terms: CSV export or API JSON
(search_term_view or campaign_search_term_view). Prefer the account's LIFETIME terms:

    SELECT search_term_view.search_term, metrics.clicks, metrics.cost_micros, metrics.conversions
    FROM search_term_view WHERE segments.date BETWEEN '2010-01-01' AND '<today>'

    python negatives.py --terms lifetime_terms.json --keywords keywords.json --candidate '"easy way"' --candidate wax
    python negatives.py --terms search_terms.csv --candidates-file candidates.txt --json

Exit codes: 0 no candidate blocks a converted term or an active keyword (in the data given); 1 at least one does;
2 invalid input (missing file, paginated or malformed JSON, candidate with an open mark or an unmodeled symbol).
Terms hidden by the privacy threshold are not tested: state the coverage (references/02, section 5).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.dont_write_bytecode = True  # the sibling import must not leave __pycache__ inside the skill
sys.path.insert(0, str(Path(__file__).resolve().parent))
from n_gram_analysis import InvalidInput, read_terms  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

MAX_QUERY_WORDS = 16
TYPES = {"[": "EXACT", '"': "PHRASE"}
INVALID = set(",!@%^()={};~<>?\\|`")  # Google rejects negatives with these symbols (g/2453972)


def tokens(text: str) -> list[str]:
    """Words as a negative sees them: lowercase, accents kept, '&' as a word, punctuation out."""
    text = unicodedata.normalize("NFC", text).casefold()
    return re.findall(r"&|[^\W_]+", text)


def _readings(word: str) -> set[tuple[str, ...]]:
    """Possible readings of a negative's word where the rule is not explicit: a period, '+', hyphen or apostrophe
    inside the word both joins ('fifth ave.' = 'fifth ave', '1.5' = '15') and splits."""
    joined = tuple(tokens(re.sub(r"[.+'’-]", "", word)))
    split = tuple(tokens(word))
    return {x for x in (joined, split) if x}


def candidate_readings(text: str) -> tuple[str, list[list[str]]]:
    """'[x]' exact, '"x"' phrase, anything else broad, with operators and symbols by the official rule.

    Returns (type, readings): each reading is a list of words. An invalid symbol, an asterisk, an operator with ':'
    other than site:, or a candidate left without words raises InvalidInput (exit 2), never an approval."""
    t = text.strip()
    if t[:1] in TYPES:
        close = "]" if t[0] == "[" else '"'
        if len(t) < 2 or t[-1] != close:
            raise InvalidInput(f"candidate with an open mark: {text!r}")
        kind, t = TYPES[t[0]], t[1:-1]
    else:
        if t[-1:] in ('"', "]"):
            raise InvalidInput(f"candidate with a closing mark and no opening one: {text!r}")
        kind = "BROAD"
    if any(c in '"[]' for c in t):
        raise InvalidInput(f"candidate with quotes or brackets inside: {text!r}")
    bad = sorted({c for c in t if c in INVALID})
    if bad:
        raise InvalidInput(f"Google rejects negatives with {' '.join(bad)}: {text!r}")
    if "*" in t:
        raise InvalidInput(f"an asterisk in a negative has no documented rule; test without it: {text!r}")
    readings: list[list[str]] = [[]]
    for part in t.split():
        if part.startswith("-"):
            continue  # "dark -chocolate" works as "dark"
        if part == "OR":
            continue  # search operator, ignored
        if part.lower().startswith("site:"):
            continue  # "site:" is dropped from the negative
        if ":" in part:
            raise InvalidInput(f"operator {part.split(':')[0]}: has no documented rule in negatives: {text!r}")
        options = _readings(part)
        if not options:
            continue  # only ignored punctuation
        readings = [base + list(opt) for base in readings for opt in sorted(options)]
    readings = [x for x in readings if x]
    if not readings:
        raise InvalidInput(f"candidate without words after removing operators and symbols: {text!r}")
    unique = []
    for x in readings:
        if x not in unique:
            unique.append(x)
    return kind, unique


def candidate(text: str) -> tuple[str, list[str]]:
    """Type and the first reading (shortcut for callers that only need the type)."""
    kind, readings = candidate_readings(text)
    return kind, readings[0]


def blocks(kind: str, negative: list[str], search: list[str]) -> bool:
    """Does the negative block the search? Official rule (no close variants; broad and phrase only see the first 16
    words). Exact compares the WHOLE search: a search with an extra word is not identical, even after the 16th."""
    if kind == "EXACT":
        return search == negative
    window = search[:MAX_QUERY_WORDS]
    if kind == "PHRASE":
        k = len(negative)
        return any(window[i:i + k] == negative for i in range(len(window) - k + 1))
    return set(negative) <= set(window)


def group(terms: list[dict]) -> list[dict]:
    """Adds up the same term (several campaigns, ad groups and days) in the form the negative sees."""
    groups: dict[tuple, dict] = {}
    for t in terms:
        key = tuple(tokens(t["term"]))
        if not key:
            continue
        g = groups.setdefault(key, {"term": t["term"], "words": list(key), "clicks": 0.0, "cost": 0.0, "conv": 0.0})
        for field in ("clicks", "cost", "conv"):
            g[field] += float(t.get(field, 0) or 0)
    return list(groups.values())


def read_keywords(path: Path) -> list[str]:
    """Text (one per line, [ ] and " " accepted, # comments) or API JSON of ad_group_criterion rows."""
    if not path.is_file():
        raise InvalidInput(f"keywords file not found: {path}")
    if path.suffix.lower() == ".json":
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except ValueError as err:
            raise InvalidInput(f"invalid JSON in {path}: {err}") from err
        if isinstance(data, dict):
            if data.get("nextPageToken"):
                raise InvalidInput("paginated response (nextPageToken) in the keywords")
            data = data.get("results")
        if not isinstance(data, list):
            raise InvalidInput(f"{path}: the JSON must be a list of rows or an object with 'results'")
        out = []
        for i, row in enumerate(data):
            crit = row.get("adGroupCriterion") if isinstance(row, dict) else None
            if not isinstance(crit, dict):
                raise InvalidInput(f"{path}, row {i}: no adGroupCriterion")
            if crit.get("negative") in (True, "true") or crit.get("status") not in (None, "ENABLED"):
                continue  # negative, paused or removed is not an active positive keyword
            kw = crit.get("keyword")
            if not isinstance(kw, dict) or not isinstance(kw.get("text"), str) or not kw["text"].strip():
                raise InvalidInput(f"{path}, row {i}: adGroupCriterion.keyword without 'text' (got {kw!r})")
            out.append(kw["text"])
        return out
    out = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line.strip('[]"+'))
    return out


def check(candidates: list[str], terms: list[dict], keywords: list[str]) -> list[dict]:
    grouped = group(terms)
    positives = [(k, tokens(k)) for k in keywords if tokens(k)]
    result = []
    for text in candidates:
        kind, readings = candidate_readings(text)

        def caught(search: list[str]) -> bool:
            return any(blocks(kind, reading, search) for reading in readings)

        hit = [g for g in grouped if caught(g["words"])]
        # Any positive credit protects the term: rounding is for display only.
        converted = sorted((g for g in hit if g["conv"] > 0), key=lambda g: -g["conv"])
        hit_keywords = [k for k, toks in positives if caught(toks)]
        warnings = []
        if len(readings) > 1:
            warnings.append("readings tested: " + " | ".join(" ".join(x) for x in readings))
        if kind == "BROAD" and any(len(x) == 1 for x in readings):
            warnings.append(f"single-word broad negative: blocks every search with '{min(readings, key=len)[0]}' anywhere")
        verdict = "BLOCKS CONVERSION" if converted else "BLOCKS KEYWORD" if hit_keywords else "OK"
        result.append({
            "candidate": text, "type": kind, "words": readings[0], "readings": readings, "verdict": verdict,
            "terms_blocked": len(hit), "clicks": round(sum(g["clicks"] for g in hit), 2),
            "cost": round(sum(g["cost"] for g in hit), 2), "conv": round(sum(g["conv"] for g in hit), 4),
            "converted_blocked": [{"term": g["term"], "conv": round(g["conv"], 4), "clicks": g["clicks"]}
                                  for g in converted],
            "keywords_blocked": hit_keywords,
            "examples": [g["term"] for g in sorted(hit, key=lambda g: -g["cost"])[:10]],
            "warnings": warnings,
        })
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="What each candidate negative would block in your terms and keywords.")
    ap.add_argument("--terms", required=True, help="CSV export or API JSON with the search terms (ideally lifetime)")
    ap.add_argument("--candidate", action="append", default=[], help='[exact], "phrase" or broad; repeat')
    ap.add_argument("--candidates-file", help="one candidate per line (# comments)")
    ap.add_argument("--keywords", help="active positive keywords: text (one per line) or API JSON of ad_group_criterion")
    ap.add_argument("--json", action="store_true")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exit_:
        return 0 if exit_.code == 0 else 2

    try:
        candidates = list(args.candidate)
        if args.candidates_file:
            f = Path(args.candidates_file)
            if not f.is_file():
                raise InvalidInput(f"candidates file not found: {f}")
            candidates += [x.strip() for x in f.read_text(encoding="utf-8-sig").splitlines()
                           if x.strip() and not x.strip().startswith("#")]
        if not candidates:
            raise InvalidInput("no candidate (use --candidate or --candidates-file)")
        terms = read_terms(Path(args.terms))
        keywords = read_keywords(Path(args.keywords)) if args.keywords else []
        result = check(candidates, terms, keywords)
    except InvalidInput as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 2

    failed = [r for r in result if r["verdict"] != "OK"]
    warnings = []
    if terms and not any(t["conv"] > 0 for t in terms):
        warnings.append("no term with conversions in the data: check that the query selected metrics.conversions "
                        "over the lifetime window (the API omits zero metrics); otherwise OK does not protect buyers")
    if args.json:
        print(json.dumps({"terms_read": len(terms), "keywords_read": len(keywords), "warnings": warnings,
                          "candidates": result, "failed": len(failed)}, ensure_ascii=False, allow_nan=False))
        return 1 if failed else 0

    print(f"terms read: {len(terms)}  |  active keywords: {len(keywords)}"
          + ("" if keywords else " (no --keywords: keyword conflicts were not tested)"))
    for w in warnings:
        print(f"WARNING: {w}")
    for r in result:
        print(f"\n{r['verdict']:17} {r['candidate']} ({r['type'].lower()}): {r['terms_blocked']} terms, "
              f"{r['clicks']:.0f} clicks, cost {r['cost']:.2f}, conversions {r['conv']:.2f}")
        for c in r["converted_blocked"][:10]:
            print(f"    converted: {c['term']} ({c['conv']:.2f} conv., {c['clicks']:.0f} clicks)")
        for k in r["keywords_blocked"][:10]:
            print(f"    active keyword blocked: {k}")
        for w in r["warnings"]:
            print(f"    warning: {w}")
        if r["examples"] and r["verdict"] == "OK":
            print("    would block: " + "; ".join(r["examples"][:5]))
    print("\nOK means: in the data given, nothing that converted and no active keyword is blocked. Hidden terms and "
          "misspellings are outside the test; intent is still your call.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
