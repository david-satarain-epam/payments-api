"""
Contract test — OpenAPI schema validation.

Ensures the baseline OpenAPI spec is valid and complete.
In production, this would be run against every PR.
"""

import json
import pytest
from pathlib import Path


class TestOpenAPIBaseline:

    @pytest.fixture
    def baseline_spec(self):
        """Load the baseline OpenAPI spec."""
        path = Path(__file__).parent.parent.parent / "openapi" / "baseline.json"
        with open(path) as f:
            return json.load(f)

    def test_spec_has_valid_version(self, baseline_spec):
        """OpenAPI spec should have a valid version."""
        assert "openapi" in baseline_spec
        assert baseline_spec["openapi"] == "3.0.3"

    def test_spec_has_info(self, baseline_spec):
        """OpenAPI spec should have info section."""
        info = baseline_spec["info"]
        assert info["title"] == "Payment API"

    def test_spec_has_refund_endpoint(self, baseline_spec):
        """OpenAPI spec should define /refund endpoint."""
        paths = baseline_spec["paths"]
        assert "/refund" in paths
        assert "post" in paths["/refund"]

    def test_spec_has_health_endpoint(self, baseline_spec):
        """OpenAPI spec should define /health endpoint."""
        paths = baseline_spec["paths"]
        assert "/health" in paths

    def test_spec_defines_required_schemas(self, baseline_spec):
        """Schemas section should define RefundRequest and RefundResponse."""
        schemas = baseline_spec["components"]["schemas"]
        assert "RefundRequest" in schemas
        assert "RefundResponse" in schemas

    def test_refund_request_required_fields(self, baseline_spec):
        """RefundRequest should define required fields."""
        schema = baseline_spec["components"]["schemas"]["RefundRequest"]
        required = schema["required"]

        assert "refund_id" in required
        assert "transaction_id" in required
        assert "amount" in required
        assert "reason" in required
        assert "customer_email" in required

    def test_refund_response_status_enum(self, baseline_spec):
        """RefundResponse status should be an enum."""
        schema = baseline_spec["components"]["schemas"]["RefundResponse"]
        status_prop = schema["properties"]["status"]

        assert "enum" in status_prop
        assert "PENDING" in status_prop["enum"]
        assert "PROCESSED" in status_prop["enum"]
        assert "FAILED" in status_prop["enum"]