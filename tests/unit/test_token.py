"""
Unit tests for token lifecycle management.
"""

import pytest
from src.auth.token import refresh_access_token, revoke_token


class TestTokenRefresh:

    def test_valid_refresh_returns_new_token(self, sample_oauth_config):
        """Valid refresh token should return new tokens."""
        result = refresh_access_token("valid-refresh-token", sample_oauth_config)

        assert result.access_token is not None
        assert result.refresh_token is not None
        assert result.expires_in == 3600

    def test_empty_refresh_raises_error(self, sample_oauth_config):
        """Empty refresh token should raise ValueError."""
        with pytest.raises(ValueError, match="Refresh token is required"):
            refresh_access_token("", sample_oauth_config)


class TestTokenRevocation:

    def test_revoke_returns_true(self):
        """Token revocation should return True."""
        result = revoke_token("aegis-at-1234567890")
        assert result is True