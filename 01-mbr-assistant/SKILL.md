---
name: mbr-assistant
description: Draft a partner monthly business review (MBR) from an activity spreadsheet. Use when someone uploads partner activity data (MDF, leads, opportunities, pipeline) and asks for an MBR, partner review or monthly summary.
---

# MBR Assistant (Claude / Cowork skill)

## When to use
The user provides a CSV or spreadsheet of partner activities and wants a monthly business review.

## Steps
1. **Check the data.** Confirm the columns: partner, date, activity, type, mdf_spent, leads, opportunities, pipeline_usd, marketplace_deals. List any missing or non-numeric values and ask before guessing.
2. **Calculate, do not generate.** Run `python mbr.py --data <file> --partner "<name>"` from this folder. Use its KPI totals as the only source of numbers.
3. **Analyze.** Rank funded activities by pipeline per MDF dollar. Flag funded activities with zero opportunities, cost per opportunity above $2,000, and lead sets above 40 with under 3% conversion.
4. **Draft.** Follow the five sections in `prompt_template.md`. Keep it to one page.
5. **Hand back for review.** End with: "Draft for human review. Numbers come from mbr.py; verify activity names and next steps with the partner owner."

## Guardrails
- Never invent or round numbers differently from the script output.
- No confidential partner data in tools that are not approved for it.
- Recommendations are suggestions for discussion, not decisions.
