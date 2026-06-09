---
name: wire-transfers
description: Investigate missing wires, wrong beneficiary, and wire fraud claims
---

# Wire Transfer Skill

## Key Rules

- **Same-day recall**: A wire can be recalled same day before the Fed's 6pm ET cutoff. After cutoff, recall requires beneficiary bank cooperation.
- **SWIFT gpi**: International wires have a UETR tracker — always pull this to show the customer real-time status.
- **Wrong beneficiary**: If funds landed at wrong account due to bank error, bank is liable for full recovery. Customer error = best-effort recovery only.
- **Wire fraud**: If customer was socially engineered into sending a wire, this is not a Reg E error — it is a fraud case. Escalate to wire fraud unit immediately.

## Investigation Steps

1. Pull wire details using transaction lookup tool: IMAD/OMAD reference, beneficiary bank, amount, send time.
2. Check wire status: pending, settled, or returned.
3. Determine fault: bank error vs. customer-initiated vs. fraud.
4. If same-day and pre-cutoff → attempt immediate recall via internal wire desk tool.
5. If international → pull SWIFT gpi tracking and provide UETR to customer.
6. Draft response based on fault determination.

## Escalation Triggers

- Wire > $50,000 → senior review required
- Fraud suspected (customer describes "investment opportunity", "IRS", or "grandchild in trouble") → wire fraud unit + SAR consideration
- Beneficiary bank is unresponsive after 3 business days → regulatory escalation path
