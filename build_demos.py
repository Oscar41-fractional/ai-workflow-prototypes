#!/usr/bin/env python3
"""Build the "See the output" pages in docs/ from the prototypes' real output.

Runs each prototype on its fictional sample data and wraps the result in a styled
HTML page. Nothing in the output is edited by hand: change the data or the script,
run this again, and the pages update.

Usage: python build_demos.py
Standard library only.
"""
import csv, html, json, re, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
GH = "https://github.com/Oscar41-fractional/ai-workflow-prototypes/blob/main/"
e = html.escape


# ---------- tiny markdown -> html (enough for the reports these scripts write) ----------
def inline(t):
    t = e(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w])_(.+?)_(?![\w])", r"<i>\1</i>", t)
    return t


def md(src):
    out, lines, i = [], src.splitlines(), 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"): j += 1
            out.append("<pre>" + e("\n".join(lines[i + 1:j])) + "</pre>"); i = j + 1; continue
        m = re.match(r"(#{1,4}) (.*)", l)
        if m:
            n = len(m.group(1)) + 1
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>"); i += 1; continue
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            head, body = rows[0], [r for r in rows[1:] if not set("".join(r)) <= set("-: ")]
            t = "<div class='tw'><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            for r in body:
                t += "<tr>" + "".join(f"<td{' class=neg' if c.startswith('-$') or c.startswith('-') and c.endswith('%') else ''}>{inline(c)}</td>" for c in r) + "</tr>"
            out.append(t + "</tbody></table></div>"); continue
        if l.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(f"<li>{inline(lines[i][2:])}</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>"); continue
        if l.strip():
            out.append(f"<p>{inline(l)}</p>")
        i += 1
    return "\n".join(out)


def run(cmd, cwd):
    r = subprocess.run([sys.executable] + cmd, cwd=ROOT / cwd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"{cwd}: {r.stderr}")
    return r.stdout


