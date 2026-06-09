---
name: complaint-triage
description: Classify inbound complaint by type, severity, and regulatory urgency
---

# Complaint Triage Skill

Your job is to analyze the raw complaint text and produce a structured classification.

## Steps

1. **Identify complaint category** — pick exactly one:
   - `reg_e_dispute` — debit card fraud, unauthorized ACH, ATM dispute
   - `wire_transfer` — missing wire, wrong beneficiary, wire fraud
   - `mortgage_fee` — escrow error, improper fee, force-placed insurance
   - `general_service` — account access, statement error, customer service

2. **Set regulatory flag** — pick all that apply:
   - `REG_E` — any unauthorized electronic fund transfer on a consumer account
   - `UDAP` — unfair, deceptive, or abusive acts (surprise fees, misleading terms)
   - `CFPB_REPORTABLE` — complaint that must be logged in CFPB system
   - `NONE` — no regulatory flag

3. **Score severity 1–5**:
   - 5: Financial loss > $1,000 or ongoing fraud
   - 4: Financial loss < $1,000 or time-sensitive (wire cutoff)
   - 3: Fee dispute, moderate impact
   - 2: Service issue, no financial impact
   - 1: General inquiry mislabeled as complaint

4. **Extract key facts**:
   - Dollar amount (if mentioned)
   - Date of incident
   - Account type (checking, savings, mortgage, etc.)
   - Customer sentiment (angry, distressed, confused, neutral)

## Output Format

Return a JSON object:
```json
{
  "category": "<category>",
  "regulatory_flags": ["<flag>", ...],
  "severity": <1-5>,
  "dollar_amount": <float or null>,
  "incident_date": "<YYYY-MM-DD or null>",
  "account_type": "<type or null>",
  "sentiment": "<angry|distressed|confused|neutral>",
  "summary": "<one sentence summary of the complaint>"
}
```
