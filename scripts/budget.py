#!/usr/bin/env python3
"""Google Ads spend limits by the official rule, including the month in which the budget changes.

Rule (support.google.com/google-ads/answer/6385083 and /answer/10487143, checked Oct 1, 2026):
- on a single day, a campaign can spend up to 2x its average daily budget;
- on the day the budget changes, the daily limit is 2x the HIGHEST budget chosen that day;
- in a month with a constant budget since day 1, the monthly limit is daily budget x 30.4;
- when the budget changes, the monthly limit becomes spend so far + new budget x days left, COUNTING the day
  of the change. That limit stays fixed until the next change.

So each campaign declares its own history this month; the script refuses the undetermined case instead of
assuming 30.4. Format (key=value, comma separated):

  name=search,budget=30,new=36,spend=450        changes now: limit = spend + new x --days-left
  name=b,budget=30,history=constant              no change this month: limit = 30.4 x budget
  name=c,budget=10,spend_at_change=200,days_at_change=16
                                                 changed earlier this month: limit = 200 + 10 x 16
  name=c,budget=10,month_limit=360               same, with the limit already computed
  name=new,budget=0,new=5,spend=0                new campaign: a change from 0 to 5
  name=back,budget=0,new=5,spend=120             re-enabled: the spend it already had this month counts
  max_today=20                                   (optional) highest budget already chosen today

A shared budget counts as one campaign. The sum is checked against the cap the account owner approved
(--cap-day for the sum of daily budgets, --cap-month for the sum of monthly limits). Spending up to 2x on a
single day is NOT an overspend: Google balances it within the month.

    python budget.py --days-left 16 --cap-month 1824 \\
      --campaign name=search,budget=30,new=36,spend=450 --campaign name=brand,budget=30,new=21,spend=450

Budget window (promotional credit, event budget): to stay under S over N days, counting the first and the last
day in the account time zone, the sum of daily budgets stays at S / (2 x N), rounded down to cents, because Google
can spend 2x every day. That holds when no higher budget was chosen on the first day: on a change day the limit is
2x the HIGHEST budget of the day (lowering from 90 to 30 today still exposes 180 today). With --campaign, the
script adds up the real exposure and, when the window starts today, requires max_today= on every campaign (use
the current budget if it did not change today); without it, it refuses (exit 2).

    python budget.py --window-budget 600 --window-days 10
    python budget.py --window-budget 600 --window-days 10 --campaign name=search,budget=10,new=30,max_today=10
    python budget.py --window-budget 600 --window-days 10 --window-start tomorrow --campaign name=search,budget=90,new=30

Exit codes: 0 within the cap, 1 over the cap (EXCEEDS), 2 invalid input (repeated name, negative number, NaN,
infinity, days outside 1 to 31, undetermined history), never a traceback.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from decimal import ROUND_FLOOR, Decimal

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

DAYS_PER_MONTH = 30.4
NUMBERS = ("budget", "new", "spend", "spend_at_change", "days_at_change", "month_limit", "max_today")


@dataclass
class Campaign:
    name: str
    budget: float
    new: float | None = None
    spend: float | None = None
    history: str | None = None
    spend_at_change: float | None = None
    days_at_change: float | None = None
    month_limit: float | None = None
    max_today: float | None = None

    @property
    def changes_now(self) -> bool:
        return self.new is not None and self.new != self.budget

    @property
    def daily_after(self) -> float:
        return self.new if self.new is not None else self.budget


def _campaign(text: str) -> Campaign:
    fields = {}
    for part in text.split(","):
        if "=" not in part:
            raise argparse.ArgumentTypeError(f"use comma separated key=value (got {part!r})")
        key, value = (x.strip() for x in part.split("=", 1))
        if key in NUMBERS:
            try:
                number = float(value)
            except ValueError as err:
                raise argparse.ArgumentTypeError(f"{key} is not a number: {value}") from err
            if not math.isfinite(number) or number < 0:
                raise argparse.ArgumentTypeError(f"{key} must be finite and >= 0 (got {value})")
            fields[key] = number
        elif key in ("name", "history"):
            fields[key] = value
        else:
            raise argparse.ArgumentTypeError(f"unknown key: {key}")
    if "name" not in fields or "budget" not in fields:
        raise argparse.ArgumentTypeError("every campaign needs name= and budget=")
    if fields.get("history") not in (None, "constant"):
        raise argparse.ArgumentTypeError("history only accepts 'constant'")
    return Campaign(**fields)


def _unique(campaigns: list[Campaign]) -> None:
    names = [c.name for c in campaigns]
    repeated = sorted({n for n in names if names.count(n) > 1})
    if repeated:
        # The name identifies the campaign in the output; repeated, one would overwrite the other.
        raise ValueError(f"repeated campaign name: {', '.join(repeated)}; use the id or a unique name")


def month_limit(c: Campaign, days_left: int | None) -> float:
    """Monthly limit of one campaign, or ValueError when its history does not determine the limit."""
    if c.changes_now:
        if c.spend is None or days_left is None:
            raise ValueError(f"{c.name}: a change now needs spend= (spend this month so far) and --days-left")
        return c.spend + c.new * days_left
    if c.month_limit is not None:
        return c.month_limit
    if c.spend_at_change is not None and c.days_at_change is not None:
        return c.spend_at_change + c.budget * c.days_at_change
    if c.history == "constant":
        return c.budget * DAYS_PER_MONTH
    raise ValueError(f"{c.name}: undetermined limit; pass history=constant, month_limit=, or spend_at_change= and "
                     "days_at_change= (did the budget change on any day this month?)")


def limits(campaigns: list[Campaign], days_left: int | None) -> dict:
    if days_left is not None and not 1 <= days_left <= 31:
        raise ValueError("--days-left goes from 1 to 31 (it counts the day of the change)")
    for c in campaigns:
        if c.days_at_change is not None and not 1 <= c.days_at_change <= 31:
            raise ValueError(f"{c.name}: days_at_change goes from 1 to 31")
    _unique(campaigns)
    # The sum comes from the list, never from the display dictionary.
    monthly = [month_limit(c, days_left) for c in campaigns]
    change_day = 2 * sum(max(c.budget, c.daily_after, c.max_today or 0) for c in campaigns)
    return {
        "daily_budget_before": sum(c.budget for c in campaigns),
        "daily_budget_after": sum(c.daily_after for c in campaigns),
        "change_day_limit": change_day,
        "next_day_limit": 2 * sum(c.daily_after for c in campaigns),
        "month_limit": round(sum(monthly), 2),
        "month_limit_by_campaign": {c.name: round(v, 2) for c, v in zip(campaigns, monthly)},
    }


def window(budget: float, days: int, campaigns: list[Campaign] | None, starts_today: bool = True) -> dict:
    """Window cap and, with campaigns, the real exposure: day 1 at the highest budget of the day if it is today."""
    if not math.isfinite(budget) or budget <= 0:
        raise ValueError("--window-budget must be finite and > 0")
    if not 1 <= days <= 31:
        raise ValueError("--window-days goes from 1 to 31 (it counts the first and the last day)")
    _unique(campaigns or [])
    # Rounded down to cents: 30.01 x 20 = 600.20 would go over a balance of 600.
    cap = (Decimal(repr(budget)) * 100 / (2 * days)).to_integral_value(rounding=ROUND_FLOOR) / 100
    r = {"window_budget": budget, "window_days": days, "window_starts_today": starts_today,
         "daily_cap_total": float(cap),
         "assumption": "no higher budget chosen on the first day; check it with --campaign"}
    if campaigns:
        if starts_today:
            missing = [c.name for c in campaigns if c.max_today is None]
            if missing:
                raise ValueError("a window that starts today needs max_today= on every campaign (the highest budget "
                                 f"chosen today; the current one if it did not change): missing in {', '.join(missing)}")
            day1 = 2 * sum(max(c.budget, c.daily_after, c.max_today) for c in campaigns)
        else:
            day1 = 2 * sum(c.daily_after for c in campaigns)
        total = sum(c.daily_after for c in campaigns)
        r.pop("assumption")
        r["daily_budget_after"] = total
        r["first_day_limit"] = round(day1, 2)
        r["max_window_exposure"] = round(day1 + 2 * total * (days - 1), 2)
    return r


def _print(r: dict, as_json: bool, verdict: str) -> None:
    if as_json:
        print(json.dumps(r, ensure_ascii=False))
        return
    for key, value in r.items():
        if key != "alerts":
            print(f"{key}: {round(value, 2) if isinstance(value, float) else value}")
    print(verdict)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Google Ads spend limits by the official rule.")
    ap.add_argument("--campaign", type=_campaign, action="append",
                    help="key=value per campaign (see the top of this file); repeat for each one")
    ap.add_argument("--days-left", type=int, help="days left in the month, counting the day of the change")
    ap.add_argument("--cap-day", type=float, help="sum of daily budgets approved by the account owner")
    ap.add_argument("--cap-month", type=float, help="monthly spend approved by the account owner")
    ap.add_argument("--window-budget", type=float, help="maximum spend of a window (for example, a credit balance)")
    ap.add_argument("--window-days", type=int, help="days in the window, counting the first and the last (account time zone)")
    ap.add_argument("--window-start", choices=("today", "tomorrow"), default="today",
                    help="the window starts today (default; counts the change day) or tomorrow")
    ap.add_argument("--json", action="store_true")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exit_:
        return 0 if exit_.code == 0 else 2

    if (args.window_budget is None) != (args.window_days is None):
        print("ERROR: --window-budget and --window-days go together", file=sys.stderr)
        return 2
    given_caps = [x for x in (args.cap_day, args.cap_month) if x is not None]
    if any(not math.isfinite(x) or x < 0 for x in given_caps):
        print("ERROR: caps must be finite and >= 0", file=sys.stderr)
        return 2
    if args.window_budget is not None:
        try:
            r = window(args.window_budget, args.window_days, args.campaign, args.window_start == "today")
            if given_caps:
                # A cap that was given is never ignored; without campaigns there is nothing to add up.
                if not args.campaign:
                    raise ValueError("--cap-day and --cap-month need --campaign in window mode too")
                r["limits"] = limits(args.campaign, args.days_left)
        except ValueError as err:
            print(f"ERROR: {err}", file=sys.stderr)
            return 2
        alerts = []
        if "max_window_exposure" in r and r["max_window_exposure"] > args.window_budget + 1e-9:
            alerts.append(f"exposure of up to {r['max_window_exposure']:.2f} in the window goes over the budget "
                          f"{args.window_budget:.2f} (first day {r['first_day_limit']:.2f}; daily cap total "
                          f"{r['daily_cap_total']:.2f})")
        if "limits" in r:
            lim = r["limits"]
            if args.cap_day is not None and lim["daily_budget_after"] > args.cap_day + 1e-9:
                alerts.append(f"sum of daily budgets {lim['daily_budget_after']:.2f} goes over the cap {args.cap_day:.2f}")
            if args.cap_month is not None and lim["month_limit"] > args.cap_month + 1e-9:
                alerts.append(f"monthly limit {lim['month_limit']:.2f} goes over the cap {args.cap_month:.2f}")
        r["alerts"] = alerts
        _print(r, args.json, "EXCEEDS: " + "; ".join(alerts) if alerts else
               "within the window cap" + (" and the given caps" if "limits" in r else ""))
        return 1 if alerts else 0

    if not args.campaign:
        print("ERROR: pass --campaign (one or more) or the window (--window-budget and --window-days)", file=sys.stderr)
        return 2
    caps = [x for x in (args.cap_day, args.cap_month) if x is not None]
    if any(not math.isfinite(x) or x < 0 for x in caps):
        print("ERROR: caps must be finite and >= 0", file=sys.stderr)
        return 2
    try:
        r = limits(args.campaign, args.days_left)
    except ValueError as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 2

    alerts = []
    if args.cap_day is not None and r["daily_budget_after"] > args.cap_day + 1e-9:
        alerts.append(f"sum of daily budgets {r['daily_budget_after']:.2f} goes over the cap {args.cap_day:.2f}")
    if args.cap_month is not None and r["month_limit"] > args.cap_month + 1e-9:
        alerts.append(f"monthly limit {r['month_limit']:.2f} goes over the cap {args.cap_month:.2f}")
    r["alerts"] = alerts
    _print(r, args.json, "EXCEEDS: " + "; ".join(alerts) if alerts else "within the cap" if caps else "no cap given")
    return 1 if alerts else 0


if __name__ == "__main__":
    sys.exit(main())
