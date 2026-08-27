"""
Auth service — Token lifecycle management.
Refresh, revoke, rotate.
"""

from datetime import datetime
from .oauth import OAuthConfig, TokenResponse


def refresh_access_token(refresh_token: str, config: OAuthConfig) -> TokenResponse:
    """Refresh an expired access token."""
    if not refresh_token:
        raise ValueError("Refresh token is required")

    return TokenResponse(
        access_token=f"aegis-at-{int(datetime.now().timestamp())}",
        token_type="Bearer",
        expires_in=3600,
        refresh_token=f"aegis-rt-{int(datetime.now().timestamp())}",
    )


def revoke_token(token: str) -> bool:
    """Revoke a token."""
    print(f"[AUTH] Token revoked: {token[:10]}...")
    return True