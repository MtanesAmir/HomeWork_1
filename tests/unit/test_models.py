"""Unit tests for the Deep Learning Models Engine.

Validates dynamic hidden layers constructor assertions, periodic training loop
loss reduction, splits validations warn printing, and logical line constraints.
"""

import io
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest
from homework_1.services import (
    FCNModel,
    LSTMModel,
    RNNModel,
)
from homework_1.services.models.trainer import (
    evaluate_loss,
    partition_dataset,
    train_neural_network,
    validate_splits,
)


def test_models_splits_warning() -> None:
    """Validates that validate_splits outputs a prominent warning to stdout if sum != 100.0."""
    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        # Splits summing to 90%
        res = validate_splits(70.0, 10.0, 10.0)
        assert res is False

        output_str = captured_output.getvalue()
        assert "WARNING" in output_str
        assert "not exactly 100%" in output_str
    finally:
        # Restore stdout
        sys.stdout = sys.__stdout__


def test_models_fcn_layer_shapes() -> None:
    """Validates that FCNModel dynamically builds weights and layers matching configured hidden profiles in PyTorch."""
    hidden_layers = [4, 8, 4]
    model = FCNModel(input_size=14, hidden_layers=hidden_layers, output_size=10)

    # In our PyTorch sequential network, linear layers reside at indices 0, 2, 4, 6
    layers = [model.network[idx] for idx in [0, 2, 4, 6]]
    assert len(layers) == 4

    # Matrix dimensions check: weight shape is (out_features, in_features)
    assert layers[0].weight.shape == (4, 14)
    assert layers[1].weight.shape == (8, 4)
    assert layers[2].weight.shape == (4, 8)
    assert layers[3].weight.shape == (10, 4)


def test_models_training_decrease_fcn() -> None:
    """Validates that training FCN on a synthetic dataset successfully converges and reduces loss."""
    # Generate a dummy dataset: key (14), target (10)
    dummy_dataset = []
    for _ in range(10):
        dummy_dataset.append({"key": [1.0] * 14, "value": [0.5] * 10})

    model = FCNModel(input_size=14, hidden_layers=[4], output_size=10)

    # Initial loss
    initial_loss = sum(
        sum((p - 0.5) ** 2 for p in model.get_prediction(row["key"])) / 10
        for row in dummy_dataset
    ) / 10

    # Train for 15 epochs
    history = train_neural_network(
        model=model,
        dataset=dummy_dataset,
        epochs=15,
        train_pct=80.0,
        val_pct=10.0,
        test_pct=10.0,
        learning_rate=0.2,
    )

    final_loss = history["train_loss"][-1]
    print(f"FCN Loss reduction: {initial_loss:.5f} -> {final_loss:.5f}")
    # Assert loss decreased
    assert final_loss < initial_loss


def test_models_training_decrease_rnn() -> None:
    """Validates that training RNN on a sequence dataset successfully converges and reduces loss."""
    dummy_dataset = []
    for _ in range(10):
        dummy_dataset.append({"key": [1.0] * 14, "value": [0.5] * 10})

    model = RNNModel(input_size=5, hidden_layers=[6], output_size=1)

    # Initial loss
    initial_loss = sum(
        sum((p - 0.5) ** 2 for p in model.get_prediction(row["key"])) / 10
        for row in dummy_dataset
    ) / 10

    # Train for 15 epochs
    history = train_neural_network(
        model=model,
        dataset=dummy_dataset,
        epochs=15,
        train_pct=80.0,
        val_pct=10.0,
        test_pct=10.0,
        learning_rate=0.01,
    )

    final_loss = history["train_loss"][-1]
    print(f"RNN Loss reduction: {initial_loss:.5f} -> {final_loss:.5f}")
    assert final_loss < initial_loss


