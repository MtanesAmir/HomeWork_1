"""SDK Client module.

Implements the primary SDK entry point layer following section 4.1 architecture.
"""

import logging
from typing import Any, Dict

from homework_1.shared.config import ConfigManager
from homework_1.shared.gatekeeper import ApiGatekeeper
from homework_1.shared.version import get_version

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("homework_1.sdk")


class HomeWorkSDK:
    """The primary SDK controller acting as the single entry point for all logic."""

    def __init__(self) -> None:
        logger.info("Initializing HomeWorkSDK version %s", get_version())
        self.config_manager = ConfigManager()
        self.gatekeeper = ApiGatekeeper(self.config_manager.get_rate_limits())

    def get_sdk_version(self) -> str:
        """Retrieves the version of the SDK."""
        return get_version()

    def process_data(self, raw_input: str) -> Dict[str, Any]:
        """Processes input data safely via the API Gatekeeper to enforce rate limits.

        Conforms to Building Blocks specifications from Section 16.
        """

        # Define the actual target function to execute under rate-limiting safety
        def _execute_processing() -> Dict[str, Any]:
            if not raw_input:
                raise ValueError("Input data cannot be empty")
            # Simple business logic simulation
            return {
                "processed": True,
                "length": len(raw_input),
                "payload": raw_input.upper()
            }

        # Run through the gatekeeper
        execution_envelope = self.gatekeeper.execute(_execute_processing)
        return execution_envelope
