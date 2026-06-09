---
name: reg-e-disputes
description: Handle debit card fraud and unauthorized ACH transfers under Regulation E
---

# Reg E Dispute Skill

Regulation E governs all electronic fund transfers on consumer deposit accounts.

## Key Rules You Must Follow

- **10-business-day rule**: Bank must provisionally credit the customer within 10 business days of receiving the dispute, or it loses the right to withhold funds during investigation.
- **45-day investigation window**: Standard disputes must be resolved within 45 days (90 days for POS, foreign, or new accounts).
- **Error notice**: Customer must report within 60 days of the statement date showing the error.
- **Liability caps**:
  - Reported within 2 days: customer liable for max $50
  - Reported 3–60 days: customer liable for max $500
  - Reported after 60 days: unlimited liability

## Investigation Steps

1. Pull transaction records from the lookup tool — get transaction ID, merchant, amount, date, channel (POS/ATM/ACH).
2. Check if the dispute is within the 60-day reporting window.
3. Calculate customer liability based on when they reported.
4. Determine if provisional credit is required (severity >= 4 OR days since incident >= 8).
5. Draft response using the appropriate template from assets/.

## Escalation Triggers

- Transaction > $2,500 → escalate to fraud ops team
- Suspected card skimming (multiple small transactions, new merchant) → escalate + flag for fraud analytics
- Customer reports identity theft → escalate to ID theft unit

## Templates Available

- `assets/provisional_credit_letter.md`
- `assets/dispute_denial_letter.md`
- `assets/escalation_notice.md`
