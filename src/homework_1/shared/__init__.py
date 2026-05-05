"""Shared utilities package.

Exposes cross-cutting tools like configurations, rate-limiters, and version control.
"""

from homework_1.shared.config import ConfigManager
from homework_1.shared.gatekeeper import ApiGatekeeper
from homework_1.shared.version import get_version

__all__ = [
    "ConfigManager",
    "ApiGatekeeper",
    "get_version",
]
