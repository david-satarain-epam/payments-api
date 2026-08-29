"""
Payment API — Schema definitions.

TIER 1 service. Max downtime: 0 minutes.
Consumed by: checkout-web, mobile-app, merchant-portal,
             billing-service, notification-service,
             and 7 external clients via API Gateway.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum


class RefundStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    MXN = "MXN"


@dataclass
class RefundRequest:
    """Single refund request."""
    refund_id: str
    transaction_id: str
    amount: float          # In cents
    reason: str
    customer_email: str


@dataclass
class RefundResponse:
    """Response for a processed refund."""
    refund_id: str
    status: RefundStatus
    processed_at: str
    transaction_id: str
    amount: int


@dataclass
class BatchRefundRequest:
    """Batch refund request. Accepts multiple refunds at once."""
    refunds: List[RefundRequest]
    mode: Optional[str] = "SEQUENTIAL"

    @property
    def total_refunds(self) -> int:
        return len(self.refunds)


@dataclass
class BatchRefundResponse:
    """Batch refund operation result."""
    batch_id: str
    total_refunds: int
    processed: int
    failed: int
    results: List[RefundResponse]