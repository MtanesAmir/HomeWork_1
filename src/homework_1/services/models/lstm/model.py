import torch
import torch.nn as nn
from typing import List


class LSTMModel(nn.Module):
    """Implements a configurable Multi-Layer Long Short-Term Memory (LSTM) sequence model utilizing PyTorch."""

    def __init__(self, input_size: int = 5, hidden_layers: List[int] = None, output_size: int = 1):
        super().__init__()
        self.input_size = input_size
        self.hidden_layers = hidden_layers if hidden_layers else [6]
        self.output_size = output_size

        # PyTorch nn.ModuleList to store recurrent layers
        self.lstm_layers = nn.ModuleList()
        prev_dim = input_size
        for h_dim in self.hidden_layers:
            # Instantiate individual LSTM layer blocks
            self.lstm_layers.append(nn.LSTM(input_size=prev_dim, hidden_size=h_dim, batch_first=True))
            prev_dim = h_dim

        self.fc = nn.Linear(self.hidden_layers[-1], output_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Propagates stacked multi-layer LSTM forward. Input shape: (Batch, seq_len, input_size)"""
        current_inputs = x
        for lstm_cell in self.lstm_layers:
            current_inputs, _ = lstm_cell(current_inputs)

        return torch.sigmoid(self.fc(current_inputs))

    def get_prediction(self, x_flat: List[float]) -> List[float]:
        """Extracts predictions from flat size-14 inputs as Python floats list."""
        self.eval()
        with torch.no_grad():
            one_hot = x_flat[:4]
            signals = x_flat[4:]
            x_seq = [one_hot + [sig] for sig in signals]

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
        targ = torch.tensor([target], dtype=torch.float32).unsqueeze(-1)

        optimizer.zero_grad()
        pred = self.forward(inp)
        loss = criterion(pred, targ)
        loss.backward()
        optimizer.step()

        return float(loss.item())
