#!/usr/bin/env python3
"""Offline test of the Google Ads skill: statistics, budget limits, n-grams, negative keywords and repo hygiene.

    python -B scripts/self_test.py

Runs with the standard library only (Python 3.10+), from any folder. The CI runs exactly this. Compilation is
checked inside the test with the bytecode written to a temporary folder, so no __pycache__ lands in the repo.
"""
from __future__ import annotations

import json
import py_compile
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
FIX = ROOT / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

import budget as bud  # noqa: E402
import n_gram_analysis as ng  # noqa: E402
import negatives as neg  # noqa: E402
import stats as st  # noqa: E402

FAILURES: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    print(("ok    " if condition else "FAIL  ") + name + ("" if condition else f"  ->  {detail}"))
    if not condition:
        FAILURES.append(name)


def close(a: float, b: float, tol: float = 0.01) -> bool:
    return abs(a - b) <= tol


def run(script: str, *args: str, bytecode: bool = False) -> tuple[int, str]:
    cmd = [sys.executable] + ([] if bytecode else ["-B"]) + [str(SCRIPTS / script), *args]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout + p.stderr


# ----------------------------------------------------------------- statistics
check("P(0) of 21 clicks at 2% = 0.654", close(st.p_zero(0.02, 21), 0.654, 0.001))
check("minimum clicks at 2% = 149", st.min_clicks(0.02) == 149)
check("conservative p: 30 conv, 100 clicks, k=3 = 0.10", close(st.click_p(30, 100, 3), 0.10, 1e-9))
check("minimum clicks at 10% = 29", st.min_clicks(0.10) == 29)
for k, args in ((None, (30, 100)), (3, (0, 100)), (3, (30, 0)), (1, (150, 100))):
    try:
        st.click_p(*args, actions_per_click=k)
        check(f"NO BASE with k={k} and base {args}", False, "did not raise NoBase")
    except st.NoBase:
        check(f"NO BASE with k={k} and base {args}", True)
check("--click-cvr measured outside wins", st.click_p(0, 0, None, 0.05) == 0.05)
lo, hi = st.poisson_ci(5)
check("Poisson interval of 5 events = [1.62, 11.67]", close(lo, 1.62) and close(hi, 11.67), f"{lo}, {hi}")
lo, hi = st.poisson_ci(0)
check("Poisson interval of 0 events = [0, 3.69]", lo == 0 and close(hi, 3.69), f"{lo}, {hi}")
lo, hi = st.cpa_ci(400, 5)
check("CPA interval with 5 conversions and 400 = [34, 246]", close(lo, 34.28, 0.05) and close(hi, 246.38, 0.1), f"{lo}, {hi}")
# Independent reference: mpmath 1.3.0, regularized gamma (Garwood). Large counts must not underflow.
for k, (ref_lo, ref_hi) in {800: (745.516993, 857.411783), 1000: (938.973018, 1063.952136)}.items():
    lo, hi = st.poisson_ci(k)
    check(f"Poisson interval of {k} events matches mpmath", close(lo, ref_lo, 1e-4) and close(hi, ref_hi, 1e-4), f"{lo}, {hi}")
check("rule of three: 0 in 150 gives 0.02", close(st.rate_ci(0, 150)["rule_of_three"], 0.02, 1e-9))
check("two-sided Fisher 0/10 vs 4/10 = 0.087 (not the 0.025 of a z test)", close(st.fisher(0, 10, 4, 10), 0.0867, 0.001))
check("Fisher is symmetric", close(st.fisher(0, 10, 4, 10), st.fisher(4, 10, 0, 10), 1e-12))
code, out = run("stats.py", "zero", "--n", "9", "--conversions", "30", "--clicks", "100")
check("CLI without a unit says NO BASE with exit 3", code == 3 and "NO BASE" in out, out)
code, out = run("stats.py", "clicks", "--conversions", "30", "--clicks", "100", "--actions-per-click", "3", "--json")
check("CLI clicks --json = 29", code == 0 and json.loads(out)["min_clicks"] == 29, out)
for label, args in (("negative n", ["zero", "--n", "-5", "--click-cvr", "0.02"]),
                    ("risk 0", ["clicks", "--click-cvr", "0.02", "--risk", "0"]),
                    ("negative events", ["poisson", "--events", "-3"]),
                    ("confidence 1", ["poisson", "--events", "5", "--conf", "1"]),
                    ("successes above trials", ["rate", "--successes", "5", "--trials", "3"]),
                    ("arm with successes above trials", ["compare", "--a", "11/10", "--b", "2/10"]),
                    ("NaN click cvr", ["zero", "--n", "21", "--click-cvr", "nan"]),
                    ("k zero", ["base", "--conversions", "30", "--clicks", "100", "--actions-per-click", "0"]),
                    ("infinite cost", ["cpa", "--cost", "inf", "--conversions", "3"])):
    code, out = run("stats.py", *args)
    check(f"stats refuses {label} with exit 2, no traceback", code == 2 and "Traceback" not in out, out)
