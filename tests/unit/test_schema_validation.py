"""
Unit tests for Payment API schemas.

Validates dataclass creation, field defaults,
and enum behavior.
"""

import pytest
from src.payment.schema import (
    RefundRequest,
    RefundResponse,
    RefundStatus,
    BatchRefundRequest,
    BatchRefundResponse,
    Currency,
)


class TestRefundRequestSchema:

    def test_create_valid_refund_request(self):
        """Should create a RefundRequest with all required fields."""
        request = RefundRequest(
            refund_id="ref-001",
            transaction_id="txn-001",
            amount=4999,
            reason="Test refund",
            customer_email="test@example.com"
        )

        assert request.refund_id == "ref-001"
        assert request.amount == 4999

    def test_refund_request_is_dataclass(self):
        """RefundRequest should be a dataclass."""
        request = RefundRequest(
            refund_id="ref-001",
            transaction_id="txn-001",
            amount=1000,
            reason="Test",
            customer_email="test@test.com"
        )

        assert hasattr(request, "__dataclass_fields__")


class TestRefundStatus:

    def test_valid_statuses(self):
        """All defined statuses should be accessible."""
        assert RefundStatus.PENDING.value == "PENDING"
        assert RefundStatus.PROCESSED.value == "PROCESSED"
        assert RefundStatus.FAILED.value == "FAILED"


class TestBatchRefundSchema:

    def test_create_batch_request(self):
        """Should create a BatchRefundRequest."""
        refunds = [
            RefundRequest("r1", "t1", 1000, "Test", "a@b.com"),
            RefundRequest("r2", "t2", 2000, "Test", "c@d.com"),
        ]

        batch = BatchRefundRequest(refunds=refunds, mode="SEQUENTIAL")

        assert batch.total_refunds == 2
        assert batch.mode == "SEQUENTIAL"


class TestCurrencyEnum:

    def test_currency_values(self):
        """Currency enum should have expected values."""
        assert Currency.USD.value == "USD"
        assert Currency.EUR.value == "EUR"
        assert Currency.MXN.value == "MXN"