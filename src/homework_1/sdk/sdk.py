"""SDK Client module.

Implements the primary SDK entry point layer following section 4.1 architecture.
"""

import logging
from typing import Any, Dict, List

from homework_1.services import (
    FCNModel,
    LSTMModel,
    RNNModel,
    SinusWave,
    generate_dataset,
    generate_sinus_samples,
    save_dataset,
    sum_sinus_lists,
    sum_sinus_waves,
    train_neural_network,
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

    def _get_or_create_dataset(self) -> List[Dict[str, Any]]:
        """Helper to retrieve or dynamically generate base dataset."""
        import json
        from pathlib import Path

        output_path = self.config_manager.get("dataset_output_path", "results/dataset.json")
        path = Path(output_path)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                db = json.load(f)
            return db.get("dataset", [])
        # Dynamically generate 100 rows if file not found
        dataset_resp = generate_dataset(num_rows=100, noise_factor=0.05)
        return dataset_resp["dataset"]

    def train_fcn(self) -> Dict[str, Any]:
        """Trains the Fully Connected Network safely via the Gatekeeper."""

        def _execute_fcn_train() -> Dict[str, Any]:
            dataset = self._get_or_create_dataset()
            model_cfg = self.config_manager.get("models", {})
            epochs = model_cfg.get("epochs", 50)
            hidden = model_cfg.get("hidden_layers", [3, 5, 3])
            train_pct = model_cfg.get("train_percentage", 70.0)
            val_pct = model_cfg.get("val_percentage", 15.0)
            test_pct = model_cfg.get("test_percentage", 15.0)

            model = FCNModel(input_size=14, hidden_layers=hidden, output_size=10)
            history = train_neural_network(
                model=model,
                dataset=dataset,
                epochs=epochs,
                train_pct=train_pct,
                val_pct=val_pct,
                test_pct=test_pct,
            )
            return {"model_type": "FCN", "history": history}

        return self.gatekeeper.execute(_execute_fcn_train)

    def train_rnn(self) -> Dict[str, Any]:
        """Trains the Recurrent Neural Network safely via the Gatekeeper."""

        def _execute_rnn_train() -> Dict[str, Any]:
            dataset = self._get_or_create_dataset()
            model_cfg = self.config_manager.get("models", {})
            epochs = model_cfg.get("epochs", 50)
            train_pct = model_cfg.get("train_percentage", 70.0)
            val_pct = model_cfg.get("val_percentage", 15.0)
            test_pct = model_cfg.get("test_percentage", 15.0)

            model = RNNModel(input_size=5, hidden_size=8, output_size=1)
            history = train_neural_network(
                model=model,
                dataset=dataset,
                epochs=epochs,
                train_pct=train_pct,
                val_pct=val_pct,
                test_pct=test_pct,
            )
            return {"model_type": "RNN", "history": history}

        return self.gatekeeper.execute(_execute_rnn_train)

    def train_lstm(self) -> Dict[str, Any]:
        """Trains the Long Short-Term Memory safely via the Gatekeeper."""

        def _execute_lstm_train() -> Dict[str, Any]:
            dataset = self._get_or_create_dataset()
            model_cfg = self.config_manager.get("models", {})
            epochs = model_cfg.get("epochs", 50)
            train_pct = model_cfg.get("train_percentage", 70.0)
            val_pct = model_cfg.get("val_percentage", 15.0)
            test_pct = model_cfg.get("test_percentage", 15.0)

            model = LSTMModel(input_size=5, hidden_size=6, output_size=1)
            history = train_neural_network(
                model=model,
                dataset=dataset,
                epochs=epochs,
                train_pct=train_pct,
                val_pct=val_pct,
                test_pct=test_pct,
            )
            return {"model_type": "LSTM", "history": history}

        return self.gatekeeper.execute(_execute_lstm_train)

    def generate_and_save_dataset(self, num_rows: int, noise_factor: float) -> Dict[str, Any]:
        """Generates the labeled dataset and saves it to disk safely via the Gatekeeper."""

        def _execute_pipeline() -> Dict[str, Any]:
            output_path = self.config_manager.get("dataset_output_path", "results/dataset.json")
            dataset = generate_dataset(num_rows=num_rows, noise_factor=noise_factor)
            save_dataset(dataset, output_path)
            return {
                "rows_generated": num_rows,
                "saved_to": output_path,
                "status": "completed",
            }

        return self.gatekeeper.execute(_execute_pipeline)
