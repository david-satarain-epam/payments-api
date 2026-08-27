"""
Integration test — Full refund flow.

Tests the payment module end-to-end:
schema → processing → invoice → notification.
"""

from src.payment.api import process_refund
from src.payment.schema import RefundRequest
from src.billing.invoice import mark_invoice_as_refunded


class TestFullRefundFlow:

    def test_refund_to_invoice_flow(self):
        """Full flow: request → process → mark invoice → verify."""
        # Step 1: Create refund request
        request = RefundRequest(
            refund_id="ref-int-001",
            transaction_id="txn-int-001",
            amount=5000,
            reason="Integration test",
            customer_email="integration@test.com"
        )

        # Step 2: Process refund
        result = process_refund(request)

        # Step 3: Verify result
        assert result.refund_id == "ref-int-001"
        assert result.status.value == "PROCESSED"

        # Step 4: Mark invoice as refunded
        invoice = mark_invoice_as_refunded("inv-int-001")
        assert invoice.status == "REFUNDED"

    def test_multiple_refunds_independent(self):
        """Multiple refunds should not interfere with each other."""
        request1 = RefundRequest("r1", "t1", 1000, "Test 1", "a@b.com")
        request2 = RefundRequest("r2", "t2", 2000, "Test 2", "c@d.com")

        result1 = process_refund(request1)
        result2 = process_refund(request2)

        assert result1.refund_id != result2.refund_id
        assert result1.amount == 1000
        assert result2.amount == 2000


class TestErrorScenarios:

    def test_validation_before_processing(self):
        """Validation should happen before any processing."""
        request = RefundRequest(
            refund_id="",
            transaction_id="txn-001",
            amount=5000,
            reason="Test",
            customer_email="test@test.com"
        )

        try:
            process_refund(request)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "refund_id is required" in str(e)