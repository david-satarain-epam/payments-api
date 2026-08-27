"""
Smoke test — Quick health validation.

Should run in under 10 seconds.
Fails fast if core functionality is broken.
"""

import pytest
from src.payment.schema import RefundRequest
from src.payment.api import process_refund


class TestSmoke:

    def test_app_imports(self):
        """Core modules should be importable."""
        # If any of these fail, something is seriously wrong
        from src.payment import api, schema
        from src.billing import invoice
        from src.auth import oauth, token
        from src.utils import logger

    def test_basic_refund_works(self):
        """Most basic refund should succeed — if this fails, nothing works."""
        request = RefundRequest(
            refund_id="smoke-test-001",
            transaction_id="smoke-txn-001",
            amount=100,
            reason="Smoke test",
            customer_email="smoke@test.com"
        )

        result = process_refund(request)

        assert result.status.value == "PROCESSED"
        assert result.refund_id == "smoke-test-001"

    def test_governance_imports(self):
        """Governance module should be importable."""
        from governance import contract_diff
        from governance.contract_diff import compare_contracts

    def test_contract_diff_baseline(self):
        """Contract diff against itself should return zero changes."""
        from governance.contract_diff import compare_contracts

        import os
        baseline = os.path.join(
            os.path.dirname(__file__), "..", "..", "openapi", "baseline.json"
        )

        result = compare_contracts(baseline, baseline)

        assert result["has_breaking_change"] is False
        assert result["total_changes"] == 0