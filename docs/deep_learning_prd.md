# Product Requirements Document (PRD): Deep Learning Models Engine

## Overview
The Deep Learning Models Engine is the model training and evaluation layer of the **HomeWork_1** package. Building upon the Dataset Generator Engine, this service will train three distinct deep learning architectures (RNN, LSTM, and FCN) to reconstruct clean original wave components from composite noised mixtures given target selection selectors.

---

## Objectives
1. Implement 3 configurable deep learning architectures:
   * **RNN** (Recurrent Neural Network)
   * **LSTM** (Long Short-Term Memory)
   * **Fully Connected Layer** (FCN / Multi-Layer Perceptron)
2. Expose flexible training configurations, including dataset splitting validation, epoch duration, and dynamic list-based hidden layer sizes.
3. Periodically evaluate and output training, validation, and test error metrics during training.

---

## Functional Requirements

### FR-1: Model Architectures
The system **MUST** support training 3 separate neural network architectures on our synthesized key-value dataset:
1.  **FCN (Fully Connected Network)**: Standard Multi-Layer Perceptron.
2.  **RNN (Recurrent Neural Network)**: Recurrent layers processing input sequences.
3.  **LSTM (Long Short-Term Memory)**: Gated recurrent units designed to model long-term temporal patterns.

---

### FR-2: Dataset Splitting & Integrity Verification
*   The training pipeline **MUST** accept configurable percentage splits for the dataset:
    *   `train_percentage` (float)
    *   `val_percentage` (float)
    *   `test_percentage` (float)
*   **Split Validation Rule**:
    *   The system **MUST** calculate the sum of the splits: $S = \text{train\_percentage} + \text{val\_percentage} + \text{test\_percentage}$.
    *   If $S \ne 100\%$, the system **MUST** print a clear **warning message** to the terminal, but may gracefully proceed by normalizing the values or using default splits.

---

### FR-3: Configurable Hidden Layer Profiles
*   The network hidden layer architectures **MUST** be specified via configuration lists:
    *   `hidden_layers`: A list of integers representing the width/size of each hidden layer.
*   **Dynamic Construction Rule**:
    *   The number of hidden layers is determined by the length of the list.
    *   The size of each hidden layer is determined by the list values.
    *   *Example*: If `hidden_layers = [3, 5, 3]`, the model must be constructed with exactly 3 hidden layers with sizes 3, 5, and 3 respectively.

---

### FR-4: Training Execution & Periodic Metrics Output
*   The number of training epochs **MUST** be loaded from the configuration files.
*   **Periodic Performance Evaluation**:
    *   During training, the system **MUST** evaluate current training loss/error on three sets:
        *   **Train Set**
        *   **Validation Set**
        *   **Test Set**
    *   This three-way error metric evaluation **MUST** be computed and printed to the terminal **after every 10 epochs**.
*   **Final Evaluation**:
    *   Upon completion of the final epoch, a complete evaluation report summarizing training loss, validation loss, and test error percentages **MUST** be plotted or printed.

---

## Input and Output Shapes Compliance

All models must consume keys and produce values conforming to the dataset schema generated in our previous pipeline:
*   **Input (X)**: Size **14** (size-4 one-hot selection array + size-10 noised composite sum signal window).
*   **Target (Y)**: Size **10** (size-10 clean original signal window).
