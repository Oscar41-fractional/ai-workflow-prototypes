# 05 · Outreach Assistant and funnel analyzer

**See the output:** [sample drafts and funnel results](https://oscar41-fractional.github.io/ai-workflow-prototypes/demo-05-outreach.html)

**Problem to solve:** AI-assisted social selling to increase LinkedIn conversations and lead-to-meeting conversion.

**Background (real):** At Neuro Plus (2023–2024) I rebuilt our prospecting around AI-assisted social selling. LinkedIn conversations tripled (to 119), lead-to-meeting reached 56%, and my LinkedIn Social Selling Index reached the top 1%.

**This repo:** a Claude/Cowork skill that drafts personalized outreach under human review (`SKILL.md`), and a funnel analyzer that compares variants stage by stage and names the weakest stage.

## Solution path
| Step | Who | What |
|---|---|---|
| 1. Target | Human | Picks the prospect, persona and one public signal |
| 2. Draft | AI (skill) | Three variants (connection note, follow-up, email) plus a self-check |
| 3. Send | Human | Edits and sends every message; nothing is sent automatically |
| 4. Log | System | One row per prospect: variant, accepted, replied, meeting |
| 5. Learn | Script | Compares variants stage by stage and names the weakest stage |

## Design choices
- A human sends every message. The AI drafts; it never sends.
- Guardrails are in the skill: no invented facts, one ask, anti-spam rules (CASL in Canada).
- Measure each stage, not just the end result: fixing one stage moves the bottleneck down the funnel.

## Run it
```bash
python funnel.py --log sample/outreach_log.csv
```
The sample log is synthetic: 240 prospects at Canadian accounting and advisory firms of 100 to 500 staff (Managing Partner, COO, HR Director, IT Manager), half contacted with generic messages and half with AI-personalized ones. The sample output page adds a worked example for one fictional account, Rivière Advisory Group. It shows the pattern I tracked: personalization lifts acceptance most, and the weakest stage then moves down the funnel.
