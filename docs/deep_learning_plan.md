# Implementation Plan: Deep Learning Models Engine

This document outlines the technical implementation plan for developing the **Deep Learning Models Engine** in the **HomeWork_1** package, providing an actionable guide for our developers.

---

## Phase 1: Architectural Setup & Folder Structure

To keep our architectures strictly modular and highly cohesive, each neural network model will have its own dedicated subdirectory under `src/homework_1/services/models/`:

```text
src/homework_1/services/models/
├── __init__.py
├── fcn/                      # Fully Connected Network (FCN)
│   ├── __init__.py
│   └── model.py
├── rnn/                      # Recurrent Neural Network (RNN)
│   ├── __init__.py
│   └── model.py
└── lstm/                     # Long Short-Term Memory (LSTM)
    ├── __init__.py
    └── model.py
```

### Configuration Layer Integration (`config/setup.json`)
Extend the settings with a dedicated `models` block:
```json
{
  "models": {
    "epochs": 50,
    "train_percentage": 70.0,
    "val_percentage": 15.0,
    "test_percentage": 15.0,
    "hidden_layers": [3, 5, 3]
  }
}
```

---

## Phase 2: Development & Code Splitting Strategy

### Code Constraint: The 150-Line Rule
Adhering strictly to Section 3.2 of the **Software Submission Guidelines (V3)**:
*   **No single Python file is allowed to exceed 150 lines of logical code** (blank lines and comments are not counted).
*   **Code Splitting Strategy**: If any model definition, training loop, or verification pipeline approaches 120-130 logical lines, it **MUST** be decomposed. For example, separate the model definition (`model.py`) from the training pipeline executor (`trainer.py`).

### Model Specifications

1.  **FCN Model (`fcn/model.py`)**:
    *   Implements a Multi-Layer Perceptron (MLP).
    *   Input: Vector of size 14. Output: Vector of size 10.
    *   Hidden layers are constructed dynamically based on the `hidden_layers` configuration array.
2.  **RNN Model (`rnn/model.py`)**:
    *   Recurrent Neural Network layer processing sequence inputs of length 14 (or sliding sequences).
    *   Dynamically maps parameters and hidden dimensions from config.
3.  **LSTM Model (`lstm/model.py`)**:
    *   LSTM layers designed to isolate temporal dependencies.
    *   Maps cell states and gated outputs dynamically from hidden layer lists.

### Training Pipeline Coordinator (`src/homework_1/services/models/trainer.py`)
To ensure `model.py` files stay exceptionally clean, we will build a centralized training coordinator:
*   **Split Verification**: Validates that `train_percentage + val_percentage + test_percentage == 100`. Logs a prominent terminal warning if the sum is invalid.
*   **Periodic Evaluation**: Evaluates Train, Validation, and Test loss **after every 10 epochs** and logs them to the terminal.

---

## Phase 3: Verification Plan & Pytest Suite

We will implement automated tests inside `tests/unit/test_models.py`:

### Test Scenarios:
1.  **Split Warning Verification**:
    *   Test with splits summing to 90% or 110% and assert that the warning is outputted to stdout/stderr.
2.  **Dynamic Network Layer Assertions**:
    *   Initialize models with hidden profiles like `[5, 10, 5]`.
    *   Programmatically assert that the number of hidden layers matches the list length, and layer sizes match the list values.
3.  **Training Verification**:
    *   Synthesize a small dataset using our generator tool.
    *   Train FCN, RNN, and LSTM on this dataset for 10 epochs.
    *   Assert that the training completes successfully, losses decrease, and evaluation metrics output correctly.
4.  **Code Style & Line Count Assertions**:
    *   Write programmatic checks to assert that **every single Python file** in the `models/` subdirectories strictly stays **under 150 lines of logical code**.
