import json
import uuid
from datetime import datetime, timedelta
from langchain_core.tools import tool


@tool
def lookup_transaction(transaction_id: str) -> str:
    """Look up a transaction by ID. Returns amount, merchant, date, channel, and status."""
    mock_db = {
        "TXN001": {
            "id": "TXN001",
            "amount": 247.50,
            "merchant": "UNKNOWN MERCHANT - ONLINE",
            "date": "2026-05-28",
            "channel": "POS",
            "account_last_four": "4821",
            "account_type": "checking",
            "status": "settled",
        },
        "TXN002": {
            "id": "TXN002",
            "amount": 15000.00,
            "merchant": "WIRE TRANSFER",
            "date": "2026-06-01",
            "channel": "WIRE",
            "beneficiary": "ACME CORP - CHASE BANK",
            "imad": "20260601MMQFMPQR000427",
            "status": "settled",
        },
    }
    txn = mock_db.get(transaction_id)
    if not txn:
        return json.dumps({"error": f"Transaction {transaction_id} not found"})
    return json.dumps(txn)


@tool
def lookup_customer(account_last_four: str) -> str:
    """Look up customer account details by last four digits of account number."""
    mock_db = {
        "4821": {
            "name": "Sarah Johnson",
            "account_last_four": "4821",
            "account_type": "checking",
            "open_date": "2019-03-15",
            "dispute_history_count": 1,
            "current_balance": 1842.33,
        }
    }
    customer = mock_db.get(account_last_four)
    if not customer:
        return json.dumps({"error": "Account not found"})
    return json.dumps(customer)


@tool
def create_case(category: str, severity: int, account_last_four: str, summary: str) -> str:
    """Create a case record in the complaint management system. Returns a case ID and SLA deadline."""
    case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"
    sla_days = 10 if severity >= 4 else 45
    return json.dumps({
        "case_id": case_id,
        "category": category,
        "severity": severity,
        "account": account_last_four,
        "summary": summary,
        "created_at": datetime.now().isoformat(),
        "status": "open",
        "sla_deadline": (datetime.now() + timedelta(days=sla_days)).strftime("%Y-%m-%d"),
    })


@tool
def escalate_case(case_id: str, escalation_type: str, reason: str) -> str:
    """Escalate a case to a specialized team.

    escalation_type options: fraud_ops, wire_fraud_unit, id_theft_unit, compliance, legal, senior_review
    """
    return json.dumps({
        "case_id": case_id,
        "escalated_to": escalation_type,
        "reason": reason,
        "escalation_time": datetime.now().isoformat(),
        "expected_response_days": 2,
    })
