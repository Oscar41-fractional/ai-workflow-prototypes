#!/usr/bin/env python3
"""Step 1 - Account prioritization for Clearmind Talent (fictional) outreach.

Scores every target account on how well it fits the Clearmind Cyber offer (placing trained,
neurodivergent Tier 1 / Tier 2 analysts at managed IT and security providers) and splits
the list into outreach waves, so the team spends its limited time on the best accounts first.

Fit score (maximum 9):
  segment          MSSP 3 · MSP 3 · IT services 2 · Enterprise 1
  open roles       open Tier 1/Tier 2 postings tracked, capped at 3
  partner tier     A 2 · B 1 · C 1 (MSPs from my former channel tier list) · none 0
  region           Quebec 1 (bilingual delivery, local onboarding support) · other 0
Waves: score 7+ = Wave 1 (personal outreach first), 5-6 = Wave 2, under 5 = Wave 3 (nurture).

Usage: python accounts.py --data sample/
Standard library only. All accounts are fictional.
"""
import argparse, csv
from collections import Counter
from pathlib import Path

SEG = {"MSSP": 3, "MSP": 3, "IT services": 2, "Enterprise": 1}
TIER = {"A": 2, "B": 1, "C": 1}


def score(a):
    parts = dict(segment=SEG[a["segment"]], open_roles=min(int(a["open_n1_n2_roles"]), 3),
                 partner_tier=TIER.get(a["partner_tier"], 0), region=1 if a["region"] == "Quebec" else 0)
    return sum(parts.values()), parts


def wave(s):
    return "Wave 1" if s >= 7 else "Wave 2" if s >= 5 else "Wave 3"


def prioritize(data_dir):
    rows = list(csv.DictReader(open(Path(data_dir) / "accounts.csv", encoding="utf-8")))
    for a in rows:
        a["score"], a["parts"] = score(a)
        a["wave"] = wave(a["score"])
    rows.sort(key=lambda a: (-a["score"], -int(a["open_n1_n2_roles"]), a["name"]))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default="sample")
    a = ap.parse_args()
    rows = prioritize(a.data)
    print("Accounts by wave:", dict(sorted(Counter(r["wave"] for r in rows).items())))
    print(f"\n{'Account':30} {'Segment':12} {'Tier':5} {'Roles':>5} {'Score':>6}  Wave")
    for r in rows[:12]:
        print(f"{r['name']:30} {r['segment']:12} {r['partner_tier'] or '-':5} {r['open_n1_n2_roles']:>5} {r['score']:>6}  {r['wave']}")


if __name__ == "__main__":
    main()
