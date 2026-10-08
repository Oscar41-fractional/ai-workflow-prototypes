# 04 · AI capability map: go-to-market

**See the output:** [the live capability map](https://oscar41-fractional.github.io/ai-workflow-prototypes/capability_map.html)

**For roles:** Cross-industry roles in Partnerships, Marketing, Sales and Customer Success; AI Enablement

**Problem to solve:** Going from process pain to AI capability built.

**Background (real):** the go-to-market functions I have worked in: Partnerships (AWS Canada partner program via The Channel Company; Hornetsecurity MSSP channel), Marketing and Sales (Clearmind Talent, AWS co-marketing), and Customer Success (Hornetsecurity, AI-Fractional).

**What it is:** a map of 18 processes across Partnerships, Marketing, Sales and Customer Success. For each process it shows:
- today's pain and the AI pattern (draft, summarize, check, detect, research);
- the **solution path**: what the human, the AI and the system of record each own;
- **where I've done this before**, side by side, with results from my CV;
- whether I have already **rebuilt it with AI**, use AI to assist, or still do it manually (the next candidates to redesign).

## Solution path
| Step | Who | What |
|---|---|---|
| 1. Map | Human | One CSV row per process: pain, AI pattern, roles, scores, track record |
| 2. Build | Script | Generates the self-contained HTML map and the "redesign next" list |
| 3. Choose | Human | Picks the next manual process to rebuild, highest opportunity x readiness first |

## Design choices
- Every process is split three ways: what the **human**, the **AI** and the **system of record** own.
- My track record sits next to each process, so the map is evidence, not theory.
- The "next to redesign" list ranks manual processes by **Opportunity x Readiness** (1-5 each, maximum 25); ties go to the process that runs more often per month.
- Scores are my own estimates and are labelled as such.

## Run it
```bash
python build_map.py --csv capability_map.csv --out capability_map.html
```
Opportunity and readiness scores are my own estimates. No employer or partner data is included.
