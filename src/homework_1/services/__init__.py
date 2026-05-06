"""Services package.

Contains specific business logic service implementations.
"""

from homework_1.services.generator import (
    generate_dataset,
    prepare_base_signals,
    save_dataset,
)
from homework_1.services.models import FCNModel, LSTMModel, RNNModel, train_neural_network
from homework_1.services.sinus import (
    SinusWave,
    generate_sinus_samples,
    sum_sinus_lists,
    sum_sinus_waves,
)

__all__ = [
    "SinusWave",
    "generate_sinus_samples",
    "sum_sinus_lists",
    "sum_sinus_waves",
    "prepare_base_signals",
    "generate_dataset",
    "save_dataset",
    "FCNModel",
    "RNNModel",
    "LSTMModel",
    "train_neural_network",
]
