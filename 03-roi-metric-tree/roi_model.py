#!/usr/bin/env python3
"""ROI metric tree and scenario model for an AI initiative.

Builds, from one JSON assumptions file:
  1. a metric tree (north-star value down to the drivers you can measure weekly)
  2. three internally consistent scenarios (conservative / base / aggressive)
  3. break-even adoption and the safety margin versus the base case
  4. a two-way sensitivity grid (adoption x realization factor)

The point is the discipline: only P&L-linked value counts (realization factor),
human review time is a cost (verification tax), and the decision gate is a margin
above break-even, not a single optimistic ROI number.

Usage:  python roi_model.py --config assumptions.json --out out/
Standard library only. Assumptions are fictional.
"""
import argparse, csv, json
from pathlib import Path


def run(c, adoption, realization, cost_growth=0.0):
    users = c["seats"] * adoption
    gross = users * c["hours_saved_per_user_month"] * c["loaded_hourly_cost"] * 12
    verification = users * c["review_hours_per_user_month"] * c["loaded_hourly_cost"] * 12
    realized = gross * realization
    fixed = c["seats"] * c["license_per_seat_month"] * 12 + c["enablement_one_time"] + c["admin_governance_year"]
    usage = users * c["usage_cost_per_active_user_month"] * 12 * (1 + cost_growth)
    cost = fixed + usage + verification
    net = realized - cost
    return dict(adoption=adoption, realization=realization, active_users=users, gross=gross, realized=realized,
                verification=verification, fixed=fixed, usage=usage, cost=cost, net=net, roi=net / cost)


def break_even(c, realization, cost_growth=0.0):
    lo, hi = 0.0, 1.0
    if run(c, hi, realization, cost_growth)["net"] < 0:
        return None
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if run(c, mid, realization, cost_growth)["net"] < 0 else (lo, mid)
    return hi


def m(x): return ("-$" if x < 0 else "$") + f"{abs(x):,.0f}"
def p(x): return f"{x * 100:.1f}%"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default="assumptions.json")
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    c = json.load(open(a.config, encoding="utf-8"))
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    sc = {k: run(c, v["adoption"], v["realization"], v.get("cost_growth", 0)) for k, v in c["scenarios"].items()}
    base = c["scenarios"]["base"]
    be = break_even(c, base["realization"], base.get("cost_growth", 0))
    margin = base["adoption"] - be if be is not None else None
    gate = c["gate_margin_points"] / 100

    L = [f"# ROI model: {c['initiative']}", "", "## Metric tree", "```",
         f"Net annual value (north star)",
         f"├── Realized value = gross time value x realization factor",
         f"│   ├── Active users = seats ({c['seats']}) x adoption rate      <- weekly active usage",
         f"│   ├── Hours saved per active user per month ({c['hours_saved_per_user_month']})  <- time study / system data",
         f"│   ├── Loaded hourly cost (${c['loaded_hourly_cost']})",
         f"│   └── Realization factor (share that reaches the P&L)  <- avoided hires, overtime, retired tools",
         f"└── Total cost",
         f"    ├── Fixed: licences ${c['license_per_seat_month']}/seat/month + enablement + governance",
         f"    ├── Usage: ${c['usage_cost_per_active_user_month']}/active user/month (tokens, agents, connectors)",
         f"    └── Verification tax: {c['review_hours_per_user_month']} h/active user/month of human review", "```", "",
         "## Scenarios", "| | " + " | ".join(k.title() for k in sc) + " |", "|---|" + "---|" * len(sc)]
    for label, key, f in [("Adoption", "adoption", p), ("Realization factor", "realization", p), ("Active users", "active_users", lambda x: f"{x:.0f}"),
                          ("Realized value", "realized", m), ("Fixed cost", "fixed", m), ("Usage cost", "usage", m),
                          ("Verification tax", "verification", m), ("Total cost", "cost", m), ("Net value", "net", m), ("ROI", "roi", p)]:
        L.append(f"| {label} | " + " | ".join(f(s[key]) for s in sc.values()) + " |")
    L += ["", "## Decision gate",
          f"- Break-even adoption (base realization): **{p(be) if be is not None else 'not reachable'}**",
          f"- Base-case adoption: {p(base['adoption'])}; safety margin: **{(margin * 100):.1f} points**" if margin is not None else "- No break-even within 100% adoption",
          f"- Gate rule: margin of at least {c['gate_margin_points']} points -> **{'PASS' if margin is not None and margin >= gate else 'FAIL: reduce scope or raise adoption first'}**", "",
          "## Sensitivity: net value by adoption (rows) and realization factor (columns)"]
    adopts, reals = c["sensitivity"]["adoption"], c["sensitivity"]["realization"]
    L += ["| Adoption \\ Realization | " + " | ".join(p(r) for r in reals) + " |", "|---|" + "---|" * len(reals)]
    rows = []
    for ad in adopts:
        vals = [run(c, ad, r)["net"] for r in reals]
        rows.append([ad] + vals)
        L.append(f"| {p(ad)} | " + " | ".join(m(v) for v in vals) + " |")
    (out / "roi_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    with open(out / "sensitivity.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["adoption"] + reals); w.writerows(rows)
    print(f"[ok] base ROI {p(sc['base']['roi'])}, break-even {p(be) if be else 'n/a'}, margin {margin * 100:.1f} pts -> {out / 'roi_report.md'}")


if __name__ == "__main__":
    main()
