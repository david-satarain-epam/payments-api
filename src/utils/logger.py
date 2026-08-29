"""
Structured logging utility.
Outputs JSON-formatted logs for Cloud Logging compatibility.
"""

from dataclasses import asdict
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"

# NUEVO: structured Cloud Logging format
@dataclass
class LogEntry:
    severity: str
    message: str
    timestamp: str
    source: str = "payment-api"
    data: Optional[dict] = None

def log(level: LogLevel, message: str, data: Optional[dict] = None) -> None:
    entry = LogEntry(
        severity=level.value,
        message=message,
        timestamp=datetime.now(timezone.utc).isoformat(),
        data=data,
    )
    print(json.dumps(asdict(entry)))


def log(level: LogLevel, message: str, data: Optional[dict] = None) -> None:
    """Emit a structured log entry."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "severity": level.value,
        "message": message,
        "source": "payment-api",
    }
    if data:
        entry["data"] = data
    print(json.dumps(entry))


def debug(message: str, data: Optional[dict] = None) -> None:
    log(LogLevel.DEBUG, message, data)


def info(message: str, data: Optional[dict] = None) -> None:
    log(LogLevel.INFO, message, data)


def warn(message: str, data: Optional[dict] = None) -> None:
    log(LogLevel.WARN, message, data)


def error(message: str, data: Optional[dict] = None) -> None:
    log(LogLevel.ERROR, message, data)