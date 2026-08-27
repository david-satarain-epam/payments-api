"""
Unit tests for billing invoice management.
"""

import pytest
from src.billing.invoice import mark_invoice_as_refunded, get_invoice, Invoice


class TestInvoiceRefund:

    def test_mark_as_refunded_changes_status(self):
        """Marking invoice as refunded should set status to REFUNDED."""
        invoice = mark_invoice_as_refunded("inv-001")

        assert invoice.status == "REFUNDED"
        assert invoice.invoice_id == "inv-001"
        assert invoice.amount == 0

    def test_refunded_invoice_has_timestamp(self):
        """Refunded invoice should have updated_at set."""
        invoice = mark_invoice_as_refunded("inv-002")

        assert invoice.updated_at is not None


class TestGetInvoice:

    def test_get_invoice_returns_data(self):
        """get_invoice should return an Invoice."""
        invoice = get_invoice("inv-001")

        assert invoice is not None
        assert invoice.invoice_id == "inv-001"
        assert invoice.status == "PAID"