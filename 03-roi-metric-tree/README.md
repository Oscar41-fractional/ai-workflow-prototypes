# 03 · ROI metric tree and scenario model

**See the output:** [broad rollout vs. power users, side by side](https://oscar41-fractional.github.io/ai-workflow-prototypes/demo-03-roi.html)

**For roles:** Sales and Marketing leaders, Partner Development, Revenue Operations

**Problem to solve:** An AI investment case with a metric tree, three scenarios, break-even adoption and a pass/fail gate.

**Background (real):** Investment-committee style AI business cases from my Microsoft *AI Evaluation and Investment Decisions* certificate work, combined with years of pipeline and MDF metrics: 89.6% MDF utilization set as a team benchmark; at Hornetsecurity, Salesforce dashboards that improved pipeline visibility 30%.

**This repo:** one JSON file of assumptions produces a metric tree, three scenarios, break-even adoption with a safety-margin gate, and a two-way sensitivity grid.

## Solution path
| Step | Who | What |
|---|---|---|
| 1. Assume | Human | Sets seats, costs, hours saved and scenario ranges in one JSON file |
| 2. Model | Script | Metric tree, three scenarios, break-even adoption, sensitivity grid |
| 3. Gate | Script | Pass only if base adoption clears break-even by 15+ points |
| 4. Decide | Human | Go, rescope or stop; the model shows which lever matters most |

## The reframe it demonstrates
```bash
python roi_model.py --config assumptions.json --out out/broad            # 80 seats: base ROI -8.5%, margin -8 pts -> FAIL
python roi_model.py --config assumptions_power_users.json --out out/pu   # 30 power users: ROI +38.6%, margin +30 pts -> PASS
```
The broad rollout fails the gate. Narrowing the scope to the people with the most repetitive work passes it with room to spare. Same tool, different question.

## Design choices
- Only **P&L-linked value** counts (realization factor), not "hours saved".
- **Human review time is a cost** (verification tax).
- The decision rule is a **margin above break-even**, not one optimistic ROI number.