# ---------- page shell ----------
CSS = """
:root{--ink:#121212;--coal:#1c1b1b;--smoke:#8d8a88;--bone:#ecebe7;--paper:#f7f6f3;--red:#f01e2c;--deep:#b5121d;--ok:#1d7a4a;--warn:#9a6200}
*{box-sizing:border-box}body{margin:0;font-family:"IBM Plex Sans",system-ui,sans-serif;background:var(--paper);color:var(--ink);line-height:1.55}
a{color:var(--deep)}.w{max-width:1100px;margin:auto;padding-inline:20px}
header{background:var(--ink);color:var(--bone);padding-block:40px 34px}
.eb{font-family:"IBM Plex Mono",monospace;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--red)}
h1,h2,h3,h4{font-family:"IBM Plex Sans Condensed",sans-serif;line-height:1.15}
header h1{font-size:clamp(30px,5vw,46px);margin:8px 0 0}.rule{height:4px;width:80px;background:var(--red);margin:16px 0}
header p{max-width:68ch;color:#c9c6c2;margin:0}header p.rl{margin-top:10px;font-size:14px;color:#bdbab6}header p.rl b{color:#fff}
.nav{margin-top:18px;display:flex;flex-wrap:wrap;gap:8px}.nav a{color:var(--bone);border:1px solid #444;padding:7px 12px;border-radius:5px;text-decoration:none;font-size:14px}.nav a:hover{border-color:var(--red)}
.how{background:var(--coal);color:var(--bone);padding-block:18px}.how .w{display:flex;flex-wrap:wrap;gap:10px;align-items:center;font-size:14px}
.how .st{border:1px solid #444;border-radius:5px;padding:6px 10px}.how .st i{font-style:normal;color:var(--red);font-family:"IBM Plex Mono",monospace;font-size:12px;margin-right:6px}
.how .ar{color:var(--smoke)}
main{padding-block:28px 40px}.lead{max-width:75ch;color:#444;margin:0 0 18px}
.doc{background:#fff;border:1px solid #ddd;border-radius:8px;padding:24px 28px;box-shadow:0 1px 3px rgba(0,0,0,.05)}
.doc h2{font-size:26px;margin:0 0 6px}.doc h3{font-size:20px;margin:22px 0 8px;border-bottom:2px solid var(--bone);padding-bottom:4px}.doc h4{font-size:17px;margin:18px 0 6px}
.doc p{margin:6px 0}.doc ul{margin:6px 0;padding-left:20px}.doc li{margin:3px 0}
.doc pre{background:var(--ink);color:var(--bone);padding:12px 14px;border-radius:6px;overflow-x:auto;font-size:13px;line-height:1.45}
code{font-family:"IBM Plex Mono",monospace;font-size:.9em;background:var(--bone);padding:1px 5px;border-radius:3px}
.tw{overflow-x:auto;border:1px solid #e3e1dc;border-radius:6px;margin:8px 0}table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #eee;vertical-align:top}th{background:var(--ink);color:#fff;font-weight:600;white-space:nowrap}
tr:nth-child(even) td{background:var(--paper)}td.neg{color:var(--deep);font-weight:600}td.pos{color:var(--ok);font-weight:600}
.tabs{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}.tabs button{font:inherit;font-size:14px;border:1px solid #ccc;background:#fff;padding:7px 14px;border-radius:99px;cursor:pointer}
.tabs button[aria-selected=true]{background:var(--ink);color:#fff;border-color:var(--ink)}
.note{font-size:13px;color:#666;margin-top:14px}
.badge{display:inline-block;font-size:12px;font-weight:700;color:#fff;padding:3px 10px;border-radius:99px;letter-spacing:.04em}
.pass{background:var(--ok)}.fail{background:var(--deep)}.amber{background:var(--warn)}.grey{background:#6b6764}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-bottom:22px}
.kpi{background:#fff;border:1px solid #ddd;border-radius:8px;padding:18px}.kpi h3{margin:0 0 4px;font-size:20px}
.kpi .big{font-family:"IBM Plex Sans Condensed",sans-serif;font-size:40px;font-weight:700;line-height:1}
.kpi dl{display:grid;grid-template-columns:auto auto;gap:4px 14px;margin:12px 0 0;font-size:14px}.kpi dt{color:#666}.kpi dd{margin:0;font-weight:600;text-align:right}
.bar{height:12px;background:var(--bone);border-radius:6px;overflow:hidden}.bar span{display:block;height:100%;background:var(--deep)}
.msg{background:var(--paper);border-left:3px solid var(--red);padding:10px 14px;margin:8px 0;white-space:pre-line}
.msg small{display:block;font-family:"IBM Plex Mono",monospace;color:var(--deep);font-size:12px;margin-bottom:4px;white-space:normal}
.grid4{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:12px 0 16px}.kl{font-size:13px;color:#666;display:block;margin-top:6px}
.frow{display:flex;align-items:center;gap:10px;margin:6px 0;font-size:14px}.fl{width:330px;flex:none}.fv{width:40px;text-align:right}.fr{width:150px;color:#666;font-size:12.5px}
@media(max-width:700px){.fl{width:140px;font-size:12.5px}.fr{display:none}}
.hint{font-size:14px;color:#444;margin:8px 0}
[hidden]{display:none!important}
footer{padding-block:24px;color:var(--smoke);font-size:13px;border-top:1px solid #e3e1dc}
"""
TABS_JS = """<script>document.querySelectorAll('.tabs').forEach(function(t){var b=t.querySelectorAll('button');b.forEach(function(x){x.onclick=function(){b.forEach(function(y){y.setAttribute('aria-selected',y===x);document.getElementById(y.dataset.t).hidden=y!==x})}})});</script>"""


ROLES = {"01": "Partner / Channel Managers · Alliances · Partner Marketing", "02": "Sales · Marketing · Business Development · Partner Development",
         "03": "Sales and Marketing leaders · Partner Development · Revenue Operations", "05": "Sales · Marketing · Demand generation · Business Development"}


