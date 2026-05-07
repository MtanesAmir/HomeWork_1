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


import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from homework_1.services.models.rnn.model import RNNModel
from homework_1.services.models.lstm.model import LSTMModel


def evaluate_loss(model: Any, dataset_set: List[Dict[str, Any]]) -> float:
    """Calculates mean squared error (MSE) loss of a model on a dataset subset utilizing PyTorch tensors."""
    if not dataset_set:
        return 0.0
    model.eval()
    criterion = nn.MSELoss()

    keys = [row["key"] for row in dataset_set]
    values = [row["value"] for row in dataset_set]

    with torch.no_grad():
        if isinstance(model, (RNNModel, LSTMModel)):
            # Format recurrent sequence shape (Batch, 10, 5)
            seqs = []
            for key in keys:
                one_hot = key[:4]
                signals = key[4:]
                seqs.append([one_hot + [sig] for sig in signals])
            inp = torch.tensor(seqs, dtype=torch.float32)
            targ = torch.tensor(values, dtype=torch.float32).unsqueeze(-1)
        else:
            inp = torch.tensor(keys, dtype=torch.float32)
            targ = torch.tensor(values, dtype=torch.float32)

        pred = model(inp)
        loss = criterion(pred, targ)
        return float(loss.item())


def train_neural_network(
    model: Any,
    dataset: List[Dict[str, Any]],
    epochs: int,
    train_pct: float,
    val_pct: float,
    test_pct: float,
    learning_rate: float = 0.01,
) -> Dict[str, List[float]]:
    """Runs PyTorch batched training loops using Adam optimizer, MSELoss, and norm gradient clipping."""
    validate_splits(train_pct, val_pct, test_pct)
    train_set, val_set, test_set = partition_dataset(dataset, train_pct, val_pct, test_pct)

    history = {"train_loss": [], "val_loss": [], "test_loss": []}

    # 1. Prepare PyTorch DataLoader batching (Batch Size: 32)
    train_keys = [row["key"] for row in train_set]
    train_values = [row["value"] for row in train_set]

    if isinstance(model, (RNNModel, LSTMModel)):
        seqs = []
        for key in train_keys:
            one_hot = key[:4]
            signals = key[4:]
            seqs.append([one_hot + [sig] for sig in signals])
        x_tensor = torch.tensor(seqs, dtype=torch.float32)
        y_tensor = torch.tensor(train_values, dtype=torch.float32).unsqueeze(-1)
    else:
        x_tensor = torch.tensor(train_keys, dtype=torch.float32)
        y_tensor = torch.tensor(train_values, dtype=torch.float32)

    train_loader = DataLoader(TensorDataset(x_tensor, y_tensor), batch_size=32, shuffle=True)

    # 2. Initialize PyTorch Adam Optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.MSELoss()

    for epoch in range(1, epochs + 1):
        model.train()
        for bx, by in train_loader:
            optimizer.zero_grad()
            pred = model(bx)
            loss = criterion(pred, by)
            loss.backward()

            # 3. Apply PyTorch norm gradient clipping (Max Norm: 5.0)
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
            optimizer.step()

        # Record metrics progress histories
        history["train_loss"].append(evaluate_loss(model, train_set))
        history["val_loss"].append(evaluate_loss(model, val_set))
        history["test_loss"].append(0.0)

        if epoch == 1 or epoch % 10 == 0 or epoch == epochs:
            t_loss = history["train_loss"][-1]
            v_loss = history["val_loss"][-1]
            print(
                f"[Epoch {epoch:02d}/{epochs}] "
                f"Train Loss: {t_loss:.5f} | Val Loss: {v_loss:.5f} | Test Loss: (Evaluating at end...)"
            )

    # Compute holdout Test Set MSE once training completes
    history["test_loss"][-1] = evaluate_loss(model, test_set)
    final_test = history["test_loss"][-1]
    print(f"\n>> Training complete. Final Test Set MSE: {final_test:.5f}\n")

    return history
