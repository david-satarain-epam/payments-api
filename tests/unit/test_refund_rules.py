"""
Unit tests for refund business rules.

Tests the core processing logic in isolation.
No database, no HTTP, no external services.
"""

import pytest
from src.payment.api import process_refund
from src.payment.schema import RefundRequest


class TestRefundProcessing:

    def test_valid_refund_succeeds(self, sample_refund_request):
        """A valid refund request should be processed successfully."""
        result = process_refund(sample_refund_request)

        assert result.refund_id == "ref-001"
        assert result.status.value == "PROCESSED"
        assert result.transaction_id == "txn-001"
        assert result.amount == 4999

    def test_missing_refund_id_raises_error(self, sample_refund_request):
        """Missing refund_id should raise ValueError."""
        sample_refund_request.refund_id = ""

        with pytest.raises(ValueError, match="refund_id is required"):
            process_refund(sample_refund_request)

    def test_missing_transaction_id_raises_error(self, sample_refund_request):
        """Missing transaction_id should raise ValueError."""
        sample_refund_request.transaction_id = ""

        with pytest.raises(ValueError, match="transaction_id is required"):
            process_refund(sample_refund_request)

    def test_negative_amount_raises_error(self, sample_refund_request):
        """Negative amount should raise ValueError."""
        sample_refund_request.amount = -100

        with pytest.raises(ValueError, match="amount must be greater than 0"):
            process_refund(sample_refund_request)

    def test_zero_amount_raises_error(self, sample_refund_request):
        """Zero amount should raise ValueError."""
        sample_refund_request.amount = 0

        with pytest.raises(ValueError, match="amount must be greater than 0"):
            process_refund(sample_refund_request)

    def test_refund_amount_is_preserved(self, sample_refund_request):
        """Refund amount in response should match request."""
        sample_refund_request.amount = 9999

        result = process_refund(sample_refund_request)

        assert result.amount == 9999

    def test_refund_creates_processed_at_timestamp(self, sample_refund_request):
        """Response should include a processed_at timestamp."""
        result = process_refund(sample_refund_request)

        assert result.processed_at is not None
        assert len(result.processed_at) > 0


class TestRefundValidation:

    def test_empty_refund_id_fails(self):
        """Empty string refund_id should fail."""
        request = RefundRequest(
            refund_id="",
            transaction_id="txn-001",
            amount=1000,
            reason="Test",
            customer_email="test@test.com"
        )

        with pytest.raises(ValueError):
            process_refund(request)

    def test_special_characters_in_refund_id(self, sample_refund_request):
        """Special characters should be fine as long as present."""
        sample_refund_request.refund_id = "ref-äöü-ñ-001"

        result = process_refund(sample_refund_request)

        assert result.refund_id == "ref-äöü-ñ-001"

    def test_large_amount_handled(self, sample_refund_request):
        """Very large amounts should be handled correctly."""
        sample_refund_request.amount = 999999999

        result = process_refund(sample_refund_request)

        assert result.amount == 999999999