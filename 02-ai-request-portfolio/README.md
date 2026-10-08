# 02 · AI Transformation Request Portfolio

**See the output:** [sample ranked portfolio](https://oscar41-fractional.github.io/ai-workflow-prototypes/demo-02-intake.html)

**For roles:** Sales, Marketing, Business Development, Partner Development, AI Enablement

**Problem to solve:** Consistent MDF (market development funds) pre-approval using the [FRACTION gate framework](https://www.ai-fractional.com).

**Background (real):** Managing MDF across 19 partners meant judging dozens of funding requests consistently, with the same pre-approval rules and proof-of-execution checks every time. At AI-Fractional I turned that habit into the gate-based **FRACTION** framework for AI use cases.

**This repo:** an intake log of AI requests from Sales, Marketing, Business Development and Partner Development teams, plus a script that applies the same gates to every request and outputs a ranked portfolio with decision briefs. A Claude/Cowork skill (`SKILL.md`) turns a free-text request into an intake row.

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
Sample result: 8 AI requests from Sales, Marketing, Business Development and Partner Development teams. Partner business review drafts and inbound lead research rank as "build the business case now"; campaign asset drafts get a small pilot; account research and the MDF claim pre-check are worth doing but need data or process fixes first; win-loss summaries and partner fit scoring are parked until their data and process are ready; mass LinkedIn scraping is excluded (platform terms and anti-spam law).
