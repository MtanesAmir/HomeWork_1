# Technical Plan: Second Feedback Revisions Implementation

This document defines the technical roadmap for implementing all revisions detailed in **[second_feedback_prd.md](file:///Users/amirmt/Desktop/ME/Me/MSC-ComputerScience/2025-B/agent%20AI/hw1/HomeWork_1/docs/second_feedback_prd.md)**, including additional visual metrics descriptors panels on Screen 2.

---

## Phase 1: Sliced Sum Wave Dynamic Styling callback (Screen 3 Input)

### 1. Proposed Changes
*   **Target File**: `src/homework_1/shared/gui/callbacks_playground.py`
*   **Modification**:
    *   Update the `handle_slice_generation` callback to accept `Input("toggle-dots-lines", "value")` as an input dependency.
    *   Inside `handle_slice_generation`, change the go.Scatter mode:
        ```python
        # From:
        fig.add_trace(go.Scatter(..., mode="lines+markers"))
        # To:
        fig.add_trace(go.Scatter(..., mode=draw_mode))
        ```
*   **Line Count Check**: Ensure `callbacks_playground.py` remains strictly below **150 logical lines of code**.

### 2. Phase Verification
*   Run layout tests and verify that the input sliced wave figure correctly matches active style selection traces.

---

## Phase 2: RNN & LSTM Sequence Predictions Overlays Fixes

### 1. Proposed Changes
*   **Target File**: `src/homework_1/shared/gui/callbacks_playground.py`
*   **Modification**:
    *   Debug `evaluate_models_predictions` logic.
    *   Verify that the flat input vector of size 14 ($One-Hot Mask [4] + sliding sum [10]$) is extracted and passed correctly to the `RNNModel.get_prediction()` and `LSTMModel.get_prediction()` sequences in BPTT dimensions.
    *   Ensure predictions lists of size 10 are returned and mapped to go.Scatter traces correctly, updating all three graphs overlay outputs on Screen 3.

### 2. Phase Verification
*   Assert in `tests/unit/test_gui.py` that the prediction figures generated for FCN, RNN, and LSTM have data lengths of exactly 10 and are properly formatted.

---

## Phase 3: Metrics Legend panel addition (Screen 2 Left Side)

### 1. Proposed Changes
*   **Target File**: `src/homework_1/shared/gui/screen2.py`
*   **Modification**:
    *   Modify `get_screen2_layout()`. Split the main display into a sidebar-panel grid layout.
    *   *Left Sidebar (Legend Panel)*: Create a styled column displaying the following text descriptions (strictly max 1 line per metric):
        *   **Train Loss Curve (Blue Line)**: *Average prediction error on training samples, showing how the model learns.*
        *   **Val Loss Curve (Orange Line)**: *Unbiased prediction error on validation samples to detect overfitting.*
        *   **Test MSE Badge (Green Text)**: *Final accuracy score on unseen holdout samples after training concludes.*
*   **Line Count Check**: Ensure `screen2.py` remains strictly below **150 logical lines of code**.

### 2. Phase Verification
*   Verify using pytest layout collection that Screen 2 renders the left sidebar legend panel correctly.

---

## Phase 4: Screen 4 "Bye Bye" Splash view Addition & Delayed Exit Protocol

### 1. Proposed Changes
*   **Target Files**: 
    *   `src/homework_1/shared/gui/screen3.py` (Exit button routing)
    *   `src/homework_1/shared/gui/app.py` (Registering new exit page route `/exit`)
    *   `src/homework_1/shared/gui/callbacks_playground.py` (Delayed PID safe termination timer)
*   **Modifications**:
    *   In `app.py`, implement a routing path `/exit` mapping to a new visual Screen 4 layout displaying the text: **"Bye Bye, hope you enjoy!!"**
    *   In `callbacks_playground.py`, modify `handle_server_exit`.
        *   On click, redirect `pathname` immediately to `/exit`.
        *   Fire a non-blocking delayed timer using a background thread or `time.sleep` inside a spawned thread (e.g., 1.2 seconds) to let Dash finish rendering Screen 4 in the browser.
        *   Once the timer expires, safely kill the process using `os.kill(os.getpid(), signal.SIGTERM)`.
*   **Line Count Check**: Verify all layout and callbacks files remain strictly under **150 logical lines of code**.

### 2. Phase Verification
*   Add tests inside `tests/unit/test_gui.py` verifying `/exit` path routing returns Screen 4 layouts.
*   Assert that exit callbacks redirect to `/exit` and trigger a delayed server termination sequence.
*   Run `PYTHONPATH=src pytest` to confirm a 100% green verification status.