def test_models_training_decrease_lstm() -> None:
    """Validates that training LSTM on a sequence dataset successfully converges and reduces loss."""
    dummy_dataset = []
    for _ in range(10):
        dummy_dataset.append({"key": [1.0] * 14, "value": [0.5] * 10})

    model = LSTMModel(input_size=5, hidden_layers=[6], output_size=1)

    # Initial loss
    initial_loss = sum(
        sum((p - 0.5) ** 2 for p in model.get_prediction(row["key"])) / 10
        for row in dummy_dataset
    ) / 10

    # Train for 15 epochs
    history = train_neural_network(
        model=model,
        dataset=dummy_dataset,
        epochs=15,
        train_pct=80.0,
        val_pct=10.0,
        test_pct=10.0,
        learning_rate=0.01,
    )

    final_loss = history["train_loss"][-1]
    print(f"LSTM Loss reduction: {initial_loss:.5f} -> {final_loss:.5f}")
    # Assert training loss decreased
    assert final_loss < initial_loss

    # Assert Test set evaluation isolation (intermediate indices must be placeholder 0.0s)
    for t in range(len(history["test_loss"]) - 1):
        assert history["test_loss"][t] == 0.0
    # Only the final index evaluates
    assert history["test_loss"][-1] > 0.0


def test_models_lstm_learning_convergence() -> None:
    """Validates robust LSTM BPTT mathematical convergence, ensuring training loss drops by at least 15%."""
    dummy_dataset = []
    for _ in range(15):
        dummy_dataset.append({"key": [1.0, 0.0, 0.0, 0.0] + [0.8] * 10, "value": [0.3] * 10})

    model = LSTMModel(input_size=5, hidden_layers=[8], output_size=1)
    
    initial_loss = evaluate_loss(model, dummy_dataset)

    # Train LSTM for 30 epochs to assert math convergence
    history = train_neural_network(
        model=model,
        dataset=dummy_dataset,
        epochs=30,
        train_pct=80.0,
        val_pct=10.0,
        test_pct=10.0,
        learning_rate=0.01,
    )

    final_loss = history["train_loss"][-1]
    percentage_drop = ((initial_loss - final_loss) / initial_loss) * 100.0
    print(f"\n>> LSTM Convergence Drop: {initial_loss:.5f} -> {final_loss:.5f} (Drop: {percentage_drop:.1f}%)\n")

    # Guarantee learning convergence by asserting drop is at least 15.0%
    assert percentage_drop >= 15.0


def test_line_limit_models_package() -> None:
    """Asserts that FCN, RNN, LSTM, and Trainer files strictly stay under 150 logical lines of code."""
    models_dir = Path(__file__).resolve().parents[2] / "src" / "homework_1" / "services" / "models"

    files_to_check = [
        models_dir / "fcn" / "model.py",
        models_dir / "rnn" / "model.py",
        models_dir / "lstm" / "model.py",
        models_dir / "trainer.py",
        models_dir / "math_utils.py",
    ]

    for filepath in files_to_check:
        assert filepath.exists()
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        logical_code_lines = 0
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                continue
            logical_code_lines += 1

        print(f"Logical code line count of {filepath.name}: {logical_code_lines}")
        # Every file must stay strictly under the 150-line limit
        assert logical_code_lines <= 150


def test_sdk_models_training_integration() -> None:
    """Validates that FCN, RNN, and LSTM models train successfully through the SDK entry points."""
    from homework_1.sdk import HomeWorkSDK

    sdk = HomeWorkSDK()

    # Adjust config temporarily to run a very quick 2-epoch training run to prevent slow tests
    sdk.config_manager._setup_config["models"]["epochs"] = 2

    # 1. Test FCN training
    fcn_resp = sdk.train_fcn()
    assert fcn_resp["status"] == "success"
    assert fcn_resp["result"]["model_type"] == "FCN"
    assert len(fcn_resp["result"]["history"]["train_loss"]) == 2

    # 2. Test RNN training
    rnn_resp = sdk.train_rnn()
    assert rnn_resp["status"] == "success"
    assert rnn_resp["result"]["model_type"] == "RNN"
    assert len(rnn_resp["result"]["history"]["train_loss"]) == 2

    # 3. Test LSTM training
    lstm_resp = sdk.train_lstm()
    assert lstm_resp["status"] == "success"
    assert lstm_resp["result"]["model_type"] == "LSTM"
    assert len(lstm_resp["result"]["history"]["train_loss"]) == 2

