# AI workflow prototypes · Oscar Farrera

Small, working prototypes that redesign real workflows around AI. Each one starts from a problem I ran into in my own work (partner marketing, channel sales, AI enablement), shows the **solution path** (what the human, the AI and the system each do), and runs with fictional data and Python's standard library only.

**Landing page:** `docs/index.html` (GitHub Pages) · **Portfolio with live demo:** https://oscarfarrera-portfolio.netlify.app · **AI practice:** https://www.ai-fractional.com

| # | Prototype | Type | Workflow it redesigns | Where it comes from |
|---|---|---|---|---|
| 01 | [MBR Copilot](01-mbr-copilot) | Script + Claude skill + LLM prompt | Monthly partner business reviews | AWS Canada partner program (via The Channel Company): ~60% less JMP/MBR time |
| 02 | [Intake prioritizer](02-intake-prioritizer) | Script + Claude skill | AI request intake, scoring and decision briefs | MDF pre-approval discipline; FRACTION framework |
| 03 | [ROI metric tree](03-roi-metric-tree) | Scenario model | Business case, break-even and sensitivity for an AI rollout | AI investment coursework; pipeline and MDF metrics |
| 04 | [Capability map](04-capability-map) | Data + HTML generator | Go-to-market processes, AI solution paths and where I have done each one | Partnerships, Marketing, Sales and CS roles at AWS Canada, Hornetsecurity, Neuro Plus |
| 05 | [Outreach copilot](05-outreach-copilot) | Claude skill + analyzer | AI-assisted social selling and funnel measurement | Neuro Plus: LinkedIn conversations tripled, 56% lead-to-meeting |

## Quick start
```bash
git clone <this repo> && cd <repo>
python 01-mbr-copilot/mbr.py --data 01-mbr-copilot/sample/partner_activity_2026-05.csv --out out/mbr
python 02-intake-prioritizer/prioritize.py --intake 02-intake-prioritizer/sample/intake.csv --out out/portfolio.md
python 03-roi-metric-tree/roi_model.py --config 03-roi-metric-tree/assumptions_power_users.json --out out/roi
python 04-capability-map/build_map.py --csv 04-capability-map/capability_map.csv --out out/capability_map.html
python 05-outreach-copilot/funnel.py --log 05-outreach-copilot/sample/outreach_log.csv
```

## Principles across all five
1. **Calculate, then generate.** Scripts own the numbers; models write the narrative.
2. **Name the solution path.** Every workflow states what people, AI and systems each own.
3. **Measure against a baseline.** Only value that reaches the P&L counts; human review time is a cost.
4. **Gate decisions.** Forbidden zone, readiness, value, then margin above break-even.
5. **Humans decide.** Every output is a draft for review.

See [LESSONS.md](LESSONS.md) for where AI was useful in these builds and where it fell over.

_All company names and data in this repo are fictional. Results cited from past roles come from my CV; no employer or partner data is included._