def page(fname, num, title, intro, folder, steps, cmd, body, code_file, data_file, extra="", gloss=""):
    nav = (f'<a href="index.html">← All prototypes</a><a href="{GH}{folder}/{code_file}">View the code</a>'
           f'<a href="{GH}{folder}/{data_file}">Sample data</a><a href="{GH}{folder}/README.md#solution-path">Solution path</a>'
           f'<a href="{GH}{folder}/README.md#design-choices">Design choices</a>')
    how = '<span class="ar">→</span>'.join(f'<span class="st"><i>{e(w)}</i>{e(t)}</span>' for w, t in steps)
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · Sample output</title><meta name="description" content="{e(intro)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans+Condensed:wght@600;700&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<header><div class="w"><div class="eb">Prototype {num} · Sample output</div><h1>{e(title)}</h1><div class="rule"></div>
<p>{e(intro)}</p><p class="rl">For roles: <b>{e(ROLES.get(num, ""))}</b></p><div class="nav">{nav}</div></div></header>
<div class="how"><div class="w">{how}</div></div>
<main><div class="w">{body}
<p class="note">Produced by running <code>{e(cmd)}</code> on fictional sample data. The output is shown as generated, not edited by hand.{extra}</p>{f'<p class="note"><b>Acronyms:</b> {e(gloss)}</p>' if gloss else ''}</div></main>
<footer><div class="w">All company names and data are fictional. © 2026 Oscar Farrera · All rights reserved.</div></footer>{TABS_JS}</body></html>"""
    (DOCS / fname).write_text(doc, encoding="utf-8")
    print(f"[ok] docs/{fname}")


def tabs(prefix, items):
    btn = "".join(f'<button data-t="{prefix}{i}" aria-selected="{str(i == 0).lower()}">{e(lbl)}</button>' for i, (lbl, _) in enumerate(items))
    pan = "".join(f'<div id="{prefix}{i}" class="doc"{" hidden" if i else ""}>{h}</div>' for i, (_, h) in enumerate(items))
    return f'<div class="tabs" role="tablist">{btn}</div>{pan}'


def main():
    tmp = Path(tempfile.mkdtemp())

    # 01 MBR Assistant
    run(["mbr.py", "--data", "sample/partner_activity_2026-05.csv", "--out", str(tmp / "mbr")], "01-mbr-assistant")
    reports = sorted((tmp / "mbr").glob("*_mbr.md"))
    items = [(re.search(r"Monthly business review: (.+?) \(", f.read_text()).group(1), md(f.read_text())) for f in reports]
    body = '<p class="lead">One raw activity file for three fictional partners goes in. A draft monthly business review for each partner comes out, with the numbers calculated by the script, not by the AI. Pick a partner:</p>' + tabs("p", items)
    page("demo-01-mbr.html", "01", "MBR Assistant", "Raw partner activity data turned into a one-page monthly business review per partner, ready for a human to check and share.",
         "01-mbr-assistant", [("Input", "Partner activity CSV"), ("Script", "Clean, calculate, rank"), ("AI or template", "Draft the story"), ("Human", "Review and share")],
         "python mbr.py --data sample/partner_activity_2026-05.csv", body, "mbr.py", "sample/partner_activity_2026-05.csv",
         gloss="MBR = monthly business review; JMP = joint marketing plan; MDF = market development funds (money a vendor gives partners for joint marketing); "
               "KPI = key performance indicator; SI = systems integrator; CSV = spreadsheet file in comma-separated format.")

    # 02 AI Transformation Request Portfolio
    run(["prioritize.py", "--intake", "sample/intake.csv", "--out", str(tmp / "portfolio.md")], "02-ai-request-portfolio")
    h = md((tmp / "portfolio.md").read_text())
    pill = {"Prioritize": "pass", "Invest &amp; schedule": "amber", "Pilot with caution": "grey", "Decline for now": "fail"}
    for q, c in pill.items(): h = h.replace(f"<td>{q}</td>", f'<td><span class="badge {c}">{q}</span></td>')
    h = h.replace("Forbidden: excluded before scoring", '<span class="badge fail">Forbidden</span> excluded before scoring')
    n = list(csv.DictReader(open(ROOT / "02-ai-request-portfolio/sample/intake.csv", encoding="utf-8")))
    body = (f'<p class="lead">{len(n)} free-text AI requests from the Sales, Marketing, Business Development and Partner Development teams of a fictional company go in. A ranked portfolio comes out, '
            'with the same gates applied to every request, a decision for each, and a short brief a leader can approve.</p>'
            f'<div class="doc">{h}</div>')
    page("demo-02-intake.html", "02", "AI Transformation Request Portfolio", "Every AI request from Sales, Marketing, Business Development and Partner Development scored the same way, ranked, and turned into a decision brief.",
         "02-ai-request-portfolio", [("AI skill", "Request → intake row"), ("Human", "Confirm scores"), ("Script", "Gate, score, rank"), ("Human", "Approve portfolio")],
         "python prioritize.py --intake sample/intake.csv", body, "prioritize.py", "sample/intake.csv",
         gloss="KPI = key performance indicator; KB = knowledge base; NDA = non-disclosure agreement; MSA = master services agreement; "
               "HR = human resources; CS = customer success; P&L = profit and loss statement.")

    # 03 ROI metric tree
    cards, items = [], []
    for cfg, lbl in [("assumptions.json", "Broad rollout"), ("assumptions_power_users.json", "Focused: power users")]:
        out = tmp / cfg
        msg = run(["roi_model.py", "--config", cfg, "--out", str(out)], "03-roi-metric-tree")
        c = json.load(open(ROOT / "03-roi-metric-tree" / cfg, encoding="utf-8"))
        roi, be, mg = re.search(r"base ROI (-?[\d.]+)%, break-even ([\d.]+)%, margin (-?[\d.]+) pts", msg).groups()
        ok = float(mg) >= c["gate_margin_points"]
        cards.append(f'<div class="kpi"><span class="badge {"pass" if ok else "fail"}">{"PASS" if ok else "FAIL"}</span><h3 style="margin-top:8px">{lbl}: {c["seats"]} seats</h3>'
                     f'<div class="big" style="color:var({"--ok" if ok else "--deep"})">{float(roi):+.1f}%</div><span style="font-size:13px;color:#666">base-case ROI</span>'
                     f'<dl><dt>Break-even adoption</dt><dd>{be}%</dd><dt>Base-case adoption</dt><dd>{c["scenarios"]["base"]["adoption"] * 100:.0f}%</dd>'
                     f'<dt>Safety margin</dt><dd>{float(mg):+.1f} pts</dd><dt>Gate rule</dt><dd>≥ {c["gate_margin_points"]} pts</dd></dl></div>')
        items.append((f"Full report: {lbl.lower()}", md((out / "roi_report.md").read_text())))
    body = ('<p class="lead">Same model, two questions. Rolling an AI assistant out to all 80 staff fails the decision gate. '
            'Focusing on the 30 people with the most repetitive work passes it with room to spare. Open either full report for the metric tree, scenarios and sensitivity grid.</p>'
            f'<div class="grid2">{"".join(cards)}</div>' + tabs("r", items))
    page("demo-03-roi.html", "03", "ROI metric tree", "An AI investment case built from one assumptions file: metric tree, three scenarios, break-even adoption and a pass/fail gate.",
         "03-roi-metric-tree", [("Human", "Set assumptions"), ("Script", "Model scenarios"), ("Script", "Apply 15-pt gate"), ("Human", "Go, rescope or stop")],
         "python roi_model.py --config assumptions.json", body, "roi_model.py", "assumptions.json",
         gloss="ROI = return on investment; P&L = profit and loss statement; h = hours.")

    # 05 Outreach Assistant (Clearmind Talent (fictional))
    sys.path.insert(0, str(ROOT / "05-outreach-assistant")); import funnel, accounts as acc
    run(["make_sample.py"], "05-outreach-assistant")
    sd = ROOT / "05-outreach-assistant" / "sample"
    D = funnel.load(sd); A = acc.prioritize(sd); R5 = funnel.reach(D)
    names = {a["account_id"]: a["name"] for a in A}
    pct = lambda x: f"{x * 100:.1f}%"
    def tbl(head, rows):
        return ("<div class='tw'><table><thead><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
                + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
    def kpis(items):
        return '<div class="grid4">' + "".join(f'<div class="kpi"><div class="big">{v}</div><span class="kl">{l}</span></div>' for v, l in items) + "</div>"

    s1 = ("<h3>Step 1 · The company, the problem and the offer</h3>"
          "<p><b>Clearmind Talent</b> (fictional name) stands for the Montreal-area talent-placement firm I worked for: it places neurodivergent professionals with employers "
          "in technology and business roles. Consultants are placed with client companies and billed at a rate similar to a full-time employee. "
          "Its <b>Clearmind Cyber</b> offer focuses on cybersecurity: many highly qualified neurodivergent people have strengths that match security work "
          "(attention to detail, pattern recognition, persistence with complex systems).</p>"
          "<p><b>The problem to solve:</b> managed service providers (MSPs) and managed security service providers (MSSPs) in Quebec cannot fill Tier 1 "
          "and Tier 2 analyst roles. The market is tight, salaries are rising, and sales keep bringing in new clients the team must serve. "
          "The typical buyer is the <b>service desk or SOC director</b>, under pressure from leadership to deliver. On the other side, Clearmind Talent had a small "
          "team and a lean marketing budget, so it had to reach hundreds of employers without adding people.</p>"
          + tbl(["What Clearmind Talent offers", "How it works"], [
              ["<b>Placed consultants</b>", "Trained neurodivergent analysts placed with the client, billed at a rate similar to an employee; no recruiting fee"],
              ["<b>Training roadmap</b>", "Four certification blocks matched to the roles employers post (below), so candidates arrive job-ready"],
              ["<b>Onboarding and support</b>", "Clearmind Talent coaches both the consultant and the team during onboarding and throughout the placement"],
              ["<b>Content and events</b>", "Webinars, campaigns and talks that help employers understand and adapt to neurodivergent talent"]])
          + "<h4>Cybersecurity training roadmap (candidates)</h4>"
          + tbl(["Block", "Target roles", "Example certifications"], [
              ["1. Cybersecurity fundamentals", "Help desk, Tier 1 IT support, IT specialist", "CompTIA A+, ISC2 Certified in Cybersecurity, Google Cybersecurity Certificate"],
              ["2. Core domains", "Tier 2 IT support, network security analyst, cloud security", "CompTIA Network+, Security+, Cloud+; ISC2 SSCP"],
              ["3. Penetration testing", "Ethical hacker, pen tester, threat analyst", "EC-Council Ethical Hacking Essentials, CompTIA PenTest+, CEH"],
              ["4. Security operations center", "SOC analyst Tier 1 and 2, incident handler", "EC-Council Certified SOC Analyst, Incident Handler, Threat Intelligence Analyst"]]))

    W = {}
    for a in A: W[a["wave"]] = W.get(a["wave"], 0) + 1
    top = [[f"<b>{e(a['name'])}</b>", a["segment"], a["partner_tier"] or "-", a["open_n1_n2_roles"],
            f"{a['parts']['segment']} + {a['parts']['open_roles']} + {a['parts']['partner_tier']} + {a['parts']['region']} = <b>{a['score']}</b>",
            f'<span class="badge {"pass" if a["wave"] == "Wave 1" else "amber"}">{a["wave"]}</span>'] for a in A[:10]]
    s2 = ("<h3>Step 2 · Prioritize the accounts (script)</h3>"
          f"<p>The target list combined the prospect tracker (MSPs, MSSPs, IT services firms and enterprises with in-house security teams) and the MSP "
          f"segment from my former channel partner tier list. <code>accounts.py</code> scores all {len(A)} accounts out of 9 and splits them into waves, "
          "so personal outreach goes to the best fit first.</p>"
          + kpis([(W.get("Wave 1", 0), "Wave 1: personal outreach (score 7-9)"), (W.get("Wave 2", 0), "Wave 2: AI-personalized sequences (5-6)"),
                  (W.get("Wave 3", 0), "Wave 3: newsletter and events (under 5)")])
          + "<p class='hint'><b>Score</b> = segment (MSSP or MSP 3, IT services 2, enterprise 1) + open Tier 1/Tier 2 roles tracked (up to 3) "
            "+ partner tier (A 2, B or C 1) + Quebec 1. Top 10:</p>"
          + tbl(["Account (fictional)", "Segment", "Tier", "Open roles", "Score", "Wave"], top))

    s3 = """<h3>Step 3 · What the skill drafts (illustrative)</h3>
