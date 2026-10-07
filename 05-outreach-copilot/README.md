# 05 · Outreach copilot and funnel analyzer

**Origin (real):** At Neuro Plus (2023–2024) I rebuilt our prospecting around AI-assisted social selling. LinkedIn conversations tripled (to 119), lead-to-meeting reached 56%, and my LinkedIn Social Selling Index reached the top 1%.

**This repo:** a Claude/Cowork skill that drafts personalized outreach under human review (`SKILL.md`), and a funnel analyzer that compares variants stage by stage and names the weakest stage.

```bash
python funnel.py --log sample/outreach_log.csv
```
The sample log is synthetic. It shows the pattern I tracked: personalization lifts acceptance most, and the weakest stage then moves down the funnel.