code, out = run("stats.py", "cpa", "--cost", "100", "--conversions", "0", "--json")
check("CPA with zero conversions: valid JSON, no Infinity", code == 0 and json.loads(out)["cpa_upper"] is None
      and "Infinity" not in out, out)

# ----------------------------------------------------------------- budget
C = bud.Campaign
r = bud.limits([C("search", 30, new=36, spend=450), C("brand", 30, new=21, spend=450)], 16)
check("budget 30+30 -> 36+21: change day 132", r["change_day_limit"] == 132, str(r))
check("budget 30+30 -> 36+21: month 1,812 (900 + 57 x 16)", r["month_limit"] == 1812, str(r))
check("budget: next day 114", r["next_day_limit"] == 114, str(r))
r = bud.limits([C("a", 28, history="constant"), C("b", 32, history="constant")], None)
check("constant budget since day 1: month 1,824 (60 x 30.4)", r["month_limit"] == 1824 and r["change_day_limit"] == 120, str(r))
r = bud.limits([C("existing", 10, spend_at_change=200, days_at_change=16, max_today=20), C("new", 0, new=5, spend=0)], 16)
check("earlier change this month + new campaign: 440 (not 384)", r["month_limit"] == 440, str(r))
check("change day uses the highest budget of the day (2 x (20 + 5))", r["change_day_limit"] == 50, str(r))
r = bud.limits([C("back", 0, new=5, spend=120)], 10)
check("re-enabling keeps the spend already made this month (120 + 5 x 10)", r["month_limit"] == 170, str(r))
for name, campaigns, days in (("no history", [C("x", 10)], 16), ("change without spend", [C("x", 10, new=12)], 16),
                              ("negative days", [C("x", 30, new=40, spend=300)], -10),
                              ("days above 31", [C("x", 30, new=40, spend=300)], 40),
                              ("repeated name", [C("s", 10, history="constant"), C("s", 20, history="constant")], None)):
    try:
        bud.limits(campaigns, days)
        check(f"budget refuses {name}", False, "accepted")
    except ValueError:
        check(f"budget refuses {name}", True)
code, out = run("budget.py", "--cap-month", "800", "--campaign", "name=Search A,budget=10,history=constant",
                "--campaign", "name=Search B,budget=20,history=constant")
check("CLI: 912 against a cap of 800 is EXCEEDS with exit 1", code == 1 and "912" in out, out)
for label, extra in (("NaN", ["--campaign", "name=a,budget=nan,new=40,spend=300"]),
                     ("infinity", ["--campaign", "name=a,budget=30,new=inf,spend=300"]),
                     ("negative", ["--campaign", "name=a,budget=30,new=40,spend=-1"]),
                     ("undetermined", ["--campaign", "name=a,budget=30"]),
                     ("no campaign and no window", [])):
    code, out = run("budget.py", "--days-left", "10", *extra)
    check(f"CLI refuses {label} with exit 2", code == 2 and "Traceback" not in out, out)
# Budget window: 600 over 10 days, counting the first and the last.
r = bud.window(600, 10, None)
check("window: 600 over 10 days gives 30.00", r["daily_cap_total"] == 30.0, str(r))
r = bud.window(700, 9, None)
check("window: 700 over 9 days rounds down to 38.88 (38.89 x 18 = 700.02)", r["daily_cap_total"] == 38.88, str(r))
for label, camp in (("lowering 90 to 30 today", C("s", 90, new=30, max_today=90)),
                    ("max_today=90 with a current 10", C("s", 10, new=30, max_today=90))):
    r = bud.window(600, 10, [camp])
    check(f"window: {label} exposes 720 (180 + 9 x 60)", close(r["max_window_exposure"], 720, 1e-6), str(r))
