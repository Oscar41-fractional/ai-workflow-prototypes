---
name: outreach-assistant
description: Draft personalized LinkedIn and email outreach to MSP, MSSP and IT employers for a neurodiversity talent-placement offer, with guardrails, and log it for funnel analysis. Use when asked to write prospecting messages, connection notes, follow-ups or event invitations for Clearmind Cyber.
---

# Outreach Assistant (Claude / Cowork skill)

Built for Clearmind Talent's cybersecurity offer (Clearmind Cyber): placing trained, neurodivergent Tier 1 / Tier 2 analysts at managed IT and security
providers. The buyer is usually the service desk or SOC director who cannot fill open roles fast enough.

## Steps
1. **Pick the account and contact.** Start from Wave 1 in `accounts.py` (best fit first). Note the persona and the segment.
2. **Find one public signal:** an open Tier 1/Tier 2 posting, a post about growth or new clients, an event they attended.
   Use only public information the user provides or links. Never guess personal details.
3. **Match the message to the persona:**
   - Service desk / SOC director: open roles filled faster, trained analysts, onboarding support included.
   - CTO / VP technology: capacity to deliver what sales has sold; certification path for each analyst.
   - CEO / owner: cost of unfilled roles; a consultant billed at a rate similar to an employee, no recruiting fee.
   - HR / talent acquisition: a pre-screened, pre-trained talent pool; support through onboarding.
   - People & inclusion lead: invite to a webinar first; inclusion as a business result, not a favour.
4. **Draft three variants** in the contact's language (French or English): connection note under 300 characters,
   follow-up under 80 words, email under 120 words. Each one names the signal, states one relevant outcome and ends with
   a single low-friction ask (a 15-minute call, a candidate profile review, or a webinar seat).
5. **Self-check:** no flattery, no invented facts or numbers, one ask only, plain language. Flag anything the user must verify.
6. **Log it:** update the contact's row (variant, reply or conversation, qualified call, meeting, demos) so `funnel.py`
   can compare variants, personas and segments.

## Guardrails
- A human sends every message. The AI drafts; it never sends.
- **Candidates' privacy comes first.** Never mention a specific candidate's diagnosis or personal details. Describe skills,
  certifications and work style only, and only with the candidate's consent.
- Present neurodiversity as a talent and business advantage, never as charity.
- Respect platform terms and Canada's Anti-Spam Legislation (CASL): consent, identification, unsubscribe in every email.
- Do not store personal data beyond what the log needs.
