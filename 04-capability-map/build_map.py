#!/usr/bin/env python3
"""AI capability map builder: go-to-market functions.

Reads capability_map.csv (one row per process in Partnerships, Marketing, Sales and
Customer Success) and writes a self-contained HTML map. Each process shows today's
pain, the AI pattern, the solution path (what the human, the AI and the system of
record each do) and, side by side, where I have done this work before and whether
I have already rebuilt it with AI.

Usage: python build_map.py --csv capability_map.csv --out capability_map.html
Standard library only. Scores are my own estimates; results quoted are from my CV.
"""
import argparse, csv, html
from collections import Counter, OrderedDict

STATUS = OrderedDict([("Rebuilt with AI", "#1d7a4a"), ("AI-assisted", "#b5121d"), ("Manual today", "#6b6764")])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--csv", default="capability_map.csv"); ap.add_argument("--out", default="capability_map.html")
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.csv, newline="", encoding="utf-8")))
    by_fn = OrderedDict()
    for r in rows: by_fn.setdefault(r["function"], []).append(r)
    cnt = Counter(r["ai_status"] for r in rows)
    nxt = sorted([r for r in rows if r["ai_status"] == "Manual today"], key=lambda r: (-(int(r["opportunity"]) * int(r["readiness"])), -int(r["runs_per_month"])))[:5]
    e = html.escape
    def heat(v): return f"background:rgba(240,30,44,{0.12 + 0.17 * (int(v) - 1):.2f})"
    secs = []
    for fn, rs in by_fn.items():
        trs = "".join(f"""<tr><td class="proc"><b>{e(r['process'])}</b><span class="st" style="background:{STATUS[r['ai_status']]}">{e(r['ai_status'])}</span>
<div class="pain">{e(r['pain_today'])}</div><div class="sc"><span style="{heat(r['opportunity'])}">Opportunity {r['opportunity']}/5</span><span style="{heat(r['readiness'])}">Readiness {r['readiness']}/5</span><span class="sc-t">Score {int(r['opportunity']) * int(r['readiness'])}/25</span><span class="sc-t">~{r['runs_per_month']} runs/month</span></div></td>
<td class="path"><span><i>Human</i>{e(r['human_role'])}</span><span><i>AI · {e(r['ai_pattern'])}</i>{e(r['ai_role'])}</span><span><i>System</i>{e(r['system_role'])}</span></td>
<td class="exp">{e(r['where_ive_done_this'])}</td></tr>""" for r in rs)
        secs.append(f'<section><h2>{e(fn)}</h2><div class="tw"><table><thead><tr><th>Process</th><th>Solution path</th><th>Where I&#39;ve done this before</th></tr></thead><tbody>{trs}</tbody></table></div></section>')
    stats = "".join(f'<div class="k"><b>{cnt.get(s, 0)}</b><span>{s}</span></div>' for s in STATUS)
    nlist = "".join(f"<li><b>{e(r['function'])}:</b> {e(r['process'])} <em>(Opportunity {r['opportunity']} x Readiness {r['readiness']} = <b>{int(r['opportunity']) * int(r['readiness'])}</b>; runs ~{r['runs_per_month']} time{'' if r['runs_per_month'] == '1' else 's'}/month)</em></li>" for r in nxt)
    ties = len({int(r['opportunity']) * int(r['readiness']) for r in nxt}) < len(nxt)
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Capability Map · Go-to-Market</title><style>
*{{box-sizing:border-box}}body{{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#f7f6f3;color:#121212}}
header{{background:#121212;color:#ecebe7;padding:28px 20px}}header .w{{max-width:1200px;margin:auto}}h1{{margin:0;font-size:28px}}header p{{margin:8px 0 0;color:#bdbab6;max-width:75ch}}
.w{{max-width:1200px;margin:auto;padding:22px 20px}}.kpis{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px}}
.k{{background:#fff;border-top:4px solid #f01e2c;padding:10px 16px;min-width:150px}}.k b{{font-size:26px;display:block}}.k span{{font-size:13px;color:#555}}
.next{{background:#fff;border-left:4px solid #f01e2c;padding:12px 18px;margin-bottom:10px}}.next h3{{margin:0 0 6px;font-size:17px}}.next ol{{margin:0;padding-left:20px}}
section{{margin-top:26px}}h2{{font-size:20px;margin:0 0 10px;border-bottom:2px solid #121212;padding-bottom:6px}}
.tw{{overflow-x:auto;background:#fff;border:1px solid #ddd;border-radius:8px}}table{{border-collapse:collapse;width:100%;min-width:820px}}
th{{background:#121212;color:#fff;text-align:left;font-size:13px;padding:9px 12px}}th:last-child{{background:#b5121d}}
td{{vertical-align:top;padding:12px;border-bottom:1px solid #eee;font-size:13.5px}}tr:last-child td{{border:0}}
.proc{{width:30%}}.proc b{{display:block;font-size:15px;margin-bottom:4px}}.st{{display:inline-block;color:#fff;font-size:11px;padding:2px 8px;border-radius:99px;margin-bottom:6px}}
.pain{{color:#555;margin-bottom:8px}}.sc-t{{background:#ecebe7}}.how{{margin:0 0 8px;font-size:14px;color:#444}}details{{margin-top:10px;font-size:14px}}summary{{cursor:pointer;font-weight:600;color:#b5121d}}.sc{{display:flex;gap:6px;flex-wrap:wrap;font-size:12px}}.sc span{{padding:2px 8px;border-radius:4px}}
.path{{width:38%}}.path span{{display:block;background:#f7f6f3;padding:5px 8px;border-radius:4px;margin-bottom:4px}}
.path i{{font-style:normal;font-weight:600;color:#b5121d;display:block;font-size:11px;text-transform:uppercase;letter-spacing:.05em}}
.exp{{width:32%;background:#fbf3f3;border-left:3px solid #f01e2c;line-height:1.5}}footer{{color:#8d8a88;font-size:12px;padding:10px 20px 30px;max-width:1200px;margin:auto}}
</style></head><body><header><div class="w" style="padding:0"><a href="https://oscar41-fractional.github.io/ai-workflow-prototypes/" style="color:#ecebe7;font-size:14px;text-decoration:none;border:1px solid #444;padding:6px 12px;border-radius:5px;display:inline-block;margin-bottom:14px">← All prototypes</a><h1>AI capability map: go-to-market</h1>
<p>Partnerships, Marketing, Sales and Customer Success. For each process: today&#39;s pain, what the human, the AI and the system each own, and where I have done this work before.</p><p style="font-size:14px">For roles: <b style="color:#fff">Cross-industry roles in Partnerships, Marketing, Sales and Customer Success · AI Enablement</b></p></div></header>
<div class="w"><div class="kpis">{stats}</div><div class="next"><h3>Next to redesign with AI</h3><p class="how">Of the processes still done manually, these five have the highest <b>score = Opportunity x Readiness</b> (maximum 5 x 5 = 25). {"Where scores tie, the process that runs more often comes first, because each improvement pays back more times a month." if ties else ""}</p><ol>{nlist}</ol>
<details><summary>What the 1-5 ratings mean</summary><div class="tw" style="margin-top:8px"><table style="min-width:0"><thead><tr><th>Rating</th><th>Opportunity: value of redesigning it with AI</th><th>Readiness: how easy it is to start now</th></tr></thead><tbody>
<tr><td>5</td><td>Core, repetitive work with a big time or revenue impact</td><td>Clean data in one system; stable, documented process</td></tr>
<tr><td>4</td><td>Frequent work with a clear time saving</td><td>Data mostly available; process stable with minor cleanup</td></tr>
<tr><td>3</td><td>Useful but occasional or moderate saving</td><td>Data spread across tools; process varies</td></tr>
<tr><td>2</td><td>Small saving; mostly convenience</td><td>Data largely unstructured; no agreed process</td></tr>
<tr><td>1</td><td>Negligible</td><td>Unknown data quality; heavy judgement or legal constraints</td></tr></tbody></table></div>
<p class="how">Ratings and run frequencies are my own estimates from doing this work.</p></details></div>
{''.join(secs)}</div><footer>Generated by build_map.py from capability_map.csv. Opportunity, readiness and run frequency are my own estimates. Results quoted come from my CV; no employer or partner data is included. © 2026 Oscar Farrera · All rights reserved.<br><br>Acronyms: ACE = AWS partner co-sell program (APN Customer Engagements); AI = artificial intelligence; ARR = annual recurring revenue; AWS = Amazon Web Services; CAD = Canadian dollars; CPPO = Channel Partner Private Offer (AWS Marketplace); CRM = customer relationship management; GPTs = custom ChatGPT assistants; ISV = independent software vendor; JMP = joint marketing plan; KPI = key performance indicator; MBR = monthly business review; MCP = Model Context Protocol (connects AI to tools); MDF = market development funds; MSSP = managed security service provider; SI = systems integrator; SPPO = private offer made directly by the seller (AWS Marketplace); SSI = LinkedIn Social Selling Index; VP = vice president.</footer></body></html>"""
    import os; os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(doc)
    print(f"[ok] {len(rows)} processes across {len(by_fn)} functions -> {a.out}")

if __name__ == "__main__":
    main()
