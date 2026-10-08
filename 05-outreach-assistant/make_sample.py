#!/usr/bin/env python3
"""Generate the synthetic sample data for prototype 05 (Clearmind Talent (fictional) outreach).

Every company, contact and event here is fictional. The records are synthetic, but they are
calibrated so that the TOTALS match the results reported on my CV for the Clearmind Talent program
(Oct 2023 - Sep 2024). The script fails if any total drifts from those targets.

Usage: python make_sample.py        (writes sample/*.csv; same output every run)
Standard library only.
"""
import csv, json, random
from datetime import date, timedelta
from pathlib import Path

R = random.Random(2024)
OUT = Path(__file__).resolve().parent / "sample"

# ---------- targets (from the CV) ----------
T = dict(email_contacts=1150, companies=264, linkedin_conversations=119, qualified_calls=67,
         meetings=38, demos=46, events=9, placement_intents=3, signed=1, placement_value=340000)

# ---------- accounts ----------
PREFIX = ["Northvale", "Maplecrest", "Rivermark", "Stonebridge", "Bluepine", "Clearwater", "Granite Peak", "Harborview",
          "Ironleaf", "Lakeshore", "Lynxwood", "Oakridge", "Pinecrest", "Portage", "Redcedar", "Riverbend", "Silverbirch",
          "Snowline", "Summit Ridge", "Tamarack", "Timberline", "Trillium", "Whitecap", "Wolfden", "Borealis", "Laurentia",
          "Cartier Bay", "Champlain Ridge", "Kestrel", "Saguenay Peak", "Ashgrove", "Brightwater", "Frostgate"]
SEGMENTS = [("MSSP", 72, ["SecureOps", "Cyber Defense", "Threat Watch"]),
            ("MSP", 96, ["Managed IT", "Networks", "IT Partners"]),
            ("IT services", 56, ["IT Consulting", "Tech Services"]),
            ("Enterprise", 40, ["Insurance", "Logistics", "Financial Group"])]

accounts, used = [], set()
for seg, n, suffixes in SEGMENTS:
    k = 0
    while k < n:
        name = f"{R.choice(PREFIX)} {R.choice(suffixes)}"
        if name in used:
            continue
        used.add(name); k += 1
        accounts.append(dict(account_id=f"A{len(accounts) + 1:03d}", name=name, segment=seg))
# the worked example in the case study must exist
accounts[0]["name"] = "Laurentide SecureOps"

msp_ids = [a for a in accounts if a["segment"] == "MSP"]
tiers = ["A"] * 5 + ["B"] * 5 + ["C"] * 40
for a in accounts:
    a["source"] = "CRM tracker"; a["partner_tier"] = ""
for a, t in zip(R.sample(msp_ids, len(tiers)), tiers):
    a["source"] = "Partner tier list"; a["partner_tier"] = t
for a in accounts:
    a["region"] = "Ontario" if R.random() < 0.13 else "Quebec"
    base = {"MSSP": 0.55, "MSP": 0.3, "IT services": 0.25, "Enterprise": 0.2}[a["segment"]]
    a["open_n1_n2_roles"] = R.choice([1, 1, 2, 2, 3]) if R.random() < base else 0
ex = accounts[0]; ex.update(region="Quebec", open_n1_n2_roles=3)

# ---------- contacts (every account gets at least one) ----------
PERSONAS = [("Service Desk / SOC Director", 260), ("CTO / VP Technology", 230), ("CEO / Owner", 250),
            ("HR / Talent Acquisition", 260), ("People & Inclusion Lead", 150)]
plist = [p for p, n in PERSONAS for _ in range(n)]
R.shuffle(plist)
acc_for = [a["account_id"] for a in accounts] + [R.choice(accounts)["account_id"] for _ in range(T["email_contacts"] - len(accounts))]
R.shuffle(acc_for)
seg = {a["account_id"]: a["segment"] for a in accounts}
contacts = [dict(contact_id=f"C{i + 1:04d}", account_id=acc_for[i], persona=plist[i], segment=seg[acc_for[i]])
            for i in range(T["email_contacts"])]
for c in contacts:
    c.update(email_variant="", email_reply=0, li_variant="", li_accepted=0, li_conversation=0,
             met_at_event="", qualified_call=0, meeting=0, demos=0, first_touch="")

START = date(2023, 10, 2)
def day(lo, hi): return (START + timedelta(days=R.randint(lo, hi))).isoformat()

# email: wave 1 generic (Q4 2023), later waves AI-personalized
idx = list(range(len(contacts))); R.shuffle(idx)
for j, i in enumerate(idx):
    c = contacts[i]
    c["email_variant"] = "generic" if j < 400 else "ai_personalized"
    c["first_touch"] = day(0, 85) if j < 400 else day(95, 360)
for variant, n in (("generic", 8), ("ai_personalized", 50)):
    for c in R.sample([c for c in contacts if c["email_variant"] == variant], n):
        c["email_reply"] = 1

# LinkedIn: 330 contacts messaged, 110 generic / 220 AI-personalized
li = R.sample(contacts, 330)
for j, c in enumerate(li):
    c["li_variant"] = "generic" if j < 110 else "ai_personalized"
