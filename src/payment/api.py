"""
Payment API — Single refund processing.

Core endpoint: POST /refund
TIER 1 — Payment processing.
Breaks here = money stops flowing.
"""

from datetime import datetime, timezone
from .schema import RefundRequest, RefundResponse, RefundStatus


def process_refund(request: RefundRequest) -> RefundResponse:
    """
    Process a single refund through the payment gateway.

    Args:
        request: Validated refund request.

    Returns:
        RefundResponse with processing status.

    Raises:
        ValueError: If validation fails.
    """
    if request.partial_refund_amount is not None:
        if request.partial_refund_amount <= 0:
            raise ValueError("partial_refund_amount must be greater than 0")
        if request.partial_refund_amount > request.amount:
            raise ValueError("partial_refund_amount cannot exceed total amount")
        
    # ── Validation ──
    if not request.refund_id:
        raise ValueError("refund_id is required")

    if not request.transaction_id:
        raise ValueError("transaction_id is required")

    if request.amount <= 0:
        raise ValueError("amount must be greater than 0")

    # ── Payment gateway call ──
    gateway_result = _call_payment_gateway(
        transaction_id=request.transaction_id,
        amount=request.amount,
        reason=request.reason,
    )

    # ── Notification ──
    _send_refund_notification(
        email=request.customer_email,
        refund_id=request.refund_id,
        amount=request.amount,
        status="PROCESSED" if gateway_result["success"] else "FAILED",
    )

    return RefundResponse(
        refund_id=request.refund_id,
        status=RefundStatus.PROCESSED if gateway_result["success"] else RefundStatus.FAILED,
        processed_at=datetime.now(timezone.utc).isoformat(),
        transaction_id=request.transaction_id,
        amount=request.amount,
    )


# ── Internal helpers (mocked for demo) ──

def _call_payment_gateway(transaction_id: str, amount: int, reason: str) -> dict:
    """In production: calls external payment processor (Stripe/Adyen)."""
    return {
        "success": True,
        "gateway_ref": f"gw-{int(datetime.now().timestamp())}",
        "status": "PROCESSED",
    }


def _send_refund_notification(email: str, refund_id: str, amount: int, status: str) -> None:
    """In production: sends email via notification-service."""
    print(f"[NOTIFICATION] Refund {refund_id} — {status} — sent to {email}")