#!/usr/bin/env python3
"""Low-volume statistics for Google Ads, standard library only.

The unit for every probability here is the CONVERTED CLICK: p = probability that one click produces at least
one conversion. Google Ads counts actions, not converted clicks: one click can produce two conversions (a call
and a form), an action counted "Every" counts several times per click, and data-driven attribution gives
fractional credit. So the default base is the CONSERVATIVE p:

    p = conversions / (clicks * k)

with k = the maximum number of primary conversions one click can produce (the number of primary actions
counted "One", `conversion_action.counting_type = ONE_PER_CLICK`). A smaller p asks for more clicks before
cutting, so the error stays on the safe side. Without k and without a p measured outside the platform
(`--click-cvr`, unique clicks that became leads in your CRM), there is no base: the answer is NO BASE, never a
number.

    python stats.py base --conversions 30 --clicks 100 --actions-per-click 3
    python stats.py zero --n 21 --click-cvr 0.02
    python stats.py clicks --conversions 30 --clicks 100 --actions-per-click 3
    python stats.py poisson --events 5
    python stats.py cpa --cost 400 --conversions 5
    python stats.py rate --successes 0 --trials 150
    python stats.py compare --a 0/10 --b 4/10

Every subcommand accepts --json (infinity, such as the upper CPA bound with zero conversions, is printed as
null). Exit codes: 0 answer, 3 NO BASE, 2 invalid input (non-finite or negative number, risk or confidence
outside (0, 1), successes above trials, k below 1), never a traceback. Usage: references/08-low-volume.md.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from statistics import NormalDist

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")


class NoBase(ValueError):
    """The base does not allow an honest statistical answer (unknown unit or no data)."""


def click_p(conversions: float, clicks: float, actions_per_click: int | None = None,
            click_cvr: float | None = None) -> float:
    """Probability that one click converts: the p measured outside, or the conservative p from k actions."""
    if click_cvr is not None:
        if not 0 < click_cvr < 1:
            raise NoBase(f"--click-cvr must be between 0 and 1 (got {click_cvr})")
        return click_cvr
    if actions_per_click is None:
        raise NoBase("unknown unit: pass --actions-per-click (primary actions counted 'One') or a --click-cvr "
                     "measured outside the platform")
    if actions_per_click < 1:
        raise NoBase("--actions-per-click must be 1 or more")
    if clicks <= 0:
        raise NoBase("base without clicks")
    if conversions <= 0:
        raise NoBase("base without conversions: the rate cannot be estimated")
    p = conversions / (clicks * actions_per_click)
    if p >= 1:
        raise NoBase(f"p = {p:.3f} >= 1: a primary action counts 'Every', or k is too low")
    return p


def p_zero(p: float, clicks: float) -> float:
    """P(no click converts in n clicks) with probability p per click."""
    return (1 - p) ** clicks


def min_clicks(p: float, risk: float = 0.05) -> int:
    """Smallest n with P(0 | p, n) < risk: below it, zero conversions is compatible with a good term."""
    return math.ceil(math.log(risk) / math.log(1 - p))


def _poisson_cdf(k: int, lam: float) -> float:
    """P(X <= k) in log scale (log-sum-exp): a direct exp(-lam) underflows to zero from lam ~ 745."""
    if lam <= 0:
        return 1.0
    log_lam = math.log(lam)
    logs = [-lam + i * log_lam - math.lgamma(i + 1) for i in range(k + 1)]
    top = max(logs)
    return min(1.0, math.exp(top) * math.fsum(math.exp(x - top) for x in logs))


def _bisect(f, lo: float, hi: float) -> float:
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def poisson_ci(events: float, conf: float = 0.95) -> tuple[float, float]:
    """Exact (Garwood) interval for the mean of a count. Fractional credit is rounded."""
    k = int(round(events))
    alpha = (1 - conf) / 2
    lower = 0.0 if k == 0 else _bisect(lambda lam: (1 - _poisson_cdf(k - 1, lam)) - alpha, 0, k + 50)
    upper = _bisect(lambda lam: alpha - _poisson_cdf(k, lam), 0, 5 * k + 50)
    return lower, upper


def cpa_ci(cost: float, conversions: float, conf: float = 0.95) -> tuple[float, float]:
    """CPA interval: cost divided by the Poisson interval of conversions (inf when the lower bound is zero)."""
    lower, upper = poisson_ci(conversions, conf)
    return cost / upper, (math.inf if lower == 0 else cost / lower)


def rate_ci(successes: int, trials: int, conf: float = 0.95) -> dict:
    """Wilson interval; with zero successes it also returns the rule of three (upper bound ~ 3/n at 95%)."""
    if trials <= 0:
        raise NoBase("no trials")
    z = NormalDist().inv_cdf(1 - (1 - conf) / 2)
    f = successes / trials
    den = 1 + z * z / trials
    center = (f + z * z / (2 * trials)) / den
    half = z * math.sqrt(f * (1 - f) / trials + z * z / (4 * trials ** 2)) / den
    out = {"rate": f, "lower": max(0.0, center - half), "upper": min(1.0, center + half)}
    if successes == 0:
        out["rule_of_three"] = 3 / trials
    return out


def _hyper(x: int, n1: int, n2: int, total: int) -> float:
    return math.comb(n1, x) * math.comb(n2, total - x) / math.comb(n1 + n2, total)


def fisher(a: int, n1: int, b: int, n2: int) -> float:
    """Two-sided Fisher exact test for a/n1 against b/n2 (the right test with small samples)."""
    s = a + b
    lo, hi = max(0, s - n2), min(s, n1)
    observed = _hyper(a, n1, n2, s)
    p = sum(_hyper(x, n1, n2, s) for x in range(lo, hi + 1) if _hyper(x, n1, n2, s) <= observed * (1 + 1e-9))
    return min(1.0, p)


def _fraction(text: str) -> tuple[int, int]:
    try:
        k, n = text.split("/")
        return int(k), int(n)
    except ValueError as err:
        raise argparse.ArgumentTypeError(f"use successes/trials, like 3/40 (got {text})") from err


def _invalid(args) -> str | None:
    """Input with no honest answer: returns the reason (exit 2), never a traceback or an absurd number."""
    for name in ("n", "events", "cost", "conversions", "base_clicks", "click_cvr", "risk", "conf"):
        value = getattr(args, name, None)
        if value is not None and (not math.isfinite(value) or value < 0):
            return f"--{name.replace('_', '-')} must be finite and >= 0 (got {value})"
    for name in ("risk", "conf"):
        value = getattr(args, name, None)
        if value is not None and not 0 < value < 1:
            return f"--{name} must be between 0 and 1 (got {value})"
    cvr = getattr(args, "click_cvr", None)
    if cvr is not None and not 0 < cvr < 1:
        return f"--click-cvr must be between 0 and 1 (got {cvr})"
    k = getattr(args, "actions_per_click", None)
    if k is not None and k < 1:
        return "--actions-per-click must be 1 or more"
    if args.cmd == "rate" and (args.trials < 1 or not 0 <= args.successes <= args.trials):
        return f"rate needs 0 <= successes <= trials and trials >= 1 (got {args.successes}/{args.trials})"
    if args.cmd == "compare":
        for label, (k_, n_) in (("--a", args.a), ("--b", args.b)):
            if n_ < 1 or not 0 <= k_ <= n_:
                return f"{label} needs 0 <= successes <= trials and trials >= 1 (got {k_}/{n_})"
    return None


def _json(result: dict) -> str:
    """Valid JSON: infinity (CPA with no upper bound) becomes null."""
    clean = {k: (None if isinstance(v, float) and not math.isfinite(v) else v) for k, v in result.items()}
    return json.dumps(clean, ensure_ascii=False, default=str, allow_nan=False)


def _base(args) -> float:
    return click_p(args.conversions or 0, args.base_clicks or 0, args.actions_per_click, args.click_cvr)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Low-volume statistics for Google Ads.")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="JSON output")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def new(name: str, help_text: str) -> argparse.ArgumentParser:
        return sub.add_parser(name, help=help_text, parents=[common])

    def with_base(sp):
        sp.add_argument("--conversions", type=float, help="base conversions (mature days only)")
        sp.add_argument("--base-clicks", "--clicks", dest="base_clicks", type=float, help="base clicks (mature days)")
        sp.add_argument("--actions-per-click", type=int, help="k: primary actions counted 'One'")
        sp.add_argument("--click-cvr", type=float, help="p measured outside the platform (unique clicks that became leads)")

    with_base(new("base", "conservative converted-click p"))
    sp = new("zero", "P(zero conversions) in n clicks")
    with_base(sp)
    sp.add_argument("--n", type=float, required=True, help="clicks of the term or keyword")
    sp = new("clicks", "minimum clicks for P(0) < risk")
    with_base(sp)
    sp.add_argument("--risk", type=float, default=0.05)
    sp = new("poisson", "exact interval of a count")
    sp.add_argument("--events", type=float, required=True)
    sp.add_argument("--conf", type=float, default=0.95)
    sp = new("cpa", "CPA interval")
    sp.add_argument("--cost", type=float, required=True)
    sp.add_argument("--conversions", type=float, required=True)
    sp.add_argument("--conf", type=float, default=0.95)
    sp = new("rate", "Wilson interval of a rate (rule of three with zero)")
    sp.add_argument("--successes", type=int, required=True)
    sp.add_argument("--trials", type=int, required=True)
    sp.add_argument("--conf", type=float, default=0.95)
    sp = new("compare", "two-sided Fisher exact test between two rates")
    sp.add_argument("--a", type=_fraction, required=True, help="successes/trials of arm A")
    sp.add_argument("--b", type=_fraction, required=True, help="successes/trials of arm B")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exit_:
        return 0 if exit_.code == 0 else 2
    reason = _invalid(args)
    if reason:
        if args.json:
            print(json.dumps({"status": "INVALID INPUT", "reason": reason}))
        else:
            print(f"ERROR: {reason}", file=sys.stderr)
        return 2

    try:
        if args.cmd == "base":
            p = _base(args)
            r = {"click_p": p, "min_clicks_5pct": min_clicks(p)}
        elif args.cmd == "zero":
            p = _base(args)
            r = {"click_p": p, "clicks": args.n, "p_zero": p_zero(p, args.n)}
        elif args.cmd == "clicks":
            p = _base(args)
            r = {"click_p": p, "risk": args.risk, "min_clicks": min_clicks(p, args.risk)}
        elif args.cmd == "poisson":
            lo, hi = poisson_ci(args.events, args.conf)
            r = {"events": args.events, "conf": args.conf, "lower": lo, "upper": hi,
                 "rounded": int(round(args.events)) != args.events}
        elif args.cmd == "cpa":
            lo, hi = cpa_ci(args.cost, args.conversions, args.conf)
            r = {"cpa": args.cost / args.conversions if args.conversions else math.inf,
                 "cpa_lower": lo, "cpa_upper": hi, "conf": args.conf}
        elif args.cmd == "rate":
            r = rate_ci(args.successes, args.trials, args.conf)
        else:
            (a, n1), (b, n2) = args.a, args.b
            r = {"a": f"{a}/{n1}", "b": f"{b}/{n2}", "p_fisher_two_sided": fisher(a, n1, b, n2)}
    except NoBase as err:
        print(json.dumps({"status": "NO BASE", "reason": str(err)}) if args.json else f"NO BASE: {err}")
        return 3

    if args.json:
        print(_json(r))
    else:
        for key, value in r.items():
            print(f"{key}: {round(value, 6) if isinstance(value, float) else value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
