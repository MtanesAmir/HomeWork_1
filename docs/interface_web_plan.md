# Implementation Plan: Interactive Signal Reconstruction Web Dashboard

This document outlines the visual implementation roadmap for building a three-screen **Dash/Plotly web application** integrated on top of our mathematical, dataset, and neural network training services.

---

## Phase 1: Architecture, Tech Stack & Bootstrapping

### Tech Stack Choice
We will construct the visual dashboard utilizing **Dash by Plotly** (with **Dash Bootstrap Components - DBC** for rich aesthetics and dark mode theme).
*   **Why Dash**: Dash matches Python perfectly, allows fast Cartesian grid plotting natively, provides reactive callbacks for live slider updates, and compiles cleanly without massive web frames.
*   **Line count rule compliance**: Dash layout code can get verbose. To respect the **150 logical lines of code limit** per file, each screen's visual layout **MUST** be isolated in a separate module inside `src/homework_1/shared/gui/`:
    *   `gui/screen1.py` (Wave configuration and sliders)
    *   `gui/screen2.py` (Training progress Cartesian curves)
    *   `gui/screen3.py` (Playground and reconstruction comparison)
    *   `gui/app.py` (Coordinator routing and entrypoint)

---

## Phase 2: Development & Screen-by-Screen Milestones

### Phase 2.1: Screen 1 (Parameter Control Panel)
*   **Layout**:
    *   *Left Panel*: Sidebar inputs for epochs count, dataset size, noise, and train/val/test percentages.
    *   *Middle Top Cards*: 4 distinct sinusoid control cards with default values and sliders for frequency, phase, and amplitude.
    *   *Right Plots Grid*:
        1.  Plot A (clean sinus wave components overlaid on the same coordinate system).
        2.  Plot B (the composite clean summed signal continuous wave).
*   **Callbacks**:
    *   Moving any slider triggers the sinus wave generator domain models in real-time, redrawing Plots A and B.
*   **Validations & Triggers**:
    *   Clicking **"Let the models learn"** triggers a split verification.
    *   *Verification logic*: If `train_pct + val_pct + test_pct != 100.0`, display an error alert banner on Screen 1 and halt execution.
    *   *Success logic*: If valid, trigger the 10 base lists preparation and dataset generator in the background, then route the client to Screen 2.

### Phase 2.2: Screen 2 (Asynchronous Diagnostic Training Curves)
*   **Layout**:
    *   Three distinct Cartesian grids mapping **FCN**, **RNN**, and **LSTM** MSE losses respectively.
    *   An interactive progress bar and status ticker (e.g., `Training epoch 24/50`).
    *   Displaying **Test Set MSE** score adjacent to the corresponding model's Cartesian graph at final completion.
*   **Callbacks**:
    *   An asynchronous interval callback queries the training coordinator dynamically. Plot the Training MSE and Validation MSE curves after each epoch as they are computed.
    *   Upon completion of all three models, unlock the **"Lets play"** button.

### Phase 2.3: Screen 3 (Signal Reconstruction Playground) & Exit Protocol
*   **Layout**:
    *   *Top Plot*: Interactive Cartesian graph plotting `sum origin list` Continuous Curve or Discrete Dots based on toggle checks.
    *   *Control Panels*:
        *   **"Generate"** button picking random $X \in [0, 9990]$.
        *   Segmented component mask selector cards **[1, 2, 3, 4]** representing one-hot selection arrays.
        *   Toggles switching between continuous lines or discrete samples.
    *   *Prediction Plots Grid*: Three grids displaying predictions from FCN, RNN, and LSTM overlaid with option selections.
    *   *Exit Button*: An **"Exit"** button positioned prominently at the bottom of Screen 3.
*   **Callbacks**:
    *   Clicking **"Generate"** or modifying selectors triggers the deep learning prediction models in the backend, updating all three prediction grids.
    *   Clicking the **"Exit"** button triggers a callback calling `os.kill(os.getpid(), signal.SIGTERM)` to safely shutdown the Dash server and terminate the service.

---

## Phase 3: Automated Verification & End-to-End Testing

We will implement a rigorous automated visual test suite in `tests/unit/test_gui.py`:

### Test Scenarios:
1.  **Screen 1 Layout & Verification Test**:
    *   Verify default wave parameter models parse correctly.
    *   Submit splits summing to 95% and assert that the verification alert message is visible in the layout.
    *   Submit splits summing to 100% and assert that the warning is successfully dismissed.
2.  **Interactive Slider callbacks Test**:
    *   Trigger wave slider update events and assert that Plots A and B receive correct data arrays.
3.  **Asynchronous Trainer Updates Test**:
    *   Mock training metrics streams and assert that Cartesian grids receive updated coordinates data periodically.
4.  **E2E User Flow Test (Simulated Callback Executions)**:
    *   Instantiate the Dash client router.
    *   Simulate clicking **"Let the models learn"** $\rightarrow$ verify background datasets are generated.
    *   Simulate training metrics stream $\rightarrow$ verify transition to playground once completed.
    *   Simulate clicking **"Generate"** $\rightarrow$ assert key/value size-14 predictions evaluate successfully.
    *   Simulate clicking **"Exit"** $\rightarrow$ assert shutdown callback receives the termination signal.
5.  **Code Line Limits Constraint**:
    *   Assert that `screen1.py`, `screen2.py`, `screen3.py`, `app.py`, and `test_gui.py` **each strictly stay under 150 logical code lines**.
