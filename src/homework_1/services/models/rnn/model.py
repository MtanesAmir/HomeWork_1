"""Recurrent Neural Network (RNN) model module.

Implements a sequence-by-sequence Recurrent Neural Network processing
temporal inputs and selection masks to generate clean signal components.
"""

from typing import List

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


class RNNModel:
    """Implements a temporal Recurrent Neural Network (RNN) model."""

    def __init__(self, input_size: int = 5, hidden_size: int = 8, output_size: int = 1):
        self.input_size = input_size  # size 5: one-hot (4) + signal (1)
        self.hidden_size = hidden_size
        self.output_size = output_size  # size 1: clean signal scalar

        # Initialize weights
        self.W_xh = random_matrix(hidden_size, input_size)
        self.W_hh = random_matrix(hidden_size, hidden_size)
        self.W_hy = random_matrix(output_size, hidden_size)

        # Initialize biases
        self.b_h = random_vector(hidden_size)
        self.b_y = random_vector(output_size)

    def forward_sequence(self, x_seq: List[List[float]]) -> List[List[float]]:
        """Runs the forward pass over a sequence of inputs. Returns all hidden states."""
        hidden_states = [random_vector(self.hidden_size)]  # Initial hidden state h_0
        current_h = hidden_states[0]

        for x_t in x_seq:
            # z_h = W_xh * x_t + W_hh * h_{t-1} + b_h
            term1 = matmul(self.W_xh, x_t)
            term2 = matmul(self.W_hh, current_h)
            z_h = [t1 + t2 + b for t1, t2, b in zip(term1, term2, self.b_h)]
            current_h = [tanh(z_i) for z_i in z_h]
            hidden_states.append(current_h)

        return hidden_states

    def get_prediction(self, x_flat: List[float]) -> List[float]:
        """Directly extracts predictions from flat size-14 inputs."""
        # Convert flat 14 to sequence of 10 steps of size 5
        one_hot = x_flat[:4]
        signals = x_flat[4:]
        x_seq = [one_hot + [sig] for sig in signals]

        hidden_states = self.forward_sequence(x_seq)
        predictions = []
        # Skip initial h_0, map h_1..h_10 to predictions
        for h_t in hidden_states[1:]:
            z_y = matmul(self.W_hy, h_t)[0] + self.b_y[0]
            predictions.append(sigmoid(z_y))

        return predictions

    def backward(
        self, x_flat: List[float], target: List[float], learning_rate: float = 0.1
    ) -> float:
        """Backpropagation training step for RNN. Adjusts parameters via gradient descent."""
        one_hot = x_flat[:4]
        signals = x_flat[4:]
        x_seq = [one_hot + [sig] for sig in signals]

        hidden_states = self.forward_sequence(x_seq)
        predictions = []
        y_layers = []
        for h_t in hidden_states[1:]:
            z_y = matmul(self.W_hy, h_t)[0] + self.b_y[0]
            y_val = sigmoid(z_y)
            predictions.append(y_val)
            y_layers.append(y_val)

        # 1. Calculate MSE Loss
        loss = sum((p - t) ** 2 for p, t in zip(predictions, target)) / len(target)

        # 2. Calculate Output errors and deltas
        dy_deltas = []
        for p, t in zip(predictions, target):
            dy_deltas.append((p - t) * sigmoid_derivative(p))

        # 3. Backpropagation Through Time (BPTT)
        dh_next = [0.0] * self.hidden_size
        for t in range(len(x_seq) - 1, -1, -1):
            h_t = hidden_states[t + 1]
            h_prev = hidden_states[t]
            x_t = x_seq[t]

            # Gradient of output weights
            for i in range(self.hidden_size):
                self.W_hy[0][i] -= learning_rate * dy_deltas[t] * h_t[i]
            self.b_y[0] -= learning_rate * dy_deltas[t]

            # Error back to hidden state
            dh = [self.W_hy[0][i] * dy_deltas[t] + dh_next[i] for i in range(self.hidden_size)]
            # Gradient of Tanh activation
            dh_raw = [dh_i * tanh_derivative(h_i) for dh_i, h_i in zip(dh, h_t)]

            # Update W_xh weights
            for i in range(self.hidden_size):
                for j in range(self.input_size):
                    self.W_xh[i][j] -= learning_rate * dh_raw[i] * x_t[j]

            # Update W_hh weights
            for i in range(self.hidden_size):
                for j in range(self.hidden_size):
                    self.W_hh[i][j] -= learning_rate * dh_raw[i] * h_prev[j]

            # Update biases b_h
            for i in range(self.hidden_size):
                self.b_h[i] -= learning_rate * dh_raw[i]

            # Compute next hidden state delta
            dh_next = [sum(self.W_hh[j][i] * dh_raw[j] for j in range(self.hidden_size)) for i in range(self.hidden_size)]

        return loss