for variant, acc, conv in (("generic", 44, 18), ("ai_personalized", 140, 101)):
    pool = [c for c in li if c["li_variant"] == variant]
    a = R.sample(pool, acc)
    for c in a: c["li_accepted"] = 1
    for c in R.sample(a, conv): c["li_conversation"] = 1

# events: 9 events, 40 contacts met in person
EVENTS = [("2023-11-15", "Montreal cybersecurity conference (booth)", "Conference"),
          ("2024-01-30", "Webinar: Neurodiversity at work, turning challenges into opportunities", "Webinar (hosted)"),
          ("2024-02-21", "MSP peer group breakfast, Laval", "Networking"),
          ("2024-03-19", "Webinar: Recruiting strategies for neurodiversity", "Webinar (hosted)"),
          ("2024-04-17", "Quebec IT services association meetup", "Networking"),
          ("2024-05-08", "Diversity and inclusion in tech forum", "Panel"),
          ("2024-06-05", "Cybersecurity talent and workforce summit", "Conference"),
          ("2024-06-26", "Webinar: Cognitive diversity as a business advantage", "Webinar (hosted)"),
          ("2024-09-18", "MSSP partner day, Montreal", "Networking")]
met = R.sample([c for c in contacts if not c["li_conversation"] and not c["email_reply"]], 40)
for k, c in enumerate(met):
    c["met_at_event"] = EVENTS[k % 9][0]

# qualified calls 67 -> meetings 38 -> demos 46 (8 accounts got a second demo)
W = {"Service Desk / SOC Director": 3.0, "CTO / VP Technology": 1.8, "CEO / Owner": 1.4,
     "HR / Talent Acquisition": 1.0, "People & Inclusion Lead": 0.5}
SW = {"MSSP": 2.4, "MSP": 1.6, "IT services": 1.2, "Enterprise": 0.7}
def wpick(pool, n, boost=lambda c: 1.0):
    pool, out = list(pool), []
    for _ in range(n):
        ws = [W[c["persona"]] * SW[c["segment"]] * boost(c) for c in pool]
        c = R.choices(pool, ws)[0]; out.append(c); pool.remove(c)
    return out
qc = wpick([c for c in contacts if c["li_conversation"]], 38, lambda c: 1.6 if c["li_variant"] == "ai_personalized" else 1)
qc += wpick([c for c in contacts if c["email_reply"] and c not in qc], 17)
qc += wpick([c for c in contacts if c["met_at_event"] and c not in qc], 12)
for c in qc: c["qualified_call"] = 1
mt = wpick(qc, 38)
for c in mt: c["meeting"] = 1; c["demos"] = 1
for c in R.sample(mt, 8): c["demos"] = 2
# the worked example account has a meeting
exc = next(c for c in contacts if c["account_id"] == "A001")
if not exc["meeting"]:
    swap = next(c for c in mt if c["account_id"] != "A001")
    for f in ("qualified_call", "meeting", "demos", "li_variant", "li_accepted", "li_conversation", "email_reply", "met_at_event"):
        exc[f], swap[f] = swap[f], exc[f]
    exc["persona"] = "Service Desk / SOC Director"

# placements: 3 intents at meeting accounts, 1 signed; $340K combined 6-month value
meet_accts = sorted({c["account_id"] for c in contacts if c["meeting"]} - {"A001"})
pa = ["A001"] + R.sample(meet_accts, 2)
placements = [
    dict(account_id=pa[0], role="SOC Analyst Tier 1 (x2)", consultants=2, tenure_months=6, value_6m=150000, status="Signed"),
    dict(account_id=pa[1], role="Service Desk Analyst Tier 2", consultants=1, tenure_months=6, value_6m=100000, status="Candidates under review"),
    dict(account_id=pa[2], role="Cybersecurity Analyst Tier 1", consultants=1, tenure_months=6, value_6m=90000, status="Candidates under review")]

# ---------- checks ----------
got = dict(email_contacts=len(contacts), companies=len({c["account_id"] for c in contacts}),
           linkedin_conversations=sum(c["li_conversation"] for c in contacts),
           qualified_calls=sum(c["qualified_call"] for c in contacts), meetings=sum(c["meeting"] for c in contacts),
           demos=sum(c["demos"] for c in contacts), events=len(EVENTS), placement_intents=len(placements),
           signed=sum(p["status"] == "Signed" for p in placements), placement_value=sum(p["value_6m"] for p in placements))
assert got == T, {k: (got[k], T[k]) for k in T if got[k] != T[k]}

# ---------- write ----------
OUT.mkdir(exist_ok=True)
def write(name, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
write("accounts.csv", accounts)
write("contacts.csv", contacts)
write("events.csv", [dict(date=d, event=n, type=t, contacts_met=sum(c["met_at_event"] == d for c in contacts)) for d, n, t in EVENTS])
write("placements.csv", placements)
(OUT / "baseline.json").write_text(json.dumps({
    "_note": "Before the AI-augmented program. Figures implied by the multipliers reported on the CV.",
    "email_contacts": 230, "events": 3, "linkedin_conversations": 40, "demos": 10, "placement_intents": 1,
    "reported_only": {"pipeline_growth": "+40%", "linkedin_ssi": "Top 1%", "close_rate_forecast": 0.60}}, indent=2) + "\n")
print("[ok] sample data written; totals match CV:", got)
