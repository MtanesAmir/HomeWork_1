"""Training coordinator module.

Handles dataset partitioning, split percentage integrity checks,
and running training iterations with periodic diagnostic logging.
"""

import logging
from typing import Any, Dict, List, Tuple

# Set up logger
logger = logging.getLogger("homework_1.services.models.trainer")


def validate_splits(train_pct: float, val_pct: float, test_pct: float) -> bool:
    """Validates that dataset splits sum to exactly 100%. Logs warning if invalid."""
    total = train_pct + val_pct + test_pct
    if abs(total - 100.0) > 1e-7:
        print(
            f"\n⚠️ WARNING: Dataset splits (Train: {train_pct}%, Val: {val_pct}%, Test: {test_pct}%) "
            f"sum to {total}%, which is not exactly 100%!\n"
        )
        return False
    return True


def partition_dataset(
    dataset: List[Dict[str, Any]], train_pct: float, val_pct: float, test_pct: float
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Partitions dataset rows into train, validation, and test subsets."""
    total_rows = len(dataset)
    train_size = int(total_rows * (train_pct / 100.0))
    val_size = int(total_rows * (val_pct / 100.0))

    train_set = dataset[:train_size]
    val_set = dataset[train_size : train_size + val_size]
    test_set = dataset[train_size + val_size :]

    return train_set, val_set, test_set


def evaluate_loss(model: Any, dataset_set: List[Dict[str, Any]]) -> float:
    """Calculates mean squared error (MSE) loss of a model on a dataset subset."""
    if not dataset_set:
        return 0.0
    total_loss = 0.0
    for row in dataset_set:
        pred = model.get_prediction(row["key"])
        target = row["value"]
        total_loss += sum((p - t) ** 2 for p, t in zip(pred, target)) / len(target)
    return total_loss / len(dataset_set)


def train_neural_network(
    model: Any,
    dataset: List[Dict[str, Any]],
    epochs: int,
    train_pct: float,
    val_pct: float,
    test_pct: float,
    learning_rate: float = 0.05,
) -> Dict[str, List[float]]:
    """Runs training epochs loop, updates parameters, and outputs diagnostics every 10 epochs."""
    validate_splits(train_pct, val_pct, test_pct)
    train_set, val_set, test_set = partition_dataset(dataset, train_pct, val_pct, test_pct)

    history = {"train_loss": [], "val_loss": [], "test_loss": []}

    for epoch in range(1, epochs + 1):
        # Perform gradient descent backward step on train set
        for row in train_set:
            model.backward(row["key"], row["value"], learning_rate=learning_rate)

        # Record loss histories
        history["train_loss"].append(evaluate_loss(model, train_set))
        history["val_loss"].append(evaluate_loss(model, val_set))
        history["test_loss"].append(0.0)  # Use 0.0 as placeholder during epochs

        # Periodic Evaluation: after each 10 epochs (and epoch 1)
        if epoch == 1 or epoch % 10 == 0 or epoch == epochs:
            t_loss = history["train_loss"][-1]
            v_loss = history["val_loss"][-1]
            # Skip calculating test loss during training updates to save speed
            print(
                f"[Epoch {epoch:02d}/{epochs}] "
                f"Train Loss: {t_loss:.5f} | Val Loss: {v_loss:.5f} | Test Loss: (Evaluating at end...)"
            )

    # Compute Test Set MSE exactly once, strictly at final epoch completion
    history["test_loss"][-1] = evaluate_loss(model, test_set)
    final_test = history["test_loss"][-1]
    print(f"\n>> Training complete. Final Test Set MSE: {final_test:.5f}\n")

    return history
