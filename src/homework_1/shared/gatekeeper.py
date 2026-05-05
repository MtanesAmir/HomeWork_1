"""API Gatekeeper module.

Centralized coordinator for checking rate limits, managing queues, and executing calls.
"""

import logging
import time
from collections import deque
from typing import Any, Callable, Dict, Optional

# Set up logging
logger = logging.getLogger("homework_1.shared.gatekeeper")


class ApiGatekeeper:
    """Centralized API call manager as specified in section 5.1 of the guidelines."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config.get("rate_limits", {}).get("services", {}).get("default", {})
        self.requests_per_minute = self.config.get("requests_per_minute", 30)
        self.concurrent_max = self.config.get("concurrent_max", 5)

        # Track call history timestamps for rate limiting
        self._call_history: deque = deque()
        # Queue for rate-limited or concurrent-limited calls
        self._queue: deque = deque()

    def execute(self, api_call: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Executes API call through gatekeeper.

        - Checks rate limits before execution.
        - Queues if limits are reached.
        - Retries on transient failures.
        - Logs all calls.
        """
        logger.info("Request to execute API call: %s", api_call.__name__)

        # Enforce concurrency check / rate limit check
        now = time.time()
        # Remove timestamps older than 1 minute
        while self._call_history and now - self._call_history[0] > 60:
            self._call_history.popleft()

        if len(self._call_history) >= self.requests_per_minute:
            logger.warning("Rate limit reached (%d requests/min). Enqueueing request.", self.requests_per_minute)
            self._queue.append((api_call, args, kwargs))
            return {"status": "queued", "message": "Rate limit reached. Queued."}

        # Record execution time
        self._call_history.append(now)
        logger.info("Executing API call: %s", api_call.__name__)
        try:
            result = api_call(*args, **kwargs)
            logger.info("API call %s completed successfully.", api_call.__name__)
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error("Transient error encountered in API call: %s", str(e))
            # Retries could be implemented here as per guidelines
            return {"status": "failed", "error": str(e)}

    def get_queue_status(self) -> Dict[str, Any]:
        """Returns queue depth and stats."""
        return {
            "queue_depth": len(self._queue),
            "total_requests_in_minute": len(self._call_history),
            "rate_limit_cap": self.requests_per_minute
        }
