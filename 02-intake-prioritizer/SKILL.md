---
name: transformation-intake
description: Turn a free-text AI or process-improvement request into a structured intake record, ask the missing questions, and score it with prioritize.py. Use when someone says "I have an idea for AI in my team", submits a request, or asks where a request ranks.
---

# Transformation intake (Claude / Cowork skill)

## Steps
1. **Restate the request** in one sentence: who has the problem, what happens today, and what "better" looks like.
2. **Fill the intake fields** (see `sample/intake.csv` header). Ask only for what is missing, in one message:
   - volume per month and minutes per item today
   - data involved and its class (green = public, amber = internal, red = personal, financial, legal or regulated)
   - whether any legal or policy rule reserves the decision for a human (forbidden zone)
3. **Propose scores** for value (1-5) and readiness (1-5) using the rubric below and show your reasoning. The requester confirms or corrects them.
4. **Append the row** to the intake log and run `python prioritize.py --intake <log> --out out/portfolio.md`.
5. **Reply with the rank, quadrant and decision**, plus the solution path: what the human does, what AI does, what the system of record does.

## Rubric
| Score | Value | Readiness |
|---|---|---|
| 5 | Shifts a core KPI (for example cost to serve -20%) | Clean, structured, access-controlled data; stable process |
| 4 | 10-20% gain on a key process | Minor cleanup |
| 3 | 5-10% productivity gain | Defined cleanup project needed |
| 2 | Under 5%; convenience | Largely unstructured |
| 1 | Negligible | Unknown quality |

## Guardrails
- Score the request, not the requester.
- Red data plus irreversible outcome means human approval on every output.
- Every "not now" gets a re-entry condition and a date.
