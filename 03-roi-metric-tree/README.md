# 03 · ROI metric tree and scenario model

**Origin (real):** Investment-committee style AI business cases from my Microsoft *AI Evaluation and Investment Decisions* certificate work, combined with years of pipeline and MDF metrics: 89.6% MDF utilization set as a team benchmark; at Hornetsecurity, Salesforce dashboards that improved pipeline visibility 30%.

**This repo:** one JSON file of assumptions produces a metric tree, three scenarios, break-even adoption with a safety-margin gate, and a two-way sensitivity grid.

## The reframe it demonstrates
```bash
python roi_model.py --config assumptions.json --out out/broad            # 80 seats: base ROI -8.5%, margin -8 pts -> FAIL
python roi_model.py --config assumptions_power_users.json --out out/pu   # 30 power users: ROI +38.6%, margin +30 pts -> PASS
```
The broad rollout fails the gate. Narrowing the scope to the people with the most repetitive work passes it with room to spare. Same tool, different question.

## Principles built in
- Only **P&L-linked value** counts (realization factor), not "hours saved".
- **Human review time is a cost** (verification tax).
- The decision rule is a **margin above break-even**, not one optimistic ROI number.
