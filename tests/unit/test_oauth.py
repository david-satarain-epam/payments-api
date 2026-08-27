"""
Unit tests for OAuth2 authentication logic.
"""

import pytest
from src.auth.oauth import exchange_code_for_token, validate_token


class TestOAuthExchange:

    def test_valid_code_returns_token(self, sample_oauth_config):
        """Valid auth code should return a token response."""
        result = exchange_code_for_token("valid-code", sample_oauth_config)

        assert result.access_token is not None
        assert result.token_type == "Bearer"
        assert result.expires_in == 3600
        assert result.refresh_token is not None

    def test_empty_code_raises_error(self, sample_oauth_config):
        """Empty authorization code should raise ValueError."""
        with pytest.raises(ValueError, match="Authorization code is required"):
            exchange_code_for_token("", sample_oauth_config)

    def test_token_starts_with_prefix(self, sample_oauth_config):
        """Access token should start with expected prefix."""
        result = exchange_code_for_token("code", sample_oauth_config)

        assert result.access_token.startswith("aegis-at-")

    def test_refresh_token_starts_with_prefix(self, sample_oauth_config):
        """Refresh token should start with expected prefix."""
        result = exchange_code_for_token("code", sample_oauth_config)

        assert result.refresh_token.startswith("aegis-rt-")


class TestTokenValidation:

    def test_valid_token_returns_true(self):
        """A valid token should return True."""
        assert validate_token("aegis-at-1234567890") is True

    def test_empty_token_returns_false(self):
        """Empty token should return False."""
        assert validate_token("") is False

    def test_invalid_prefix_returns_false(self):
        """Token with wrong prefix should return False."""
        assert validate_token("bearer-12345") is False