# Product Requirements Document (PRD): First Feedback Revisions

## Overview
This PRD outlines targeted User Experience (UX) and architectural revisions to our Visual Web Dashboard and Deep Learning Models Engine. Based on first-hand interactive feedback, we are refining our parameter scales, isolating test evaluations to the end of training, transitioning epoch logging updates to 10-epoch increments, executing training runs in parallel threads to prevent dashboard freezing, and enforcing robust visual playground boundaries.

---

## Objectives
1. Refine visual scales for frequency parameters on Screen 1.
2. Optimise training pipelines to evaluate the test set strictly at the final epoch completion.
3. Throttle training dashboard update intervals to 10-epoch increments.
4. Implement multi-threaded parallel training execution in the background.
5. Reinforce playground state handlers to protect against accidental server shutdown signals.

---

## Detailed Functional Requirements

### 1. Sinusoid Sliders Frequency Scale Tuning (Screen 1)
*   **Requirement**: The frequency slider inputs on all 4 sinusoid cards **MUST** support a slightly lower, more granular frequency range for better wave visualization.
*   **Tuned Scale Range**: Adjust the slider limits from `[0.1, 100.0] Hz` down to a more focused range of `[0.1, 50.0] Hz` (or similar), keeping a step size of `0.1` for fine adjustments.
*   **Default Value**: Keep intuitive default values (e.g., sinusoid 1 = 5.0 Hz) within this lower range.

---

### 2. Test Set Evaluation Isolation (Deep Learning Engine)
*   **Requirement**: To align with training best practices and optimize execution speed, the training pipeline **MUST NOT** evaluate the test set during individual epoch loops.
*   **Evaluation Rules**:
    *   `train_neural_network` **MUST** calculate losses on the **Train Set** and **Validation Set** at each epoch.
    *   The **Test Set** evaluation **MUST** be computed exactly once, strictly at the very end of all epochs, once training concludes.

---

### 3. Throttled Diagnostics Plotting & Update Intervals (Screen 2)
*   **Requirement**: To reduce dashboard messaging overhead and render cleaner charts, Screen 2's plots **MUST** be updated in **10-epoch increments** instead of after every single epoch.
*   **Diagnostics Rules**:
    *   Loss/Accuracy curves (Train and Validation) on the FCN, RNN, and LSTM graphs **MUST** update their data and plot points after every 10 epochs.
    *   The final Test set loss/accuracy score **MUST** be written adjacent to the coordinate graphs strictly at the final epoch's completion.

---

### 4. Multi-Threaded Parallel Model Training (Screen 2 Back-End)
*   **Requirement**: To keep the dashboard fully responsive and allow FCN, RNN, and LSTM plots to update their progress concurrently, models **MUST** be trained in **parallel threads**.
*   **Architectural Rules**:
    *   Clicking "Let the models learn" **MUST** spin up separate background threads (or asynchronous workers) for FCN, RNN, and LSTM training loops.
    *   These parallel loops **MUST** update shared, thread-safe caches or stores holding current epoch metrics.
    *   The Dash client's interval callback **MUST** query these shared caches to update all three graphs concurrently in real-time.

---

### 5. Safe Exit Playground Boundary Protection (Screen 3)
*   **Requirement**: The dashboard **MUST NOT** trigger automated process exits. Server shutdown **MUST** occur strictly and exclusively when the user clicks the red **"Exit Dashboard"** button.
*   **Verification Checks**:
    *   Review all Screen 3 playground callbacks to ensure that clicking **"Generate"** does not intersect with or accidentally trigger the `handle_server_exit` callback.
    *   The `SIGTERM` signal callback **MUST** be fully isolated from playground updates, keeping the session open for repeated generations.
