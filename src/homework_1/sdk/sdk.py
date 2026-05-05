"""SDK Client module.

Implements the primary SDK entry point layer following section 4.1 architecture.
"""

import logging
from typing import Any, Dict, List

from homework_1.services import (
    SinusWave,
    generate_sinus_samples,
    sum_sinus_lists,
    sum_sinus_waves,
)
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
        """Processes input data safely via the API Gatekeeper to enforce rate limits."""

        def _execute_processing() -> Dict[str, Any]:
            if not raw_input:
                raise ValueError("Input data cannot be empty")
            return {"processed": True, "length": len(raw_input), "payload": raw_input.upper()}

        execution_envelope = self.gatekeeper.execute(_execute_processing)
        return execution_envelope

    def generate_samples(
        self,
        amplitude: float,
        frequency: float,
        phase: float,
        samples_per_second: int,
        seconds: float,
        noise_factor: float = 0.0,
    ) -> Dict[str, Any]:
        """Generates discrete sinus samples safely via the API Gatekeeper."""

        def _execute_generation() -> List[float]:
            return generate_sinus_samples(
                amplitude=amplitude,
                frequency=frequency,
                phase=phase,
                samples_per_second=samples_per_second,
                seconds=seconds,
                noise_factor=noise_factor,
            )

        return self.gatekeeper.execute(_execute_generation)

    def sum_samples(self, lists: List[List[float]]) -> Dict[str, Any]:
        """Sums matching lists of sinus samples safely via the API Gatekeeper."""

        def _execute_sum() -> List[float]:
            return sum_sinus_lists(lists)

        return self.gatekeeper.execute(_execute_sum)

    def sum_waves(
        self,
        waves: List[SinusWave],
        samples_per_second: int,
        seconds: float,
        noise_factor: float = 0.0,
    ) -> Dict[str, Any]:
        """Evaluates and sums waves mathematically safely via the API Gatekeeper."""

        def _execute_wave_sum() -> List[float]:
            return sum_sinus_waves(
                waves=waves,
                samples_per_second=samples_per_second,
                seconds=seconds,
                noise_factor=noise_factor,
            )

        return self.gatekeeper.execute(_execute_wave_sum)
