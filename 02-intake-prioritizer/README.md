# 02 · Transformation intake prioritizer

**See the output:** [sample ranked portfolio](https://oscar41-fractional.github.io/ai-workflow-prototypes/demo-02-intake.html)

**Problem to solve:** Consistent MDF (market development funds) pre-approval using the [FRACTION gate framework](https://www.ai-fractional.com).

**Background (real):** Managing MDF across 19 partners meant judging dozens of funding requests consistently, with the same pre-approval rules and proof-of-execution checks every time. At AI-Fractional I turned that habit into the gate-based **FRACTION** framework for AI use cases.

**This repo:** an intake log plus a script that applies the same gates to every AI request and outputs a ranked portfolio with decision briefs. A Claude/Cowork skill (`SKILL.md`) turns a free-text request into an intake row.

## Solution path
| Step | Who | What |
|---|---|---|
| 1. Capture | AI (skill) | Turns a free-text request into an intake row and asks only the missing questions |
| 2. Confirm | Human | Requester confirms or corrects the proposed value and readiness scores |
| 3. Gate and rank | Script | Forbidden zone, readiness zone, quadrant and adjustments, the same way every time |
| 4. Brief | Script | One decision brief per request, with size of prize and scoring trail |
| 5. Decide | Human | Portfolio owner approves, and gives every "not now" a re-entry condition and date |

## Design choices
The ranking does not depend on who asked: every request goes through the same gates.

1. **Forbidden zone:** legal or policy hard stops are removed before scoring (for example AI screening of candidates).
2. **Readiness zone:** data readiness × process readiness.
3. **Value × readiness quadrant**, then adjustments: change capacity (−4), reusable pattern (+2), irreversible errors (−3).

## Run it
```bash
python prioritize.py --intake sample/intake.csv --out out/portfolio.md
```
Sample result: support ticket triage ranks first; the board metrics pack has the highest value but is parked until the data is fixed; candidate screening is excluded.
