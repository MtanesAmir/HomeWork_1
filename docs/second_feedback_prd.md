# Product Requirements Document (PRD): Second Feedback Revisions

## Overview
This PRD defines targeted functional and visual updates based on the second round of interactive dashboard feedback. We are fixing Screen 3's input signal slice rendering to ensure it is affected by continuous-dots toggles, correcting prediction dimensions alignment for RNN and LSTM model prediction plots, and introducing a premium Screen 4 "Bye Bye" splash page shown to users immediately prior to server shutdown.

---

## Objectives
1. Fix Screen 3 sliced wave plotting to react to visual curve-style toggles.
2. Resolve sequence dimension alignments in RNN and LSTM prediction plots overlays on Screen 3.
3. Introduce a new Screen 4 exit splash view and coordinate process termination callbacks.

---

## Detailed Functional Requirements

### 1. Sliced Wave Plotting Styles (Screen 3 Input)
*   **Requirement**: The Cartesian grid displaying the composite noised input signal window (`plot-playground-sum-slice`) **MUST** react to the visual plotting style toggle inputs.
*   **Style Actions**:
    *   If the user selects **"Continuous lines"**, the sliced wave input **MUST** render as a continuous curve line.
    *   If the user selects **"Discrete dots"**, the sliced wave input **MUST** render as discrete data point markers.

---

### 2. RNN & LSTM Sequence Predictions Visual Fixes (Screen 3 Outputs)
*   **Requirement**: The prediction outputs for RNN and LSTM models on Screen 3 **MUST** render predictions correctly.
*   **Debugging / Alignment Fixes**:
    *   Ensure that the flat input slice values are mapped correctly to sequence dimensions in `callbacks_playground.py`.
    *   Assert that the output predictions from FCN, RNN, and LSTM are properly synchronized to their respective Cartesian plots figures.

---

### 3. Screen 4 Transition and Delayed Safe Exit Protocol
*   **Requirement**: Clicking the **"Exit Dashboard"** button **MUST NOT** terminate the process instantly. It **MUST** transition the client to a clean **Screen 4** view before shutting down.
*   **Screen 4 Visual Layout**:
    *   Display a premium visual header card: **"Bye Bye, hope you enjoy!!"**
    *   Provide a clean, modern sub-text: *"Visual dashboard has successfully shut down. You can safely close this tab."*
*   **Delayed Termination Logic**:
    *   Upon clicking **"Exit Dashboard"**, the client routes instantly to `/exit` (Screen 4).
    *   The server **MUST** initiate a brief, non-blocking delayed shutdown timer (e.g., 1.0 - 1.5 seconds) to allow Flask/Dash to complete the page transition and render Screen 4 on the browser.
    *   Once the delay expires, the server process is safely terminated via `os.kill(os.getpid(), signal.SIGTERM)`.
