# 02 · Transformation intake prioritizer

**Origin (real):** Managing MDF across 19 partners meant judging dozens of funding requests consistently, with the same pre-approval rules and proof-of-execution checks every time. At AI-Fractional I turned that habit into the gate-based **FRACTION** framework for AI use cases.

**This repo:** an intake log plus a script that applies the same gates to every AI request and outputs a ranked portfolio with decision briefs. A Claude/Cowork skill (`SKILL.md`) turns a free-text request into an intake row.

## Gates
1. **Forbidden zone:** legal or policy hard stops are removed before scoring (for example AI screening of candidates).
2. **Readiness zone:** data readiness × process readiness.
3. **Value × readiness quadrant**, then adjustments: change capacity (−4), reusable pattern (+2), irreversible errors (−3).

## Run it
```bash
python prioritize.py --intake sample/intake.csv --out out/portfolio.md
```
Sample result: support ticket triage ranks first; the board metrics pack has the highest value but is parked until the data is fixed; candidate screening is excluded.