r = bud.window(600, 10, [C("s", 90, new=30)], starts_today=False)
check("window starting tomorrow: 10 x 60 = 600 fits", close(r["max_window_exposure"], 600, 1e-6), str(r))
r = bud.window(500, 1, [C("s", 300, new=250, max_today=300)])
check("one-day window: lowering 300 to 250 today still exposes 600", r["max_window_exposure"] == 600, str(r))
for label, camp, expected in (("60/day goes over, exit 1", "name=s,budget=10,new=60,max_today=10", 1),
                              ("30/day fits, exit 0", "name=s,budget=10,new=30,max_today=10", 0),
                              ("30.01/day goes over by 20 cents, exit 1", "name=s,budget=10,new=30.01,max_today=10", 1),
                              ("window today without max_today, exit 2", "name=s,budget=10,new=30", 2)):
    code, out = run("budget.py", "--window-budget", "600", "--window-days", "10", "--campaign", camp)
    check(f"CLI window: {label}", code == expected, out)
code, out = run("budget.py", "--window-budget", "600", "--window-days", "10", "--window-start", "tomorrow",
                "--campaign", "name=s,budget=90,new=30")
check("CLI window starting tomorrow does not ask for max_today", code == 0, out)
for label, extra in (("window without days", ["--window-budget", "500"]),
                     ("NaN window", ["--window-budget", "nan", "--window-days", "9"]),
                     ("40-day window", ["--window-budget", "500", "--window-days", "40"])):
    code, out = run("budget.py", *extra)
    check(f"CLI refuses {label} with exit 2", code == 2 and "Traceback" not in out, out)

# ----------------------------------------------------------------- n-grams
check("normalization keeps accents", ng.normalize("Manutenção de Ar!") == ["manutenção", "de", "ar"])
check("--strip-accents merges spellings", ng.normalize("Manutenção", strip_accents=True) == ["manutencao"])
check("whole word: 'art' does not match 'smart watch'", not ng.contains_word("smart watch", "art"))
check("whole word: 'art' matches 'wall art prints'", ng.contains_word("wall art prints", "art"))
en = {t["term"]: t for t in ng.read_csv(FIX / "search_terms_en.csv")}
check("English CSV: skips preamble and the Total row, keeps a term that starts with 'total'",
      set(en) == {"emergency plumber near me", "how to fix a leaking tap", "plumbing course online", "total plumbing services"},
      str(list(en)))
check("English CSV: '1,234.56' becomes 1234.56 and conv value is read",
      close(en["emergency plumber near me"]["cost"], 1234.56, 1e-9) and en["emergency plumber near me"]["value"] == 800)
pt = {t["term"]: t for t in ng.read_csv(FIX / "search_terms_pt.csv")}
check("Portuguese CSV: ';', decimal comma and accents", close(pt.get("manutenção de ar condicionado", {}).get("cost", 0), 1234.56, 1e-9)
      and len(pt) == 3, str(pt))
api = ng.read_json(FIX / "api_terms.json")
check("API JSON: 6 rows, cost in micros, campaign_search_term_view accepted, value read",
      len(api) == 6 and close(api[0]["cost"], 12.0, 1e-9) and api[0]["value"] == 300 and api[5]["term"] == "cheap shoes", str(api))
try:
    ng.read_json(FIX / "api_terms_paginated.json")
    check("JSON with nextPageToken is refused", False, "accepted")
except ng.InvalidInput:
    check("JSON with nextPageToken is refused", True)
base = {"clicks": 110, "conv": 33, "cost": 660, "visible_cost": 303, "visible_clicks": 60}
synthetic = [{"term": "alpha beta", "clicks": 9, "impr": 90, "cost": 45, "conv": 0, "value": 0},
             {"term": "gamma delta", "clicks": 30, "impr": 300, "cost": 150, "conv": 0, "value": 0},
             {"term": "epsilon zeta", "clicks": 20, "impr": 200, "cost": 100, "conv": 8, "value": 400},
             {"term": "eta theta", "clicks": 1, "impr": 10, "cost": 8, "conv": 2, "value": 0}]
