# 05 · Outreach Assistant

**See the output:** [account waves, message drafts, funnel and results](https://oscar41-fractional.github.io/ai-workflow-prototypes/demo-05-outreach.html)

**For roles:** Sales, Marketing, Demand generation, Business Development

**Problem to solve:** AI-assisted outreach to fill cybersecurity analyst roles at MSPs and MSSPs with neurodivergent talent, scaling Clearmind Talent's pipeline on a lean budget.

**Background (real):** From October 2023 to September 2024 I led sales, demand generation and partnerships at a Montreal-area firm that places neurodivergent professionals with employers (shown here under the fictional name Clearmind Talent). Its cybersecurity offer targets managed IT and security providers that cannot fill Tier 1 and Tier 2 analyst roles. I rebuilt outreach around AI: account prioritization, AI-drafted personalized messages under human review, a content and event engine, and stage-by-stage measurement. Results from my CV:
- Email campaigns grew 5x to 1,150 contacts across 264 companies; events grew from 3 to 9.
- LinkedIn conversations tripled to 119 with AI-enabled social selling (LinkedIn SSI top 1%); 67 qualified calls led to 38 meetings (56.7%).
- Model-presentation demos grew 4.6x (10 to 46) and overall pipeline grew 40%.
- 3 placement intents vs. 1 at baseline (prospects asked to review candidates); 1 signed. Together they represent $340K over a 6-month tenure, forecast at a 60% close rate.

**This repo:** the same workflow rebuilt with fictional companies and contacts. The records are synthetic, but their totals are calibrated to the results above (`make_sample.py` fails if they drift).

## Solution path
| Step | Who | What |
|---|---|---|
| 1. Prioritize | Script | `accounts.py` scores 264 accounts on segment, open Tier 1/Tier 2 roles, partner tier and region, and splits them into waves |
| 2. Target | Human | Picks the contact, persona and one public signal (an open posting, a post, an event) |
| 3. Draft | AI (skill) | Three variants (connection note, follow-up, email) matched to the persona, plus a self-check |
| 4. Send | Human | Edits and sends every message; nothing is sent automatically |
| 5. Engage | Human + content | Webinars, events and model-presentation demos turn conversations into meetings |
| 6. Learn | Script | `funnel.py` measures reach, the funnel, AI vs generic, persona and segment results, and before vs after |

## Design choices
- A human sends every message. The AI drafts; it never sends.
- Candidates' privacy comes first: messages describe skills and certifications, never a person's diagnosis.
- Score accounts before writing anything, so the best-fit 21 accounts get personal outreach first.
- Measure each stage, not just the end result: the meeting rate by persona showed the service desk / SOC director is the real buyer.
- Revenue is shown as reported: 6-month value of the placement intents, weighted by the forecast close rate.

## Run it
```bash
python make_sample.py          # regenerate the synthetic, CV-calibrated sample data
python accounts.py --data sample/
python funnel.py --data sample/
```
All company and contact names are fictional; any resemblance to real organizations is coincidental. No real client, candidate or internal data is included.
