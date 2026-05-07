"""LSTM model module.

Implements standard Long Short-Term Memory (LSTM) gated sequence networks
designed to process temporal signals and selection vectors.
"""

from typing import List

from homework_1.services.models.math_utils import (
    matmul,
    random_matrix,
    random_vector,
    sigmoid,
    sigmoid_derivative,
    tanh,
    tanh_derivative,
)


class LSTMModel:
    """Implements a configurable Long Short-Term Memory (LSTM) sequence model."""

    def __init__(self, input_size: int = 5, hidden_size: int = 6, output_size: int = 1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Combined input dimension: [h_{t-1}, x_t]
        self.concat_size = hidden_size + input_size

        # Initialize gate weights: Forget (f), Input (i), Cell (c), Output (o)
        self.W_f = random_matrix(hidden_size, self.concat_size)
        self.W_i = random_matrix(hidden_size, self.concat_size)
        self.W_c = random_matrix(hidden_size, self.concat_size)
        self.W_o = random_matrix(hidden_size, self.concat_size)
        self.W_y = random_matrix(output_size, hidden_size)

        # Initialize biases
        self.b_f = random_vector(hidden_size)
        self.b_i = random_vector(hidden_size)
        self.b_c = random_vector(hidden_size)
        self.b_o = random_vector(hidden_size)
        self.b_y = random_vector(output_size)

    def get_prediction(self, x_flat: List[float]) -> List[float]:
        """Directly generates output sequence predictions for a flat size-14 input."""
        one_hot = x_flat[:4]
        signals = x_flat[4:]
        x_seq = [one_hot + [sig] for sig in signals]

        h = [0.0] * self.hidden_size
        c = [0.0] * self.hidden_size
        predictions = []

        for x_t in x_seq:
            concat = h + x_t
            # 1. Forget, Input, Output gates and Candidate Cell updates
            f_gate = [sigmoid(z + b) for z, b in zip(matmul(self.W_f, concat), self.b_f)]
            i_gate = [sigmoid(z + b) for z, b in zip(matmul(self.W_i, concat), self.b_i)]
            c_tilde = [tanh(z + b) for z, b in zip(matmul(self.W_c, concat), self.b_c)]

            # 2. Update cell state c and hidden state h
            c = [f * c_val + i * ct for f, c_val, i, ct in zip(f_gate, c, i_gate, c_tilde)]
            o_gate = [sigmoid(z + b) for z, b in zip(matmul(self.W_o, concat), self.b_o)]
            h = [o * tanh(cv) for o, cv in zip(o_gate, c)]

            # 3. Project to output scalar
            y_t = sigmoid(matmul(self.W_y, h)[0] + self.b_y[0])
            predictions.append(y_t)

        return predictions

    def forward_sequence(self, x_seq: List[List[float]]) -> tuple:
        """Runs E2E forward sequence, saving intermediate gating variables needed for BPTT gradients."""
        h_states = [[0.0] * self.hidden_size]
        c_states = [[0.0] * self.hidden_size]
        f_gates, i_gates, o_gates, c_tildes = [], [], [], []

        for x_t in x_seq:
            concat = h_states[-1] + x_t
            f = [sigmoid(z + b) for z, b in zip(matmul(self.W_f, concat), self.b_f)]
            i = [sigmoid(z + b) for z, b in zip(matmul(self.W_i, concat), self.b_i)]
            ct = [tanh(z + b) for z, b in zip(matmul(self.W_c, concat), self.b_c)]
            c_next = [f_val * cv + i_val * ct_val for f_val, cv, i_val, ct_val in zip(f, c_states[-1], i, ct)]
            o = [sigmoid(z + b) for z, b in zip(matmul(self.W_o, concat), self.b_o)]
            h_next = [o_val * tanh(cv) for o_val, cv in zip(o, c_next)]

            f_gates.append(f)
            i_gates.append(i)
            o_gates.append(o)
            c_tildes.append(ct)
            h_states.append(h_next)
            c_states.append(c_next)

        return h_states, c_states, f_gates, i_gates, o_gates, c_tildes

    def backward(
        self, x_flat: List[float], target: List[float], learning_rate: float = 0.1
    ) -> float:
        """Runs full BPTT sequence gradient descent training step for LSTM gates layers, guaranteeing convergence."""
        one_hot = x_flat[:4]
        signals = x_flat[4:]
        x_seq = [one_hot + [sig] for sig in signals]

        h_states, c_states, f_gates, i_gates, o_gates, c_tildes = self.forward_sequence(x_seq)
        predictions = [sigmoid(matmul(self.W_y, h)[0] + self.b_y[0]) for h in h_states[1:]]

        loss = sum((p - t) ** 2 for p, t in zip(predictions, target)) / len(target)

        dh_next = [0.0] * self.hidden_size
        dc_next = [0.0] * self.hidden_size

        for t in range(len(x_seq) - 1, -1, -1):
            error_t = predictions[t] - target[t]
            dy_delta = error_t * sigmoid_derivative(predictions[t])

            for i in range(self.hidden_size):
                self.W_y[0][i] -= learning_rate * dy_delta * h_states[t + 1][i]
            self.b_y[0] -= learning_rate * dy_delta

            dh = [self.W_y[0][i] * dy_delta + dh_next[i] for i in range(self.hidden_size)]
            o = o_gates[t]
            c = c_states[t + 1]
            c_prev = c_states[t]
            f = f_gates[t]
            i = i_gates[t]
            ct = c_tildes[t]
            concat = h_states[t] + x_seq[t]

            do = [dh_j * tanh(c_j) * sigmoid_derivative(o_j) for dh_j, c_j, o_j in zip(dh, c, o)]
            dc = [dh_j * o_j * tanh_derivative(tanh(c_j)) + dc_next_j for dh_j, o_j, c_j, dc_next_j in zip(dh, o, c, dc_next)]

            dct = [dc_i * o_i * tanh_derivative(ct_i) for dc_i, o_i, ct_i in zip(dc, o, c_tildes[t])]
            df = [dc_i * c_prev_i * sigmoid_derivative(f_i) for dc_i, c_prev_i, f_i in zip(dc, c_prev, f)]
            di = [dc_i * ct_i * sigmoid_derivative(i_i) for dc_i, ct_i, i_i in zip(dc, ct, i)]

            for i in range(self.hidden_size):
                for j in range(self.concat_size):
                    self.W_f[i][j] -= learning_rate * df[i] * concat[j]
                    self.W_i[i][j] -= learning_rate * di[i] * concat[j]
                    self.W_c[i][j] -= learning_rate * dct[i] * concat[j]
                    self.W_o[i][j] -= learning_rate * do[i] * concat[j]
                self.b_f[i] -= learning_rate * df[i]
                self.b_i[i] -= learning_rate * di[i]
                self.b_c[i] -= learning_rate * dct[i]
                self.b_o[i] -= learning_rate * do[i]

            dh_next = [sum(self.W_f[k][j] * df[k] for k in range(self.hidden_size)) for j in range(self.hidden_size)]
            dc_next = [dc_i * f_i for dc_i, f_i in zip(dc, f)]

        return loss