r = ng.analyze(synthetic, base, 3, None)
row = {(x["n"], x["gram"]): x for x in r["rows"]}
check("k=3: p = 0.10", close(r["click_p"], 0.10, 1e-9))
check("9 clicks without conversion: LOW DATA", row[(2, "alpha beta")]["suggestion"] == "LOW DATA")
check("30 clicks without conversion: REVIEW INTENT", row[(2, "gamma delta")]["suggestion"] == "REVIEW INTENT")
check("CPA 12.5 against a base of 20: PROMOTE? and ROAS 4", row[(2, "epsilon zeta")]["suggestion"] == "PROMOTE?"
      and row[(2, "epsilon zeta")]["roas"] == 4)
check("one click with 2 conversions does not break", row[(2, "eta theta")]["conv"] == 2.0)
check("coverage = visible cost / total cost (303/660)", close(r["coverage"]["cost"], 303 / 660, 1e-4), str(r["coverage"]))
r = ng.analyze(synthetic, base, None, None)
check("without a unit, zero conversions is NO BASE, never a cut",
      all(x["suggestion"] in ("NO BASE", "PROMOTE?", "") for x in r["rows"]) and r["click_p"] is None)
with tempfile.TemporaryDirectory() as tmp:
    out_csv = str(Path(tmp) / "out.csv")
    code, out = run("n_gram_analysis.py", str(FIX / "search_terms_pt.csv"), "--out", out_csv)
    check("CLI CSV without a unit runs and says NO BASE and unknown coverage", code == 0 and "NO BASE" in out
          and "unknown" in out, out)
    check("output CSV keeps 'manutenção'", "manutenção" in Path(out_csv).read_text(encoding="utf-8-sig"))
    code, out = run("n_gram_analysis.py", str(FIX / "search_terms_en.csv"), "--min-cost", "10", "--out", out_csv)
    check("old CLI (csv, --min-cost, --out) still works", code == 0 and Path(out_csv).exists(), out)
    bad = Path(tmp) / "bad.csv"
    bad.write_text("Search term,Clicks,Cost,Conversions\nabc,1.2.3,5,0\n", encoding="utf-8")
    for label, extra in (("missing CSV", [str(Path(tmp) / "missing.csv")]),
                         ("malformed number", [str(bad)]),
                         ("risk 0", [str(FIX / "search_terms_pt.csv"), "--risk", "0"]),
                         ("k zero", [str(FIX / "search_terms_pt.csv"), "--actions-per-click", "0"]),
                         ("paginated JSON", [str(FIX / "api_terms_paginated.json")])):
        code, out = run("n_gram_analysis.py", *extra, "--out", out_csv)
        check(f"n-gram refuses {label} with exit 2, no traceback", code == 2 and "Traceback" not in out, out)
    p = subprocess.run([sys.executable, str(SCRIPTS / "n_gram_analysis.py"), str(FIX / "search_terms_pt.csv"),
                        "--out", out_csv], capture_output=True, text=True, encoding="utf-8", errors="replace")
    check("n-gram run without -B leaves no __pycache__", p.returncode == 0 and not list(ROOT.rglob("__pycache__")), p.stderr)

# ----------------------------------------------------------------- negative keywords (g/2453972)
T = neg.tokens
check("negative: case does not matter", neg.blocks("PHRASE", T("Free Estimate"), T("free estimate roof")))
check("negative: accents matter ('cafe' does not block 'café')", not neg.blocks("BROAD", T("cafe"), T("café near me")))
check("negative: 'café' blocks 'café near me'", neg.blocks("BROAD", T("café"), T("café near me")))
check("negative: '&' and 'and' differ", not neg.blocks("PHRASE", T("socks and shoes"), T("socks & shoes outlet"))
      and neg.blocks("PHRASE", T("socks & shoes"), T("socks & shoes outlet")))
