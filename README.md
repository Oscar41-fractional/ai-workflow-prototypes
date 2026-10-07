# AI workflow prototypes · Oscar Farrera

Small, working prototypes that redesign real workflows around AI. Each one starts from a problem I ran into in my own work (partner marketing, channel sales, AI enablement), shows the **solution path** (what the human, the AI and the system each do), and runs with fictional data and Python's standard library only.

**Landing page:** https://oscar41-fractional.github.io/ai-workflow-prototypes/ · **Portfolio with live demo:** https://oscarfarrera-portfolio.netlify.app · **AI practice:** https://www.ai-fractional.com

| # | Prototype | See the output | Type | Workflow it redesigns | Problem to solve |
|---|---|---|---|---|---|
| 01 | [MBR Assistant](01-mbr-assistant) | [Sample output](https://oscar41-fractional.github.io/ai-workflow-prototypes/demo-01-mbr.html) | Script + Claude skill + LLM prompt | Monthly partner business reviews | Rebuilding JMP and MBR production around AI to cut the time (~60% less at AWS Canada) |
| 02 | [Intake prioritizer](02-intake-prioritizer) | [Sample output](https://oscar41-fractional.github.io/ai-workflow-prototypes/demo-02-intake.html) | Script + Claude skill | AI request intake, scoring and decision briefs | Consistent MDF pre-approval using the [FRACTION gate framework](https://www.ai-fractional.com) |
| 03 | [ROI metric tree](03-roi-metric-tree) | [Sample output](https://oscar41-fractional.github.io/ai-workflow-prototypes/demo-03-roi.html) | Scenario model | Business case, break-even and sensitivity for an AI rollout | AI investment case: metric tree, three scenarios, break-even adoption, pass/fail gate |
| 04 | [Capability map](04-capability-map) | [Sample output](https://oscar41-fractional.github.io/ai-workflow-prototypes/capability_map.html) | Data + HTML generator | Go-to-market processes, AI solution paths and where I have done each one | From process pain to AI capability built |
| 05 | [Outreach Assistant](05-outreach-assistant) | [Sample output](https://oscar41-fractional.github.io/ai-workflow-prototypes/demo-05-outreach.html) | Claude skill + analyzer | AI-assisted social selling and funnel measurement | AI-assisted social selling: more LinkedIn conversations, higher lead-to-meeting |

## Quick start
```bash
git clone <this repo> && cd <repo>
python 01-mbr-assistant/mbr.py --data 01-mbr-assistant/sample/partner_activity_2026-05.csv --out out/mbr
python 02-intake-prioritizer/prioritize.py --intake 02-intake-prioritizer/sample/intake.csv --out out/portfolio.md
python 03-roi-metric-tree/roi_model.py --config 03-roi-metric-tree/assumptions_power_users.json --out out/roi
python 04-capability-map/build_map.py --csv 04-capability-map/capability_map.csv --out out/capability_map.html
python 05-outreach-assistant/funnel.py --log 05-outreach-assistant/sample/outreach_log.csv

# rebuild the "See the output" pages in docs/ from the real script output
python build_demos.py
```

## Principles across all five
1. **Calculate, then generate.** Scripts own the numbers; models write the narrative.
2. **Name the solution path.** Every workflow states what people, AI and systems each own.
3. **Measure against a baseline.** Only value that reaches the P&L counts; human review time is a cost.
4. **Gate decisions.** Forbidden zone, readiness, value, then margin above break-even.
5. **Humans decide.** Every output is a draft for review.

See [LESSONS.md](LESSONS.md) for where AI was useful in these builds and where it fell over.

_All company names and data in this repo are fictional. Results cited from past roles come from my CV; no employer or partner data is included._


_Acronyms: JMP = joint marketing plan; MBR = monthly business review; MDF = market development funds; ROI = return on investment; KPI = key performance indicator; LLM = large language model._
