#!/usr/bin/env python3
"""Outreach funnel analyzer for an AI-assisted social selling workflow.

Compares message variants (for example generic vs. AI-personalized) stage by stage:
sent -> accepted -> replied -> meeting, finds the weakest stage for each variant
and persona, and prints what to fix next. Pair it with SKILL.md, which drafts the
personalized messages under human review.

Usage: python funnel.py --log sample/outreach_log.csv
Standard library only. Sample log is synthetic.
"""
import argparse, csv
from collections import defaultdict

STAGES = ["accepted", "replied", "meeting"]

def funnel(rows):
    n = len(rows); c = {s: sum(int(r[s]) for r in rows) for s in STAGES}
    prev, steps = n, []
    for s in STAGES:
        steps.append((s, c[s], c[s] / prev if prev else 0)); prev = c[s]
    return n, steps

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--log", default="sample/outreach_log.csv"); a = ap.parse_args()
    rows = list(csv.DictReader(open(a.log, newline="", encoding="utf-8")))
    for key in ("variant", "persona"):
        groups = defaultdict(list)
        for r in rows: groups[r[key]].append(r)
        print(f"\n== Funnel by {key} ==")
        print(f"{key:28} {'sent':>5} {'accept%':>8} {'reply%':>7} {'meet%':>6} {'sent->meeting':>14}  weakest stage")
        for g, rs in sorted(groups.items()):
            n, steps = funnel(rs)
            weakest = min(steps, key=lambda x: x[2])
            print(f"{g:28} {n:>5} " + " ".join(f"{s[2] * 100:>7.0f}%" for s in steps) + f" {steps[-1][1] / n * 100:>13.1f}%  {weakest[0]}")
    v = defaultdict(list)
    for r in rows: v[r["variant"]].append(r)
    if {"generic", "ai_personalized"} <= set(v):
        g = sum(int(r["meeting"]) for r in v["generic"]) / len(v["generic"])
        p = sum(int(r["meeting"]) for r in v["ai_personalized"]) / len(v["ai_personalized"])
        print(f"\nAI-personalized vs generic: {p * 100:.1f}% vs {g * 100:.1f}% sent-to-meeting ({(p / g if g else 0):.1f}x).")
        print("Caveat: small sample; treat as directional and keep testing before scaling.")

if __name__ == "__main__":
    main()
