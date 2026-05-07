# Technical Plan: First Feedback Revisions Implementation

This document defines the step-by-step implementation plan to address all user feedback detailed in **[first_feedback_prd.md](file:///Users/amirmt/Desktop/ME/Me/MSC-ComputerScience/2025-B/agent%20AI/hw1/HomeWork_1/docs/first_feedback_prd.md)**, utilizing a verification-guaranteed phased roadmap.

---

## Phase 1: Screen 1 Slider Range Tuning (Frequency Scale)

### 1. Proposed Changes
*   **Target File**: `src/homework_1/shared/gui/screen1.py`
*   **Modification**: Locate the `get_sinusoid_card` layout generation helper. Change the frequency slider parameters:
    ```python
    # From:
    dcc.Slider(id=f"freq-{idx}", min=0.1, max=100.0, step=0.1, value=default_freq, ...)
    # To:
    dcc.Slider(id=f"freq-{idx}", min=0.1, max=50.0, step=0.1, value=default_freq, ...)
    ```
*   **Line Count Check**: Confirm `screen1.py` remains strictly below **150 logical lines of code**.

### 2. Phase Verification
*   Run `PYTHONPATH=src pytest -k "test_gui_screen1_default_elements"` to verify Screen 1 elements render cleanly under the new frequency limits.

---

## Phase 2: Deep Learning Engine Training Optimization (Test Set Isolation)

### 1. Proposed Changes
*   **Target File**: `src/homework_1/services/models/trainer.py`
*   **Modification**:
    *   Modify the training epochs loop in `train_neural_network`.
    *   Remove the `evaluate_loss(model, test_set)` computation from the active loop. Append `history["test_loss"]` with `0.0` placeholders or skip recording it until the final epoch.
    *   At the final epoch completion, compute the test set error exactly once:
        ```python
        test_loss = evaluate_loss(model, test_set)
        history["test_loss"][-1] = test_loss  # Populate final epoch test loss
        ```
*   **Line Count Check**: Confirm `trainer.py` remains strictly below **150 logical lines of code**.

### 2. Phase Verification
*   Add assertions to `tests/unit/test_models.py` validating that the intermediate indices in `history["test_loss"]` are placeholders, and only the final epoch is evaluated on the test set.
*   Run `PYTHONPATH=src pytest tests/unit/test_models.py` and confirm all tests pass.

---

## Phase 3: Throttled Metrics Progress Diagnostics & Plotting

### 1. Proposed Changes
*   **Target File**: `src/homework_1/shared/gui/callbacks_training.py` and `src/homework_1/services/models/trainer.py`
*   **Modification**:
    *   Modify `train_neural_network` to only print/log diagnostics to the console if `epoch == 1 or epoch % 10 == 0 or epoch == epochs`.
    *   Modify the Dash `monitor_training_progress` callback. Limit figure coordinates update logic to fetch and plot points in 10-epoch increments (e.g. epoch 10, 20, 30, etc.).

### 2. Phase Verification
*   Run `PYTHONPATH=src pytest tests/unit/test_gui.py` to assert that throttled curves updates match Plotly coordinates targets.

---

## Phase 4: Back-End Multi-Threaded Parallel Model Training

### 1. Proposed Changes
*   **Target File**: `src/homework_1/shared/gui/callbacks_training.py`
*   **Modification**:
    *   We want to train all three models concurrently to prevent dashboard freezing.
    *   Use Python's native `threading` library. Create three background threads:
        *   `Thread(target=sdk.train_fcn)`
        *   `Thread(target=sdk.train_rnn)`
        *   `Thread(target=sdk.train_lstm)`
    *   Clicking "Let the models learn" launches these three threads in parallel.
    *   Threads will write loss metrics to a shared cache (such as global dictionaries or Dash `dcc.Store` objects).
    *   The Dash `monitor_training_progress` callback pulls metrics from these shared caches asynchronously every 500ms, updating all three graphs concurrently.
*   **Line Count Check**: Ensure `callbacks_training.py` remains strictly below **150 logical lines of code**.

### 2. Phase Verification
*   Assert in our tests that FCN, RNN, and LSTM model threads execute concurrently and complete in parallel without blocking the main dashboard process.
*   Run `PYTHONPATH=src pytest` and verify passing status.

---

## Phase 5: Safe Exit Isolation & Sandbox Protection

### 1. Proposed Changes
*   **Target File**: `src/homework_1/shared/gui/callbacks_playground.py`
*   **Modification**:
    *   Inspect `handle_slice_generation` and `evaluate_models_predictions` callbacks.
    *   Assert that no overlap occurs with `handle_server_exit` inputs or states.
    *   Confirm that the **"Exit Dashboard"** button is the *sole* trigger for process termination.

### 2. Phase Verification
*   Trigger multiple repeated **"Generate Slice"** simulations in `tests/unit/test_gui.py` and assert that the server remains active and continues producing predictions without terminating early.
*   Run the E2E test suite and confirm 100% clean, green status.
