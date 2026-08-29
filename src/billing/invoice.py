"""
Billing service — Invoice management.

Handles invoice lifecycle: PAID → REFUNDED.
Consumed by: payment-api, merchant-portal.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Invoice:
    invoice_id: str
    transaction_id: str
    amount: int
    currency: str
    status: str
    created_at: str
    updated_at: str


def mark_invoice_as_refunded(invoice_id: str) -> Invoice:
    """Mark invoice as refunded after successful refund processing."""
    now = datetime.now(timezone.utc).isoformat()
    return Invoice(
        invoice_id=invoice_id,
        transaction_id=f"txn-{invoice_id}",
        amount=0,
        status="REFUNDED",
        created_at=now,
        updated_at=now,
    )


def get_invoice(invoice_id: str) -> Optional[Invoice]:
    """Retrieve invoice by ID."""
    return Invoice(
        invoice_id=invoice_id,
        transaction_id=f"txn-{invoice_id}",
        amount=4999,
        status="PAID",
        created_at="2026-08-01T10:00:00Z",
        updated_at="2026-08-01T10:00:00Z",
    )