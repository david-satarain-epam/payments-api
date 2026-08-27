"""
Shared test fixtures for Aegis demo.

Provides test data and mock objects used across
all test categories.
"""

import pytest
from datetime import datetime, timezone


@pytest.fixture
def sample_refund_request():
    """Standard refund request for testing."""
    from src.payment.schema import RefundRequest
    return RefundRequest(
        refund_id="ref-001",
        transaction_id="txn-001",
        amount=4999,
        reason="Customer request",
        customer_email="customer@example.com"
    )


@pytest.fixture
def sample_invoice():
    """Standard invoice for testing."""
    return {
        "invoice_id": "inv-001",
        "transaction_id": "txn-001",
        "amount": 4999,
        "status": "PAID",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@pytest.fixture
def sample_oauth_config():
    """Standard OAuth2 config for testing."""
    from src.auth.oauth import OAuthConfig
    return OAuthConfig(
        client_id="test-client-id",
        client_secret="test-client-secret",
        redirect_uri="http://localhost/callback",
        scope=["read", "write"]
    )