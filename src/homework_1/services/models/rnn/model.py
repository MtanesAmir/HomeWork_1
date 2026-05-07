"""Recurrent Neural Network (RNN) model module.

Implements a sequence-by-sequence Recurrent Neural Network processing
temporal inputs and selection masks to generate clean signal components.
"""

from typing import List, Tuple

from homework_1.services.models.math_utils import (
    dot,
    matmul,
    random_matrix,
    random_vector,
    sigmoid,
    sigmoid_derivative,
    tanh,
    tanh_derivative,
)


import torch
import torch.nn as nn
from typing import List


class RNNModel(nn.Module):
    """Implements a temporal Multi-Layer Recurrent Neural Network (RNN) model utilizing PyTorch."""

    def __init__(self, input_size: int = 5, hidden_layers: List[int] = None, output_size: int = 1):
        super().__init__()
        self.input_size = input_size
        self.hidden_layers = hidden_layers if hidden_layers else [8]
        self.output_size = output_size

        # PyTorch nn.ModuleList to store recurrent layers
        self.rnn_layers = nn.ModuleList()
        prev_dim = input_size
        for h_dim in self.hidden_layers:
            # Instantiate individual RNN cell block layers
            self.rnn_layers.append(nn.RNN(input_size=prev_dim, hidden_size=h_dim, batch_first=True))
            prev_dim = h_dim

        # Final linear projection layer
        self.fc = nn.Linear(self.hidden_layers[-1], output_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Propagates stacked multi-layer recurrent states forward. Input shape: (Batch, seq_len, input_size)"""
        current_inputs = x
        for rnn_cell in self.rnn_layers:
            # Propagate sequence through RNN cell. out shape: (Batch, seq_len, h_dim)
            current_inputs, _ = rnn_cell(current_inputs)

        # Extract predictions projecting the final layer hidden sequence outputs
        return torch.sigmoid(self.fc(current_inputs))

    def get_prediction(self, x_flat: List[float]) -> List[float]:
        """Extracts predictions from flat size-14 inputs as Python floats."""
        self.eval()
        with torch.no_grad():
            one_hot = x_flat[:4]
            signals = x_flat[4:]
            x_seq = [one_hot + [sig] for sig in signals]

            # Convert to PyTorch tensor matching batch-sequence dim shape (1, 10, 5)
            inp = torch.tensor([x_seq], dtype=torch.float32)
            pred = self.forward(inp)  # shape: (1, 10, 1)
            return pred[0].squeeze(-1).tolist()

    def backward(self, x_flat: List[float], target: List[float], learning_rate: float = 0.1) -> float:
        """Compatibility backward training pass performing standard Adam step and returning loss value."""
        self.train()
        optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)
        criterion = nn.MSELoss()

        one_hot = x_flat[:4]
        signals = x_flat[4:]
        x_seq = [one_hot + [sig] for sig in signals]

        inp = torch.tensor([x_seq], dtype=torch.float32)
        targ = torch.tensor([target], dtype=torch.float32).unsqueeze(-1)  # shape: (1, 10, 1)

        optimizer.zero_grad()
        pred = self.forward(inp)
        loss = criterion(pred, targ)
        loss.backward()
        optimizer.step()

        return float(loss.item())
