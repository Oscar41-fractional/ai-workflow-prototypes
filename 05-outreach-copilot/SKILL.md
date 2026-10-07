---
name: outreach-copilot
description: Draft personalized LinkedIn or email outreach for a target account and persona, with guardrails, and log it for funnel analysis. Use when asked to write prospecting messages, connection notes or follow-ups.
---

# Outreach copilot (Claude / Cowork skill)

## Steps
1. **Collect inputs:** persona, company, one public signal (post, news, job opening), the offer, and the one action you want (accept, reply, meeting).
2. **Research lightly:** use only public information the user provides or links. Never guess personal details.
3. **Draft three variants** (connection note under 300 characters, follow-up under 80 words, email under 120 words). Each variant references the signal, states one relevant outcome, and ends with a single low-friction ask.
4. **Self-check:** no flattery, no invented facts or numbers, no more than one question, plain language. Flag anything the user must verify.
5. **Log it:** append a row to the outreach log (`prospect_id, persona, channel, variant, accepted, replied, meeting`) so `funnel.py` can compare variants.

## Guardrails
- A human sends every message. No automated sending.
- Respect platform terms and anti-spam law (for example CASL in Canada): consent, identification, unsubscribe for email.
- Do not store personal data beyond what the log needs.
