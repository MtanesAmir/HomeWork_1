"""Fully Connected Network (FCN) model module.

Implements standard Multi-Layer Perceptron supporting dynamic hidden layers,
feed-forward propagation, and backpropagation training.
"""

from typing import List

from homework_1.services.models.math_utils import (
    matmul,
    random_matrix,
    random_vector,
    sigmoid,
    sigmoid_derivative,
)


class FCNModel:
    """Implements a configurable Fully Connected Network model."""

    def __init__(
        self,
        input_size: int = 14,
        hidden_layers: List[int] = [3, 5, 3],
        output_size: int = 10,
    ):
        if not hidden_layers:
            raise ValueError("Hidden layers configuration must have at least 1 layer")

        self.input_size = input_size
        self.hidden_layers = hidden_layers
        self.output_size = output_size

        # Layer dimensions: input_size -> hidden_layers -> output_size
        self.layer_dims = [input_size] + hidden_layers + [output_size]

        # Initialize weight matrices W and bias vectors b
        self.W = []
        self.b = []
        for i in range(len(self.layer_dims) - 1):
            self.W.append(random_matrix(self.layer_dims[i + 1], self.layer_dims[i]))
            self.b.append(random_vector(self.layer_dims[i + 1]))

    def forward(self, x: List[float]) -> List[List[float]]:
        """Propagates input x forward. Returns intermediate layer activations."""
        activations = [x]
        current = x
        for w_matrix, b_vector in zip(self.W, self.b):
            z = matmul(w_matrix, current)
            # Add bias and apply Sigmoid activation
            current = [sigmoid(z_i + b_i) for z_i, b_i in zip(z, b_vector)]
            activations.append(current)
        return activations

    def get_prediction(self, x: List[float]) -> List[float]:
        """Directly returns final network predictions for input x."""
        return self.forward(x)[-1]

    def backward(
        self, x: List[float], target: List[float], learning_rate: float = 0.1
    ) -> float:
        """Executes one step of backpropagation. Updates weights and returns MSE loss."""
        activations = self.forward(x)
        output = activations[-1]

        # 1. Calculate Output Layer error and deltas
        loss = sum((out_i - tar_i) ** 2 for out_i, tar_i in zip(output, target)) / len(target)
        errors = [out_i - tar_i for out_i, tar_i in zip(output, target)]
        deltas = [err * sigmoid_derivative(out_i) for err, out_i in zip(errors, output)]

        # 2. Backpropagate deltas back through hidden layers
        all_deltas = [deltas]
        current_deltas = deltas
        for l in range(len(self.W) - 1, 0, -1):
            w_matrix = self.W[l]
            prev_activation = activations[l]
            prev_deltas = []
            for j in range(len(prev_activation)):
                err_j = sum(w_matrix[k][j] * current_deltas[k] for k in range(len(current_deltas)))
                prev_deltas.append(err_j * sigmoid_derivative(prev_activation[j]))
            all_deltas.append(prev_deltas)
            current_deltas = prev_deltas

        # Reverse all_deltas list to align with layer indices 0 to L-1
        all_deltas.reverse()

        # 3. Update weights and biases
        for l in range(len(self.W)):
            delta_l = all_deltas[l]
            act_prev = activations[l]
            # Update W
            for i in range(len(delta_l)):
                for j in range(len(act_prev)):
                    self.W[l][i][j] -= learning_rate * delta_l[i] * act_prev[j]
            # Update b
            for i in range(len(delta_l)):
                self.b[l][i] -= learning_rate * delta_l[i]

        return loss
