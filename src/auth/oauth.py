"""
Auth service — OAuth2 authentication.

TIER 1 service. Affects ALL consumers.
Changes here = total outage risk.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    scope: List[str]


@dataclass
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str


def exchange_code_for_token(code: str, config: OAuthConfig) -> TokenResponse:
    """Exchange OAuth2 authorization code for access token."""
    if not code:
        raise ValueError("Authorization code is required")

    return TokenResponse(
        access_token=f"aegis-at-{int(datetime.now().timestamp())}",
        token_type="Bearer",
        expires_in=3600,
        refresh_token=f"aegis-rt-{int(datetime.now().timestamp())}",
    )


def validate_token(token: str) -> bool:
    """Validate an access token."""
    if not token or not token.startswith("aegis-at-"):
        return False
    return True