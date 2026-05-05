"""Configuration manager module.

Loads application configuration from JSON files and environment variables.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """Handles loading, parsing, and retrieving configurations and secrets."""

    def __init__(self, config_dir: Optional[Path] = None):
        if config_dir is None:
            # Default to looking in project-root/config/
            self.config_dir = Path(__file__).resolve().parents[3] / "config"
        else:
            self.config_dir = Path(config_dir)

        self._setup_config: Dict[str, Any] = {}
        self._rate_limits_config: Dict[str, Any] = {}
        self._load_configs()

    def _load_configs(self) -> None:
        """Safely reads JSON configurations from disk."""
        setup_path = self.config_dir / "setup.json"
        rate_limits_path = self.config_dir / "rate_limits.json"

        if setup_path.exists():
            with open(setup_path, "r", encoding="utf-8") as f:
                self._setup_config = json.load(f)

        if rate_limits_path.exists():
            with open(rate_limits_path, "r", encoding="utf-8") as f:
                self._rate_limits_config = json.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve setup config value."""
        return self._setup_config.get(key, default)

    def get_rate_limits(self) -> Dict[str, Any]:
        """Retrieve loaded rate limits structure."""
        return self._rate_limits_config

    def get_secret(self, name: str, default: Optional[str] = None) -> Optional[str]:
        """Retrieve secret credentials strictly from environment variables.

        This follows section 7.4 to ensure secrets are never embedded in the code.
        """
        return os.environ.get(name, default)
