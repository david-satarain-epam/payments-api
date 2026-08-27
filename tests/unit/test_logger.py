"""
Unit tests for structured logging utility.
"""

import json
from src.utils.logger import log, LogLevel, debug, info, warn, error


class TestStructuredLogging:

    def test_log_emits_json(self, capsys):
        """Log should output valid JSON."""
        log(LogLevel.INFO, "Test message")

        captured = capsys.readouterr()
        entry = json.loads(captured.out.strip())

        assert entry["severity"] == "INFO"
        assert entry["message"] == "Test message"
        assert entry["source"] == "payment-api"
        assert "timestamp" in entry

    def test_log_with_data(self, capsys):
        """Log with extra data should include it."""
        log(LogLevel.ERROR, "Something broke", {"error_code": 500})

        captured = capsys.readouterr()
        entry = json.loads(captured.out.strip())

        assert entry["severity"] == "ERROR"
        assert entry["data"]["error_code"] == 500

    def test_debug_helper(self, capsys):
        """Debug helper should emit DEBUG level."""
        debug("Debug info")
        captured = capsys.readouterr()
        entry = json.loads(captured.out.strip())
        assert entry["severity"] == "DEBUG"

    def test_info_helper(self, capsys):
        """Info helper should emit INFO level."""
        info("Info message")
        captured = capsys.readouterr()
        entry = json.loads(captured.out.strip())
        assert entry["severity"] == "INFO"

    def test_warn_helper(self, capsys):
        """Warn helper should emit WARN level."""
        warn("Warning message")
        captured = capsys.readouterr()
        entry = json.loads(captured.out.strip())
        assert entry["severity"] == "WARN"

    def test_error_helper(self, capsys):
        """Error helper should emit ERROR level."""
        error("Error message")
        captured = capsys.readouterr()
        entry = json.loads(captured.out.strip())
        assert entry["severity"] == "ERROR"

    def test_log_level_enum(self):
        """LogLevel should have expected values."""
        assert LogLevel.DEBUG.value == "DEBUG"
        assert LogLevel.INFO.value == "INFO"
        assert LogLevel.WARN.value == "WARN"
        assert LogLevel.ERROR.value == "ERROR"

    def test_timestamp_is_iso_format(self, capsys):
        """Timestamp should be ISO 8601."""
        info("test")
        captured = capsys.readouterr()
        entry = json.loads(captured.out.strip())

        # ISO 8601: should contain T and end with Z or +00:00
        assert "T" in entry["timestamp"]