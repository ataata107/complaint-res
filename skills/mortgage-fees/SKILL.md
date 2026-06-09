---
name: mortgage-fees
description: Resolve escrow errors, improper fee charges, and force-placed insurance disputes
---

# Mortgage Fee Skill

## Key Rules

- **RESPA Section 10**: Escrow account can hold max 2 months of cushion. Overages must be refunded within 30 days of annual escrow analysis.
- **Force-placed insurance**: Bank must send two notices (45 days apart) before placing insurance. If customer had coverage, bank must cancel force-placed policy and refund premiums retroactively.
- **Payoff statement**: Must be provided within 7 business days of request (RESPA).
- **Qualified Written Request (QWR)**: Customer letters disputing mortgage account must be acknowledged within 5 business days, resolved within 30.

## Investigation Steps

1. Pull loan details: current balance, escrow balance, payment history, insurance status.
2. Identify fee type: late fee, escrow shortage, force-placed insurance, other.
3. For escrow disputes: run escrow analysis to determine if overage or shortage is correctly calculated.
4. For force-placed insurance: verify whether customer had valid coverage at time of placement.
5. Calculate any refund owed.
6. Draft response with specific dollar amounts and timeline for resolution.

## Escalation Triggers

- Alleged RESPA violation → compliance team review
- Force-placed insurance > 6 months without customer notice → legal review
- Customer mentions attorney or lawsuit → immediate escalation