check("negative: no plural ('shoe' does not block 'cheap shoes')", not neg.blocks("BROAD", T("shoe"), T("cheap shoes")))
check("broad negative: any order", neg.blocks("BROAD", T("repair roof"), T("free estimate roof repair")))
check("phrase negative: only the sequence", not neg.blocks("PHRASE", T("repair roof"), T("free estimate roof repair")))
check("exact negative: only the identical search", neg.blocks("EXACT", T("roof repair"), T("roof repair"))
      and not neg.blocks("EXACT", T("roof repair"), T("roof repair cost")))
seventeen = [f"w{i}" for i in range(1, 17)] + ["cheap"]
check("negative: a word after the 16th does not count", not neg.blocks("BROAD", ["cheap"], seventeen)
      and neg.blocks("BROAD", ["w16"], seventeen))
check("exact negative of 16 words does not block the search with one more",
      not neg.blocks("EXACT", seventeen[:16], seventeen[:16] + ["extra"]) and neg.blocks("EXACT", seventeen[:16], seventeen[:16]))
for text, reading in (("dark -chocolate", [["dark"]]), ('"OR dark chocolate"', [["dark", "chocolate"]]),
                      ("[site:www.example.com dark chocolate]", [["dark", "chocolate"]]), ("Fifth Ave.", [["fifth", "ave"]])):
    check(f"candidate {text!r} reads as {reading}", neg.candidate_readings(text)[1] == reading, str(neg.candidate_readings(text)))
check("hyphen inside a word tests joined and split",
      sorted(map(tuple, neg.candidate_readings("do-it-yourself")[1])) == [("do", "it", "yourself"), ("doityourself",)])
probe = [{"term": "dark roast coffee", "clicks": 1, "cost": 1, "conv": 1}, {"term": "dark chocolate", "clicks": 1, "cost": 1, "conv": 1}]
r = {x["candidate"]: x for x in neg.check(["dark -chocolate", '"OR dark chocolate"'], probe, [])}
check("'dark -chocolate' blocks the converted 'dark roast coffee' (works as 'dark')",
      r["dark -chocolate"]["verdict"] == "BLOCKS CONVERSION" and r["dark -chocolate"]["terms_blocked"] == 2)
check("'OR dark chocolate' blocks the converted 'dark chocolate'", r['"OR dark chocolate"']["verdict"] == "BLOCKS CONVERSION")
for text, kind in (('"free"', "PHRASE"), ("[diy kit]", "EXACT"), ("free", "BROAD")):
    check(f"candidate {text} is {kind}", neg.candidate(text)[0] == kind)
for text in ('"free', "[diy", "diy]", '""', "[ ]", "free*", "inurl:example", "hello!", "price (cheap)", "-chocolate", "site:example.com"):
    try:
        neg.candidate_readings(text)
        check(f"malformed or unmodeled candidate {text!r} is refused", False, "accepted")
    except ng.InvalidInput:
        check(f"malformed or unmodeled candidate {text!r} is refused", True)
r = {x["candidate"]: x for x in neg.check(['"free"', '"free download"', "estimate"], api, neg.read_keywords(FIX / "keywords.txt"))}
check("'free' blocks a converted term (1 + 0.9992 of the same term)",
      r['"free"']["verdict"] == "BLOCKS CONVERSION" and close(r['"free"']["converted_blocked"][0]["conv"], 1.9992, 1e-6), str(r['"free"']))
check("'free download' only blocks the download term", r['"free download"']["verdict"] == "OK" and r['"free download"']["terms_blocked"] == 1)
check("single-word 'estimate': blocks the active keyword and warns", "free estimate" in r["estimate"]["keywords_blocked"]
      and r["estimate"]["warnings"])
kw = neg.read_keywords(FIX / "keywords_api.json")
check("keywords from JSON: only active and positive", kw == ["roof design template"], str(kw))
check("exact negative equal to an active keyword is a conflict", neg.check(["[roof design template]"], [], kw)[0]["verdict"] == "BLOCKS KEYWORD")
code, out = run("negatives.py", "--terms", str(FIX / "api_terms.json"), "--keywords", str(FIX / "keywords.txt"),
                "--candidate", '"free"', "--candidate", '"free download"')
