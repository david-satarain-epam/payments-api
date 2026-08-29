"""
Auth service — OAuth2 authentication.

TIER 1 service. Affects ALL consumers.
Changes here = total outage risk.
"""
# NUEVO
from enum import Enum
from typing import Optional

class OAuthProvider(str, Enum):
    GOOGLE = "GOOGLE"
    GITHUB = "GITHUB"
    MICROSOFT = "MICROSOFT"

@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    scope: List[str]
    provider: OAuthProvider              

@dataclass  
class PKCEParams:                        
    code_verifier: str
    code_challenge: str
    code_challenge_method: str = "S256"

def exchange_code_for_token(
    code: str, 
    config: OAuthConfig,
    pkce: Optional[PKCEParams] = None    
) -> TokenResponse:
    if pkce:
        if not pkce.code_verifier or not pkce.code_challenge:
            raise ValueError("PKCE verifier and challenge required")

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