# Payment API 

## Overview

**Payment API** is a demo microservice. It simulates a real-world payment processing system.

The service exposes endpoints for processing refunds (single and batch), managing authentication, sending notifications, and handling billing invoices. It is used by internal services (checkout-web, mobile-app, merchant-portal) and 7 external clients via API Gateway.

---

## Architecture

payment-api/
- app.py: Flask application entry point
- requirements.txt: Python dependencies
- Dockerfile: Cloud Run deployment
- pytest.ini: Test runner configuration
- .gitignore
- README.md
- src/ (Source code)
  - payment/ (TIER 1 — Core payment processing)
    - __init__.py
    - schema.py: Data models, enums, type definitions
    - api.py: Single refund processing logic
    - batch_refund.py: Batch refund endpoint (NEW in PR #852)
  - billing/ (TIER 2 — Invoice management)
    - __init__.py
    - invoice.py: Invoice lifecycle (PAID → REFUNDED)
  - auth/ (TIER 1 — Authentication & SSO)
    - __init__.py
    - oauth.py: OAuth2 token exchange & validation
    - token.py: Token refresh & revocation
  - notifications/ (TIER 3 — Email & push)
    - template.html: Email notification templates
  - utils/ (Shared utilities)
    - __init__.py
    - logger.py: Structured JSON logging
- governance/ (Business rules - consumed by Aegis)
  - __init__.py
  - contract_diff.py: OpenAPI contract comparator
  - test-impact-map.yaml: Test catalog & strategy mapping
  - risk-policy.yaml: Deterministic risk scoring rules
- openapi/ (API specifications)
  - baseline.json: Current approved spec (v2.2.0)
  - pr847-proposed.json: Proposed changes (PR #847 / v2.3.0)
- tests/ (Test suite - 46 tests)
  - __init__.py
  - conftest.py: Shared fixtures & mock data
  - unit/ (32 unit tests)
    - __init__.py
    - test_refund_rules.py: Refund business logic (7 tests)
    - test_schema_validation.py: Data model validation (5 tests)
    - test_oauth.py: OAuth2 authentication (6 tests)
    - test_token.py: Token lifecycle (3 tests)
    - test_logger.py: Structured logging (8 tests)
    - test_invoice.py: Invoice management (3 tests)
  - integration/ (3 integration tests)
    - __init__.py
    - test_payment_api.py: End-to-end refund flow
  - contract/ (7 contract tests)
    - __init__.py
    - test_openapi_schema.py: OpenAPI spec validation
  - smoke/ (4 smoke tests)
    - __init__.py
    - test_health.py: Quick health & import checks

---

## Service Hierarchy (TIER Levels)

| Service | TIER | Max Downtime | Consumers | Criticality |
|---------|------|-------------|-----------|-------------|
| **payment-api** | 1 | 0 minutes | 12 (5 internal + 7 external) | Core payment processing. Breaks here = money stops. |
| **auth-service** | 1 | 0 minutes | All services | Authentication. Breaks here = nobody logs in. |
| **notification-service** | 3 | 30 minutes | 2 | Non-critical. Asynchronous. Graceful degradation OK. |

---

## Endpoints

| Method | Path | Description | Status |
|--------|------|-------------|--------|
| `GET` | `/` | Service info | Active |
| `GET` | `/health` | Health check | Active |
| `POST` | `/refund` | Process single refund | Active |
| `POST` | `/refund/batch` | Process batch refund | **NEW — PR #852** |
| `POST` | `/auth/token` | OAuth2 token exchange | Active |

---

## Demo PR Scenarios

Six pull requests demonstrate analysis capabilities:

| PR | Branch | Description | Risk | Decision | Strategy |
|----|--------|-------------|------|----------|----------|
| **#847** | `pr/847-update-refund` | Add partial refund support & change amount type to decimal | **HIGH** | ROLLOUT | CANARY |
| **#848** | `pr/848-fix-notification` | Fix typo in email template | **LOW** | APPROVE | DIRECT |
| **#849** | `pr/849-add-oauth2` | Add multi-provider OAuth2 + PKCE support | **HIGH** | ROLLOUT | CANARY |
| **#850** | `pr/850-refactor-logger` | Refactor logger for structured Cloud Logging format | **LOW** | APPROVE | DIRECT |
| **#851** | `pr/851-schema-v2` | Add multi-currency support (new required `currency` field) | **CRITICAL** | POSTPONE | NONE |
| **#852** | `pr/852-batch-refund` | Add batch refund endpoint — **zero test coverage** | **CRITICAL** | POSTPONE | NONE + 8 suggested tests |

---

## Governance Module

The `governance/` directory is the most critical part of this demo. It contains business logic that ADK Agent directly consumes.

### `contract_diff.py`

Compares two OpenAPI specifications and identifies breaking changes, new fields, and deprecated elements. Used by ADK Agent' **Impact Context MCP Server** via the `compare_api_contracts()` tool.

```bash
python -c "
from governance.contract_diff import compare_contracts
import json

result = compare_contracts(
    'openapi/baseline.json',
    'openapi/pr847-proposed.json'
)
print(json.dumps(result, indent=2))
"
```

#### Example output:

{
  "has_breaking_change": true,
  "breaking_changes": [
    {
      "type": "TYPE_CHANGED",
      "path": "RefundRequest.amount",
      "detail": "Type changed from integer to number"
    }
  ],
  "new_fields": [
    {
      "type": "ADDED",
      "path": "RefundRequest.properties.partial_refund_amount",
      "detail": "'partial_refund_amount' was added"
    }
  ],
  "deprecated": [],
  "total_changes": 2,
  "baseline": "openapi/baseline.json",
  "proposed": "openapi/pr847-proposed.json"
}

### test-impact-map.yaml
Defines which test categories are required based on risk level and service criticality. Used by ADK Agent to generate targeted test plans.


### risk-policy.yaml
Deterministic risk scoring rules. Maps file paths to minimum risk levels, defines escalation conditions, and specifies monitoring thresholds. Used by the Change Impact Agent (ADK) for risk calculation.

## Test Suite
### Test Categories
| Category | Count | Purpose | Run Time |
|----------|-------|---------|----------|
| **Unit** | 32 | Isolated business logic | &lt; 1s |
| **Integration** | 3 | Multi-module workflows | &lt; 1s |
| **Contract** | 7 | OpenAPI schema validation | &lt; 1s |
| **Smoke** | 4 | Quick health checks | &lt; 2s |
| **Total** | **46** | | **&lt; 5s** |

## Run Tests
### Install dependencies
pip install -r requirements.txt

### Run all tests
pytest

### Run specific categories
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/contract/ -v
pytest tests/smoke/ -v

### Run with coverage
pytest --cov=src --cov=governance --cov-report=term

## Quick Start
### Local Development

#### 1. Clone the repository
git clone https://github.com/your-org/payment-api.git
cd payment-api

#### 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

#### 3. Install dependencies
pip install -r requirements.txt

#### 4. Run the app
python app.py
##### → http://localhost:8080
##### → http://localhost:8080/health

#### 5. Test the governance module
python -c "
from governance.contract_diff import compare_contracts
import json
result = compare_contracts('openapi/baseline.json', 'openapi/pr847-proposed.json')
print(json.dumps(result, indent=2))
"

#### 6. Run tests
pytest

## Deploy to Cloud Run

### Build and deploy
gcloud run deploy payment-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated

### Test the deployed service
curl https://payment-api-xxxxx-uc.a.run.app/health

## Tech Stack
| Technology | Purpose |
|------------|---------|
| **Python 3.13** | Runtime |
| **Flask 3.0** | Web framework (minimal — health check only) |
| **pytest 8.0** | Test framework |
| **PyYAML 6.0** | YAML parsing (governance configs) |
| **DeepDiff 7.0** | OpenAPI contract comparison |
| **Docker** | Containerization |
| **Cloud Run** | Deployment target |

## License
MIT — Built for Demo purposes.