check("CLI negatives: a blocked conversion exits 1", code == 1 and "BLOCKS CONVERSION" in out, out)
code, out = run("negatives.py", "--terms", str(FIX / "search_terms_en.csv"), "--candidate", '"course"', "--json")
check("CLI negatives: CSV input, OK exits 0 with JSON", code == 0 and json.loads(out)["failed"] == 0, out)
for label, extra in (("paginated JSON", ["--terms", str(FIX / "api_terms_paginated.json"), "--candidate", "x"]),
                     ("open mark", ["--terms", str(FIX / "api_terms.json"), "--candidate", '"free']),
                     ("asterisk", ["--terms", str(FIX / "api_terms.json"), "--candidate", "free*"]),
                     ("no candidate", ["--terms", str(FIX / "api_terms.json")]),
                     ("missing file", ["--terms", str(FIX / "missing.csv"), "--candidate", "x"])):
    code, out = run("negatives.py", *extra)
    check(f"CLI negatives refuses {label} with exit 2", code == 2 and "Traceback" not in out, out)

# ----------------------------------------------------------------- input safety (review of Oct 3, 2026)
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    # A cap that is given is never ignored in window mode.
    code, out = run("budget.py", "--window-budget", "600", "--window-days", "10", "--cap-day", "10", "--cap-month", "100",
                    "--campaign", "name=s,budget=30,history=constant,max_today=30")
    check("window with daily and monthly caps exceeded exits 1 (912 > 100, 30 > 10)",
          code == 1 and "912" in out and "cap 10" in out, out)
    code, out = run("budget.py", "--window-budget", "600", "--window-days", "10", "--cap-month", "100")
    check("window with a cap and no campaign is refused (exit 2)", code == 2, out)
    code, out = run("budget.py", "--window-budget", "600", "--window-days", "10", "--cap-month", "2000",
                    "--campaign", "name=s,budget=30,max_today=30")
    check("window with a cap and a campaign without history is refused (exit 2)", code == 2, out)
    code, out = run("budget.py", "--window-budget", "600", "--window-days", "10", "--cap-month", "2000",
                    "--campaign", "name=s,budget=30,history=constant,max_today=30")
    check("window and caps within limits exit 0", code == 0, out)
    # Malformed numbers and truncated rows never become zero or disappear.
    for label, content in (("NaN", "Search term,Clicks,Cost,Conversions\nfree estimate,12,30,NaN\n"),
                           ("text", "Search term,Clicks,Cost,Conversions\nfree estimate,12,30,abc\n"),
                           ("negative number", "Search term,Clicks,Cost,Conversions\nfree estimate,12,-30,1\n"),
                           ("truncated row", "Search term,Clicks,Cost,Conversions\nfree estimate,12,30\n")):
        f = tmp / f"bad-{label.replace(' ', '-')}.csv"
        f.write_text(content, encoding="utf-8")
        code, out = run("negatives.py", "--terms", str(f), "--candidate", "free")
        check(f"negatives refuses a CSV with {label} (exit 2), never OK", code == 2 and "Traceback" not in out, out)
        code, out = run("n_gram_analysis.py", str(f), "--out", str(tmp / "o.csv"))
        check(f"n-gram refuses a CSV with {label} (exit 2)", code == 2 and "Traceback" not in out, out)
    good = tmp / "currencies.csv"
    good.write_text("Search term,Clicks,Cost,Conversions\na,1,\"US$ 1,234.56\",1.00\nb,2,$3.50,--\nc,1,,0\n\n", encoding="utf-8")
    rows = {t["term"]: t for t in ng.read_csv(good)}
    check("currency, thousands, '--', empty values and blank lines are still accepted",
          close(rows["a"]["cost"], 1234.56, 1e-9) and rows["b"]["conv"] == 0 and rows["c"]["cost"] == 0, str(rows))
    # Any positive credit protects the term.
    for credit in (0.0001, 0.004, 0.005):
        f = tmp / f"credit-{credit}.json"
        f.write_text(json.dumps({"results": [{"searchTermView": {"searchTerm": "free estimate"},
                                              "metrics": {"clicks": 12, "costMicros": 30000000, "conversions": credit}}]}),
                     encoding="utf-8")
        code, out = run("negatives.py", "--terms", str(f), "--candidate", "free")
        check(f"credit {credit} protects the term (BLOCKS CONVERSION, exit 1)", code == 1 and "BLOCKS CONVERSION" in out, out)
    r = ng.analyze([{"term": "x y", "clicks": 50, "impr": 0, "cost": 10, "conv": 0.004, "value": 0}],
                   {"clicks": 100, "conv": 30, "cost": 600}, 3, None)
    check("in the n-gram, a 0.004 credit is not 'zero conversions'", all(x["suggestion"] == "" for x in r["rows"]), str(r["rows"]))
    f = tmp / "zero.json"
    f.write_text(json.dumps({"results": [{"searchTermView": {"searchTerm": "free download"}, "metrics": {"clicks": 3}}]}),
                 encoding="utf-8")
    code, out = run("negatives.py", "--terms", str(f), "--candidate", "free")
    check("zero conversions stays OK and warns that nothing converted in the data", code == 0 and "WARNING" in out, out)
    # Malformed keyword JSON.
    f = tmp / "kw.json"
    f.write_text(json.dumps({"results": [{"adGroupCriterion": {"status": "ENABLED", "keyword": "free estimate"}}]}),
                 encoding="utf-8")
    code, out = run("negatives.py", "--terms", str(FIX / "api_terms.json"), "--keywords", str(f), "--candidate", "x")
    check("a keyword that is not an object exits 2, no traceback", code == 2 and "Traceback" not in out, out)

