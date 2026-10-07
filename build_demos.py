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
header p{max-width:68ch;color:#c9c6c2;margin:0}
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
[hidden]{display:none!important}
footer{padding-block:24px;color:var(--smoke);font-size:13px;border-top:1px solid #e3e1dc}
"""
TABS_JS = """<script>document.querySelectorAll('.tabs').forEach(function(t){var b=t.querySelectorAll('button');b.forEach(function(x){x.onclick=function(){b.forEach(function(y){y.setAttribute('aria-selected',y===x);document.getElementById(y.dataset.t).hidden=y!==x})}})});</script>"""


def page(fname, num, title, intro, folder, steps, cmd, body, code_file, data_file, extra=""):
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
<p>{e(intro)}</p><div class="nav">{nav}</div></div></header>
<div class="how"><div class="w">{how}</div></div>
<main><div class="w">{body}
<p class="note">Produced by running <code>{e(cmd)}</code> on fictional sample data. The output is shown as generated, not edited by hand.{extra}</p></div></main>
<footer><div class="w">All company names and data are fictional. © 2026 Oscar Farrera · MIT License.</div></footer>{TABS_JS}</body></html>"""
    (DOCS / fname).write_text(doc, encoding="utf-8")
    print(f"[ok] docs/{fname}")


def tabs(prefix, items):
    btn = "".join(f'<button data-t="{prefix}{i}" aria-selected="{str(i == 0).lower()}">{e(lbl)}</button>' for i, (lbl, _) in enumerate(items))
    pan = "".join(f'<div id="{prefix}{i}" class="doc"{" hidden" if i else ""}>{h}</div>' for i, (_, h) in enumerate(items))
    return f'<div class="tabs" role="tablist">{btn}</div>{pan}'


def main():
    tmp = Path(tempfile.mkdtemp())

    # 01 MBR Copilot
    run(["mbr.py", "--data", "sample/partner_activity_2026-05.csv", "--out", str(tmp / "mbr")], "01-mbr-copilot")
    reports = sorted((tmp / "mbr").glob("*_mbr.md"))
    items = [(re.search(r"Monthly business review: (.+?) \(", f.read_text()).group(1), md(f.read_text())) for f in reports]
    body = '<p class="lead">One raw activity file for three fictional partners goes in. A draft monthly business review for each partner comes out, with the numbers calculated by the script, not by the AI. Pick a partner:</p>' + tabs("p", items)
    page("demo-01-mbr.html", "01", "MBR Copilot", "Raw partner activity data turned into a one-page monthly business review per partner, ready for a human to check and share.",
         "01-mbr-copilot", [("Input", "Partner activity CSV"), ("Script", "Clean, calculate, rank"), ("AI or template", "Draft the story"), ("Human", "Review and share")],
         "python mbr.py --data sample/partner_activity_2026-05.csv", body, "mbr.py", "sample/partner_activity_2026-05.csv")

    # 02 Intake prioritizer
    run(["prioritize.py", "--intake", "sample/intake.csv", "--out", str(tmp / "portfolio.md")], "02-intake-prioritizer")
    h = md((tmp / "portfolio.md").read_text())
    pill = {"Prioritize": "pass", "Invest &amp; schedule": "amber", "Pilot with caution": "grey", "Decline for now": "fail"}
    for q, c in pill.items(): h = h.replace(f"<td>{q}</td>", f'<td><span class="badge {c}">{q}</span></td>')
    h = h.replace("Forbidden: excluded before scoring", '<span class="badge fail">Forbidden</span> excluded before scoring')
    n = list(csv.DictReader(open(ROOT / "02-intake-prioritizer/sample/intake.csv", encoding="utf-8")))
    body = (f'<p class="lead">{len(n)} free-text AI requests from different teams of a fictional company go in. A ranked portfolio comes out, '
            'with the same gates applied to every request, a decision for each, and a short brief a leader can approve.</p>'
            f'<div class="doc">{h}</div>')
    page("demo-02-intake.html", "02", "Transformation intake prioritizer", "Every AI request scored the same way, ranked, and turned into a decision brief, so the ranking does not depend on who asked.",
         "02-intake-prioritizer", [("AI skill", "Request → intake row"), ("Human", "Confirm scores"), ("Script", "Gate, score, rank"), ("Human", "Approve portfolio")],
         "python prioritize.py --intake sample/intake.csv", body, "prioritize.py", "sample/intake.csv")

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
         "python roi_model.py --config assumptions.json", body, "roi_model.py", "assumptions.json")

    # 05 Outreach copilot
    sys.path.insert(0, str(ROOT / "05-outreach-copilot")); import funnel
    rows = list(csv.DictReader(open(ROOT / "05-outreach-copilot/sample/outreach_log.csv", encoding="utf-8")))
    def table(key):
        g = {}
        for r in rows: g.setdefault(r[key], []).append(r)
        t = f"<div class='tw'><table><thead><tr><th>{key.title()}</th><th>Sent</th><th>Accepted</th><th>Replied</th><th>Meeting</th><th>Sent → meeting</th><th>Weakest stage</th></tr></thead><tbody>"
        for k, rs in sorted(g.items()):
            nn, steps = funnel.funnel(rs); weak = min(steps, key=lambda x: x[2])[0]
            rate = steps[-1][1] / nn
            t += (f"<tr><td><b>{e({'ai_personalized': 'AI-personalized', 'generic': 'Generic'}.get(k, k))}</b></td><td>{nn}</td>" + "".join(f"<td>{s[2] * 100:.0f}%</td>" for s in steps)
                  + f"<td><div style='display:flex;gap:8px;align-items:center'><div class='bar' style='width:90px'><span style='width:{min(rate / .2, 1) * 100:.0f}%'></span></div>{rate * 100:.1f}%</div></td><td>{weak}</td></tr>")
        return t + "</tbody></table></div>"
    v = {k: [r for r in rows if r["variant"] == k] for k in ("generic", "ai_personalized")}
    gr, pr = (sum(int(r["meeting"]) for r in v[k]) / len(v[k]) for k in ("generic", "ai_personalized"))
    drafts = """<h3>Step 2: what the skill drafts (illustrative)</h3>
<p>Inputs given to the skill: <b>Operations Manager</b> at a fictional company, <b>Maple Freight</b>; public signal: <i>a post about onboarding 40 new warehouse staff before peak season</i>; offer: a short AI-literacy session for supervisors; ask: a 15-minute call.</p>
<div class="msg"><small>Connection note · under 300 characters</small>Hi Dana, I saw your post about onboarding 40 new warehouse staff before peak. I help operations teams use AI for the repetitive parts of onboarding, like shift guides and FAQs. Happy to connect and share what has worked.</div>
<div class="msg"><small>Follow-up · under 80 words</small>Thanks for connecting, Dana. With 40 new people starting, supervisors usually lose hours answering the same questions. I run a 60-minute session that shows supervisors how to build a simple AI FAQ from your existing material, with a human checking every answer. Would a 15-minute call next week be useful to see if it fits?</div>
<div class="msg"><small>Self-check flags for the human</small>Verify the name and the post before sending · no numbers claimed about Maple Freight · one ask only · a human sends it</div>"""
    body = ('<p class="lead">Two parts work together: a Claude skill drafts personalized messages that a human edits and sends, and an analyzer compares how '
            'personalized and generic messages perform at each stage of the funnel.</p>'
            f'<div class="doc">{drafts}<h3>Step 5: what the analyzer finds</h3>'
            f'<div class="grid2"><div class="kpi"><h3>Generic</h3><div class="big">{gr * 100:.1f}%</div><span style="font-size:13px;color:#666">sent → meeting</span></div>'
            f'<div class="kpi"><h3>AI-personalized</h3><div class="big" style="color:var(--ok)">{pr * 100:.1f}%</div><span style="font-size:13px;color:#666">sent → meeting · {pr / gr:.1f}x generic</span></div></div>'
            f'<h4>By variant</h4>{table("variant")}<h4>By persona</h4>{table("persona")}'
            '<p><b>Read-out:</b> personalization lifts acceptance the most, and the weakest stage moves down the funnel to replies. '
            'Small synthetic sample: treat as directional and keep testing before scaling.</p></div>')
    page("demo-05-outreach.html", "05", "Outreach copilot", "AI-drafted, human-sent prospecting messages, measured stage by stage so you know what to fix next.",
         "05-outreach-copilot", [("Human", "Pick prospect + signal"), ("AI skill", "Draft 3 variants"), ("Human", "Edit and send"), ("Script", "Compare funnel")],
         "python funnel.py --log sample/outreach_log.csv", body, "funnel.py", "sample/outreach_log.csv",
         " The Step 2 messages are an illustrative example of what the skill drafts, following the rules in SKILL.md.")


if __name__ == "__main__":
    main()
