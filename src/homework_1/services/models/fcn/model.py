import torch
import torch.nn as nn
from typing import List


class FCNModel(nn.Module):
    """Implements a configurable Fully Connected Network model utilizing PyTorch."""

    def __init__(
        self,
        input_size: int = 14,
        hidden_layers: List[int] = None,
        output_size: int = 10,
    ):
        super().__init__()
        self.input_size = input_size
        self.hidden_layers = hidden_layers if hidden_layers else [3, 5, 3]
        self.output_size = output_size

        # Build sequential stacked dynamic layers
        layers = []
        prev_dim = input_size
        for h_dim in self.hidden_layers:
            layers.append(nn.Linear(prev_dim, h_dim))
            layers.append(nn.Sigmoid())
            prev_dim = h_dim

        layers.append(nn.Linear(prev_dim, output_size))
        layers.append(nn.Sigmoid())
        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Propagates input x forward."""
        return self.network(x)

    def get_prediction(self, x_flat: List[float]) -> List[float]:
        """Convenience prediction method returning standard Python floats list."""
        self.eval()
        with torch.no_grad():
            inp = torch.tensor(x_flat, dtype=torch.float32)
            pred = self.forward(inp)
            return pred.tolist()

    def backward(self, x_flat: List[float], target: List[float], learning_rate: float = 0.1) -> float:
        """Compatibility backward training pass performing standard Adam steps and returning loss value."""
        self.train()
        optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)
        criterion = nn.MSELoss()

        inp = torch.tensor(x_flat, dtype=torch.float32)
        targ = torch.tensor(target, dtype=torch.float32)

        optimizer.zero_grad()
        pred = self.forward(inp)
        loss = criterion(pred, targ)
        loss.backward()
        optimizer.step()

        return float(loss.item())
