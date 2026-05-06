"""Unit tests for the Dataset Generator Engine.

Validates configuration parsing, prepared signals dimension shapes, row dimension synthesis,
JSON disk serialization, and architectural line limits constraints.
"""

import json
from pathlib import Path

from homework_1.services.generator import (
    generate_dataset,
    prepare_base_signals,
    save_dataset,
)
from homework_1.shared.config import ConfigManager


def test_generator_config_loading() -> None:
    """Validates that ConfigManager parses new wave profiles and storage paths correctly."""
    config = ConfigManager()
    waves = config.get("waves", [])
    output_path = config.get("dataset_output_path", "")

    assert len(waves) == 4
    assert output_path == "results/dataset.json"

    # Verify wave profile keys are correctly set
    for w in waves:
        assert "amplitude" in w
        assert "frequency" in w
        assert "phase" in w


def test_generator_base_signals_shape() -> None:
    """Validates that prepare_base_signals outputs 10 lists of exactly 10K float samples."""
    signals = prepare_base_signals(noise_factor=0.05)

    assert "clean_waves" in signals
    assert "clean_sum" in signals
    assert "noised_waves" in signals
    assert "noised_sum" in signals

    assert len(signals["clean_waves"]) == 4
    assert len(signals["noised_waves"]) == 4

    # Ensure each base wave has size 10,000
    for wave in signals["clean_waves"]:
        assert len(wave) == 10000
    for wave in signals["noised_waves"]:
        assert len(wave) == 10000

    assert len(signals["clean_sum"]) == 10000
    assert len(signals["noised_sum"]) == 10000


def test_generator_dataset_row_dimensions() -> None:
    """Validates synthesized dataset rows dimension and selector one-hot vector integrity."""
    dataset_map = generate_dataset(num_rows=50, noise_factor=0.05)
    assert "dataset" in dataset_map

    rows = dataset_map["dataset"]
    assert len(rows) == 50

    for row in rows:
        assert "key" in row
        assert "value" in row

        key = row["key"]
        value = row["value"]

        # Key must have size 14, Value must have size 10
        assert len(key) == 14
        assert len(value) == 10

        # One-hot selector checks (first 4 indices of Key)
        one_hot = key[:4]
        assert sum(one_hot) == 1.0
        assert one_hot.count(1.0) == 1
        assert one_hot.count(0.0) == 3


def test_generator_save_dataset(tmp_path: Path) -> None:
    """Validates that save_dataset successfully serializes and writes a parseable JSON to disk."""
    test_db = {"dataset": [{"key": [1.0, 0.0, 0.0, 0.0] + [0.5] * 10, "value": [0.2] * 10}]}
    target_file = tmp_path / "test_results" / "db.json"

    save_dataset(test_db, str(target_file))
    assert target_file.exists()

    with open(target_file, "r", encoding="utf-8") as f:
        loaded_db = json.load(f)

    assert loaded_db == test_db


def test_line_limit_generator_file() -> None:
    """Asserts that src/homework_1/services/generator.py strictly stays below 150 logical lines of code."""
    gen_path = Path(__file__).resolve().parents[2] / "src" / "homework_1" / "services" / "generator.py"
    assert gen_path.exists()

    with open(gen_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    logical_code_lines = 0
    for line in lines:
        stripped = line.strip()
        # Skip empty lines and lines that are entirely comments
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        logical_code_lines += 1

    print(f"Logical code line count of generator.py: {logical_code_lines}")
    # Strictly stays below the 150-line limit
    assert logical_code_lines <= 150


def test_sdk_dataset_generation_pipeline() -> None:
    """Validates E2E SDK execution, Gatekeeper protection, and serialization to configured path."""
    from homework_1.sdk import HomeWorkSDK

    sdk = HomeWorkSDK()
    output_path = sdk.config_manager.get("dataset_output_path", "results/dataset.json")
    target_file = Path(output_path)

    # Clean up any existing database
    if target_file.exists():
        target_file.unlink()

    resp = sdk.generate_and_save_dataset(num_rows=15, noise_factor=0.02)
    assert resp["status"] == "success"
    assert resp["result"]["rows_generated"] == 15
    assert resp["result"]["saved_to"] == output_path

    assert target_file.exists()

    # Verify file is valid and has correct quantity
    with open(target_file, "r", encoding="utf-8") as f:
        db = json.load(f)

    assert len(db["dataset"]) == 15

    # Clean up
    if target_file.exists():
        target_file.unlink()

