"""Mathematical utilities module.

Provides matrix/vector mathematics and activation functions in raw Python
to stay compliant with linter and structural guidelines.
"""

import math
import random
from typing import List


def dot(v1: List[float], v2: List[float]) -> float:
    """Calculates the dot product of two vectors."""
    return sum(x * y for x, y in zip(v1, v2))


def matmul(M: List[List[float]], v: List[float]) -> List[float]:
    """Multiplies a matrix by a vector."""
    return [dot(row, v) for row in M]


def sigmoid(x: float) -> float:
    """Applies the Sigmoid activation function."""
    # Clip x to avoid overflow/underflow bounds
    x_clipped = max(-500.0, min(500.0, x))
    return 1.0 / (1.0 + math.exp(-x_clipped))


def sigmoid_derivative(y: float) -> float:
    """Derivative of Sigmoid given its output y."""
    return y * (1.0 - y)


def tanh(x: float) -> float:
    """Applies the Hyperbolic Tangent activation function."""
    return math.tanh(x)


def tanh_derivative(y: float) -> float:
    """Derivative of Tanh given its output y."""
    return 1.0 - y * y


def relu(x: float) -> float:
    """Applies the Rectified Linear Unit activation function."""
    return max(0.0, x)


def relu_derivative(y: float) -> float:
    """Derivative of ReLU given its output y."""
    return 1.0 if y > 0.0 else 0.0


def random_matrix(rows: int, cols: int) -> List[List[float]]:
    """Initializes a matrix with random values in range [-0.1, 0.1]."""
    return [[random.uniform(-0.1, 0.1) for _ in range(cols)] for _ in range(rows)]


def random_vector(size: int) -> List[float]:
    """Initializes a vector with random values in range [-0.1, 0.1]."""
    return [random.uniform(-0.1, 0.1) for _ in range(size)]