<p>Inputs given to the skill: <b>Laurentide SecureOps</b> (fictional MSSP in Laval, Wave 1); contact <b>Marc</b>, Director, Service Desk and SOC;
public signals: <i>two "SOC Analyst, Tier 1" postings open for seven weeks, and a LinkedIn post about onboarding new managed detection clients</i>;
ask: review two candidate profiles. Messages were sent in French; shown here in English.</p>
<div class="msg"><small>Connection note · under 300 characters</small>Hi Marc, I saw Laurentide is hiring two Tier 1 SOC analysts while onboarding new clients. At Clearmind Talent we place trained, certified analysts, and we support them through onboarding. Happy to connect.</div>
<div class="msg"><small>Follow-up · under 80 words</small>Thanks for connecting, Marc. Two open Tier 1 roles during client onboarding usually means your senior analysts cover the queue. Our Clearmind Cyber consultants hold Security+ or equivalent certifications, are billed like an employee with no recruiting fee, and we coach them and your team through the first months. Would you like to review two anonymized candidate profiles this week?</div>
<div class="msg"><small>Email · under 120 words</small><b>Subject: Two Tier 1 SOC analysts for Laurentide</b>
Hi Marc,
I noticed your two Tier 1 SOC analyst postings have been open for several weeks, while Laurentide adds new managed detection clients.
Clearmind Talent places neurodivergent analysts who are trained and certified for SOC work: strong attention to detail, consistency with repetitive triage, and persistence with complex alerts. They join as consultants billed at a rate similar to an employee, and we support both them and your team through onboarding.
Could I send you two anonymized candidate profiles to review?
Best regards,
Oscar Farrera, Clearmind Talent</div>
<div class="msg"><small>Self-check flags for the human</small>Verify the postings are still open · no candidate diagnosis or personal details · certifications must match the actual profiles · one ask only · CASL footer on the email · a human sends it</div>"""

    ev = [[x["date"], e(x["event"]), x["type"], x["contacts_met"]] for x in D["events"]]
    s4 = ("<h3>Step 4 · Engage: events and content (human + AI)</h3>"
          f"<p>Events grew from 3 to {len(D['events'])}, mixing conferences, MSP networking and webinars Clearmind Talent hosted. AI helped draft the content plan: "
          "10 webinar topics by audience, 10 social campaigns and 3 video scripts, each reviewed and adapted by the team.</p>"
          + tbl(["Date", "Event (generic names)", "Type", "Contacts met"], ev)
          + "<p class='hint'><b>Content examples:</b> webinar <i>Neurodiversity at work: turning challenges into opportunities</i> (HR and team leads); "
            "webinar <i>Recruiting strategies for neurodiversity</i> (talent acquisition); campaign <i>Myths and realities of neurodiversity</i>; "
            "video script <i>Neurodiversity: an asset for business</i>.</p>")

    F = funnel.funnel(D); mx = F[0][1]
    fun = "".join(f"<div class='frow'><span class='fl'>{e(n)}</span><div class='bar' style='flex:1'><span style='width:{max(v / mx, .02) * 100:.0f}%'></span></div>"
                  f"<b class='fv'>{v}</b><span class='fr'>{pct(r) + ' of previous' if r else ''}</span></div>" for n, v, r in F)
    L, M = funnel.ab(D, "linkedin"), funnel.ab(D, "email")
    abrows = [["LinkedIn", "Generic", L["generic"]["sent"], f"{L['generic']['conversations']} ({pct(L['generic']['conversations'] / L['generic']['sent'])})", L["generic"]["qualified"]],
              ["LinkedIn", "<b>AI-personalized</b>", L["ai_personalized"]["sent"], f"<b>{L['ai_personalized']['conversations']} ({pct(L['ai_personalized']['conversations'] / L['ai_personalized']['sent'])})</b>", L["ai_personalized"]["qualified"]],
              ["Email", "Generic (wave 1)", M["generic"]["sent"], f"{M['generic']['replies']} ({pct(M['generic']['replies'] / M['generic']['sent'])})", M["generic"]["qualified"]],
              ["Email", "<b>AI-personalized</b>", M["ai_personalized"]["sent"], f"<b>{M['ai_personalized']['replies']} ({pct(M['ai_personalized']['replies'] / M['ai_personalized']['sent'])})</b>", M["ai_personalized"]["qualified"]]]
    brk = lambda k: tbl([k.title(), "Contacts", "Conversations", "Qualified calls", "Meetings", "Meeting rate"],
                        [[f"<b>{e(r['name'])}</b>", r["contacts"], r["conversations"], r["qualified"], r["meetings"], pct(r["meeting_rate"])] for r in funnel.breakdown(D, k)])
    s5 = ("<h3>Step 5 · Measure: funnel and what works (script)</h3>"
          + kpis([(f"{R5['email_contacts']:,}", f"email contacts across {R5['companies']} companies"), (R5["linkedin_conversations"], "LinkedIn conversations"),
                  (f"{F[2][1]} / {F[1][1]}", f"meetings from qualified calls ({pct(F[2][1] / F[1][1])})")])
          + f"<div class='funnel'>{fun}</div><p class='hint'>Demos can exceed meetings: 8 accounts asked for a second model presentation to other stakeholders.</p>"
          + "<h4>AI-personalized vs generic</h4>" + tbl(["Channel", "Variant", "Sent", "Conversations / replies", "Qualified calls"], abrows)
          + "<h4>By persona</h4>" + brk("persona") + "<h4>By segment</h4>" + brk("segment")
          + "<p><b>Read-out:</b> AI-personalized LinkedIn messages started conversations about 2.8 times as often as generic ones. The service desk / SOC director "
            "converts best, confirming the buyer described in the business plan, and MSSPs and MSPs book far more meetings than enterprises. "
            "So the program shifted effort to Wave 1 MSSPs and MSPs, and invited HR and inclusion contacts to webinars instead of asking them for meetings.</p>")

    P = funnel.pipeline(D)
    rr = [[f"<b>{n}</b>", f"{b:,}", f"<b>{a:,}</b>", f"{x:.1f}x"] for n, b, a, x in funnel.results(D)]
    rr += [["<b>Lead-to-meeting conversion</b>", "-", f"<b>{pct(F[2][1] / F[1][1])}</b> ({F[2][1]} of {F[1][1]} qualified calls)", "-"],
           ["<b>Overall pipeline</b>", "-", "<b>+40%</b> (reported)", "-"], ["<b>LinkedIn Social Selling Index</b>", "-", "<b>Top 1%</b> (reported)", "-"]]
    pl = [[f"<b>{e(names[p['account_id']])}</b>", e(p["role"]), p["tenure_months"] + " months", f"${int(p['value_6m']):,}",
           f'<span class="badge {"pass" if p["status"] == "Signed" else "amber"}">{e(p["status"])}</span>'] for p in D["placements"]]
    s6 = ("<h3>Step 6 · Results: before vs after</h3>"
          + tbl(["Measure", "Before", "After", "Change"], rr)
          + "<h4>Placement pipeline</h4>"
          + kpis([(len(D["placements"]), "placement intents (vs 1 at baseline)"), (P["signed"], "signed contract"),
                  (f"${P['total'] / 1000:,.0f}K", f"6-month value; ${P['expected'] / 1000:,.0f}K expected at {P['rate']:.0%} close rate")])
          + tbl(["Account (fictional)", "Role", "Tenure", "6-month value", "Status"], pl)
          + "<p class='hint'>A placement intent means the prospect asked to review candidates for a defined role. The split of the $340K across the three "
            "intents is illustrative; the total, the signed contract and the 60% forecast are as reported.</p>")

    body = ('<p class="lead">A real program, rebuilt with fictional names: how a neurodiversity talent-placement firm (shown as Clearmind Talent, a fictional name) used AI-augmented outreach to reach hundreds of MSP, MSSP and IT '
            'employers with a small team, and turn conversations into placements. The records are synthetic, but their totals match the results on my CV.</p>'
            f'<div class="doc">{s1}{s2}{s3}{s4}{s5}{s6}</div>')
    page("demo-05-outreach.html", "05", "Outreach Assistant", "AI-augmented outreach for a neurodiversity talent-placement firm: prioritized accounts, AI-drafted messages sent by a human, and every stage measured.",
         "05-outreach-assistant", [("Script", "Prioritize accounts"), ("Human", "Pick contact + signal"), ("AI skill", "Draft 3 variants"),
                                  ("Human", "Send, engage, demo"), ("Script", "Measure the funnel")],
         "python accounts.py --data sample/ and python funnel.py --data sample/", body, "funnel.py", "sample/contacts.csv",
         " Company and contact names, the Step 3 messages and the event names are illustrative.",
         gloss="MSP = managed service provider; MSSP = managed security service provider; SOC = security operations center; "
               "SSI = LinkedIn Social Selling Index; CASL = Canada's Anti-Spam Legislation; CEH = Certified Ethical Hacker; "
               "ISC2 SSCP = Systems Security Certified Practitioner; K = thousand.")


if __name__ == "__main__":
    main()
