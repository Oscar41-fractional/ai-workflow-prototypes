#!/usr/bin/env python3
"""Steps 4-5 - Multi-channel funnel, A/B comparison and results for Clearmind Talent (fictional).

Reads the outreach records and answers four questions:
  1. Reach: how many contacts and companies did each channel touch?
  2. Funnel: conversations -> qualified calls -> meetings -> demos -> placement intents.
  3. What works: AI-personalized vs generic messages, and which persona and segment convert.
  4. Results: before vs after the AI-augmented program, and the placement pipeline value.

Usage: python funnel.py --data sample/
Standard library only. Records are synthetic; totals are calibrated to the results on my CV.
"""
import argparse, csv, json
from collections import defaultdict
from pathlib import Path


def load(data_dir):
    d = Path(data_dir)
    rd = lambda n: list(csv.DictReader(open(d / n, encoding="utf-8")))
    contacts = rd("contacts.csv")
    for c in contacts:
        for k in ("email_reply", "li_accepted", "li_conversation", "qualified_call", "meeting", "demos"):
            c[k] = int(c[k])
        c["conversation"] = int(bool(c["email_reply"] or c["li_conversation"] or c["met_at_event"]))
    return dict(contacts=contacts, accounts=rd("accounts.csv"), events=rd("events.csv"),
                placements=rd("placements.csv"), baseline=json.load(open(d / "baseline.json", encoding="utf-8")))


def reach(D):
    C = D["contacts"]
    return dict(email_contacts=sum(1 for c in C if c["email_variant"]),
                companies=len({c["account_id"] for c in C if c["email_variant"]}),
                linkedin_messaged=sum(1 for c in C if c["li_variant"]),
                linkedin_accepted=sum(c["li_accepted"] for c in C),
                linkedin_conversations=sum(c["li_conversation"] for c in C),
                email_replies=sum(c["email_reply"] for c in C),
                events=len(D["events"]), event_contacts=sum(1 for c in C if c["met_at_event"]))


def funnel(D):
    C = D["contacts"]
    conv = sum(c["conversation"] for c in C); qc = sum(c["qualified_call"] for c in C)
    mt = sum(c["meeting"] for c in C); dm = sum(c["demos"] for c in C)
    pi = len(D["placements"]); sg = sum(p["status"] == "Signed" for p in D["placements"])
    return [("Conversations (email reply, LinkedIn or event)", conv, None), ("Qualified calls", qc, qc / conv),
            ("Meetings", mt, mt / qc), ("Model-presentation demos", dm, None),
            ("Placement intents (candidates requested for review)", pi, None), ("Signed placement contracts", sg, None)]


def ab(D, channel):
    """AI-personalized vs generic, per channel."""
    C = D["contacts"]; out = {}
    for v in ("generic", "ai_personalized"):
        if channel == "linkedin":
            g = [c for c in C if c["li_variant"] == v]; conv = sum(c["li_conversation"] for c in g)
            out[v] = dict(sent=len(g), accepted=sum(c["li_accepted"] for c in g), conversations=conv,
                          qualified=sum(c["qualified_call"] for c in g if c["li_conversation"]))
        else:
            g = [c for c in C if c["email_variant"] == v]; rep = sum(c["email_reply"] for c in g)
            out[v] = dict(sent=len(g), replies=rep, qualified=sum(c["qualified_call"] for c in g if c["email_reply"]))
    return out


def breakdown(D, key):
    g = defaultdict(list)
    for c in D["contacts"]:
        g[c[key]].append(c)
    rows = []
    for k, cs in g.items():
        qc = sum(c["qualified_call"] for c in cs); mt = sum(c["meeting"] for c in cs)
        rows.append(dict(name=k, contacts=len(cs), conversations=sum(c["conversation"] for c in cs), qualified=qc,
                         meetings=mt, meeting_rate=mt / qc if qc else 0))
    return sorted(rows, key=lambda r: -r["meetings"])


def results(D):
    b, r = D["baseline"], reach(D); f = dict((n, v) for n, v, _ in funnel(D))
    after = dict(email_contacts=r["email_contacts"], events=r["events"], linkedin_conversations=r["linkedin_conversations"],
                 demos=f["Model-presentation demos"], placement_intents=len(D["placements"]))
    label = dict(email_contacts="Email campaign contacts", events="Events", linkedin_conversations="LinkedIn conversations",
                 demos="Model-presentation demos", placement_intents="Placement intents")
    return [(label[k], b[k], after[k], after[k] / b[k]) for k in label]


def pipeline(D):
    total = sum(int(p["value_6m"]) for p in D["placements"]); rate = D["baseline"]["reported_only"]["close_rate_forecast"]
    return dict(total=total, rate=rate, expected=total * rate, signed=sum(p["status"] == "Signed" for p in D["placements"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default="sample")
    D = load(ap.parse_args().data)
    r = reach(D)
    print(f"Reach: {r['email_contacts']:,} email contacts across {r['companies']} companies; "
          f"{r['linkedin_messaged']} LinkedIn messages -> {r['linkedin_conversations']} conversations; {r['events']} events")
    print("\nFunnel:")
    for n, v, rate in funnel(D):
        print(f"  {n:52} {v:>5}" + (f"   ({rate * 100:.1f}% of previous stage)" if rate else ""))
    for ch in ("linkedin", "email"):
        x = ab(D, ch); print(f"\n{ch.title()} A/B:")
        for v, m in x.items():
            base = m["conversations"] if ch == "linkedin" else m["replies"]
            print(f"  {v:16} sent {m['sent']:>4}  -> {base:>3} ({base / m['sent'] * 100:.1f}%)  -> {m['qualified']} qualified calls")
    print("\nBefore -> after:")
    for n, b, a, x in results(D):
        print(f"  {n:28} {b:>5} -> {a:>5}  ({x:.1f}x)")
    p = pipeline(D)
    print(f"\nPlacements: {len(D['placements'])} intents, {p['signed']} signed; 6-month value ${p['total']:,.0f}; "
          f"expected at {p['rate']:.0%} close rate ${p['expected']:,.0f}")


if __name__ == "__main__":
    main()