# ----------------------------------------------------------------- repo hygiene
with tempfile.TemporaryDirectory() as tmp:
    errors = []
    for script in sorted(SCRIPTS.glob("*.py")):
        try:
            py_compile.compile(str(script), cfile=str(Path(tmp) / (script.stem + ".pyc")), doraise=True)
        except py_compile.PyCompileError as err:
            errors.append(str(err))
    check("every script compiles (bytecode outside the repo)", not errors, "; ".join(errors))
text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
m = re.search(r'^description:\s*"?(.+?)"?\s*$', text, re.M)
description = m.group(1) if m else ""
check("SKILL.md description between 150 and 400 characters", 150 <= len(description) <= 400, f"{len(description)}: {description}")
cited, dead = set(), []
for md in sorted(ROOT.rglob("*.md")):
    if ".git" in md.parts or md.name == "CHANGELOG.md":  # the changelog names removed files on purpose
        continue
    for item in re.findall(r"`([^`\n]+)`", md.read_text(encoding="utf-8")):
        item = item.strip()
        if " " not in item and item.startswith(("references/", "scripts/", "assets/", "agents/", ".github/")) \
                and not any(x in item for x in ("<", "*")):
            cited.add(item)
            if not (ROOT / item).exists():
                dead.append(f"{md.relative_to(ROOT)}: {item}")
check("every repo path cited in backticks exists", not dead, "; ".join(dead))
bad = [p for p in ROOT.rglob("*") if ".git" not in p.parts and (p.name.startswith(".env") or p.name == "__pycache__")]
check("no .env and no __pycache__ in the repo", not bad, str(bad))
# Public text: no em dash anywhere, no spaced hyphen or spaced en dash used as punctuation outside code.
punct, personal = [], []
for f in sorted(ROOT.rglob("*")):
    if ".git" in f.parts or not f.is_file() or f.suffix not in (".md", ".py", ".txt", ".yml", ".yaml", ".json", ".csv"):
        continue
    content = f.read_text(encoding="utf-8-sig")
    if chr(0x2014) in content:
        punct.append(f"{f.relative_to(ROOT)}: em dash")
    if re.search(r"[A-Za-z]:[\\/]Users[\\/]|/home/[a-z]|Desktop[\\/]", content) and f.name != "self_test.py":
        personal.append(str(f.relative_to(ROOT)))
    if f.suffix == ".md":
        prose = re.sub(r"```.*?```", "", content, flags=re.S)
        prose = re.sub(r"`[^`\n]*`", "", prose)
        for n, line in enumerate(prose.splitlines(), 1):
            if re.search(r"\S - \S|\S \u2013 \S", line):
                punct.append(f"{f.relative_to(ROOT)}: spaced dash: {line.strip()[:60]}")
check("no em dash and no spaced hyphen used as punctuation", not punct, "; ".join(punct[:10]))
check("no personal paths in public files", not personal, "; ".join(personal))

print(f"\n{len(FAILURES)} failure(s)" if FAILURES else "\nall green")
sys.exit(1 if FAILURES else 0)
