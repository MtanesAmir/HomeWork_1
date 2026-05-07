# Product Requirements Document (PRD): Interactive Signal Reconstruction Web Dashboard

## Overview
The Signal Reconstruction Web Dashboard is a state-of-the-art, interactive visual application. It acts as the frontend interface for our core mathematical engine, dataset generator, and deep learning models. Through a clean multi-screen dashboard, users can dynamically tune sinus wave components, trigger pipeline dataset synthesis, train RNN, LSTM, and FCN architectures in the background with real-time diagnostic plotting, and interactively play with the models to evaluate blind-source separation and clean signal reconstruction.

---

## Core Platform Requirements
1. **Local Server Launch**:
   * The system **MUST** launch local servers instantly utilizing the `uv` package manager tool.
   * Command execution: `uv run python src/main.py --mode ui --port <port>` (or equivalent).
   * The interface **MUST** be fully responsive, visual, and accessible via the browser on `localhost:<port>`.
2. **Background Processing & Non-blocking State**:
   * Background pipelines (dataset generation and models training) **MUST** run asynchronously.
   * The UI **MUST** remain fully interactive and update progress dynamically without browser freezing.

---

## Detailed Screen Workflows

### Screen 1: Wave Configuration & Pipeline Parameter Tuning

The first screen is the control dashboard. It provides detailed parameter inputs and live plots:

#### 1. Parameter Panels (Left Sidebar)
The sidebar allows tuning all configurations for our synthesis and training pipeline:
*   **Epochs Count**: (Integer input, default = 50)
*   **Dataset Size**: (Integer input, default = 500 rows)
*   **Noise Percentage**: (Float slider/input, range = `[0.0, 0.5]`, default = 0.05)
*   **Dataset Split Ratios**:
    *   `train_percentage` (Float, default = 70.0%)
    *   `val_percentage` (Float, default = 15.0%)
    *   `test_percentage` (Float, default = 15.0%)

#### 2. Sinusoid Control Cards (Top Row)
Provides 4 distinct cards matching the design patterns from the image layout:
*   Each of the **4 Sinusoids** features three sliders (pre-populated with default values):
    *   **Freq (Hz)**: Range `[0.1, 100]`, float slider.
    *   **Phase (rad)**: Range `[-6.28, 6.28]`, float slider.
    *   **Amp**: Range `[0, 2.0]`, float slider.
*   **Default values**:
    *   *Sinusoid 1*: $A=1.0, f=5.0, \phi=0.0$
    *   *Sinusoid 2*: $A=1.5, f=10.0, \phi=0.5$
    *   *Sinusoid 3*: $A=2.0, f=15.0, \phi=1.0$
    *   *Sinusoid 4*: $A=0.5, f=20.0, \phi=1.5$

#### 3. Real-time Cartesian Coordinate System Visuals (Right Panel)
*   **Plot A: Individual Wave Components**: Plots all 4 active sinus waves over a 10-second Cartesian grid, plotted on the **same coordinate system** with distinctive colors.
*   **Plot B: Composite Sum Wave**: Plots the clean element-wise summation of the 4 components on a separate grid immediately below.
*   *Interactivity*: Adjusting any slider on the cards **MUST** immediately update both Plots A and B in real-time.

#### 4. Trigger Verification and Execution
*   Positioned at the bottom-middle of the screen is a prominent action button: **"Let the models learn"**.
*   **Split Verification Check**: When clicked, the system **MUST** verify the splits sum:
    *   If $train\_pct + val\_pct + test\_pct \ne 100.0$, halt execution, display a warning overlay, and prevent transitioning to Screen 2.
*   If splits are correct, the system **MUST** trigger the background pipeline:
    1. Generate the 10 base arrays of 10K samples using our sinus creation tools.
    2. Generate the training database map using our dataset generator tools.
    3. Transition to **Screen 2** and begin training FCN, RNN, and LSTM.

---

### Screen 2: Asynchronous Model Training & Diagnostics Progress

Screen 2 displays progress, periodic logs, and Cartesian metrics:

#### 1. Real-time Loss Curves (Three Cartesian Grids)
Displays three distinct plots—one for **FCN**, one for **RNN**, and one for **LSTM**.
*   **Plots Content**: For each model, plot the **Training MSE** and **Validation MSE** curves dynamically.
*   **Update Frequency**: The UI **MUST** refresh and plot updated MSE values **after each epoch** (or periodic increments) as updates are completed in the background.
*   *Visual Indicator*: Shows a clean, premium loading spinner and training epoch counter (e.g. `Training: Epoch 24/50`).

#### 2. Final Test Metrics Evaluation
*   Upon completion of the final epoch for each model, calculate the **Test Set MSE**.
*   Display the Test MSE score clearly as a badge or highlighted text **immediately adjacent to the model's Cartesian graph**.
*   Provide a prominent button in the bottom-middle: **"Lets play"** (disabled during training, enabled immediately once all 3 models complete).

---

### Screen 3: Interactive Signal Reconstruction Playground

Screen 3 provides the interactive blind-source separation playground to test and demonstrate the trained models:

#### 1. Generator Window Slice Panel
*   Provides a button: **"Generate"**.
*   **Behavior**: Generates a random index $X \in [0, 9990]$ and extracts a window of size 10 from the **Composite Original Sum List** (from index $X$ to $X+9$).
*   **Visual Plot**: Plots this `sum origin list` on a Cartesian grid. Features a toggle to display it as **discrete dots** or a **connected continuous wave**.

#### 2. One-Hot Component Selector Masks
*   Provides a segmented button bar or choice card with options **[1, 2, 3, 4]** representing the wave target:
    *   Choosing **1** $\rightarrow$ `[1, 0, 0, 0]` (Wave 1)
    *   Choosing **2** $\rightarrow$ `[0, 1, 0, 0]` (Wave 2)
    *   Choosing **3** $\rightarrow$ `[0, 0, 1, 0]` (Wave 3)
    *   Choosing **4** $\rightarrow$ `[0, 0, 0, 1]` (Wave 4)

#### 3. Real-time Prediction Dashboards (Three Model Grids)
Provides three side-by-side (or stacked) Cartesian plots—one for each network architecture (FCN, RNN, LSTM).
*   **Evaluation Logic**: Whenever the user clicks **"Generate"** or changes the sinusoid selector (1-4):
    1. Send the active `sum origin list` and target `one-hot selector mask` to the FCN, RNN, and LSTM models.
    2. Retrieve the predicted 10-sample reconstruction array from each model.
    3. Plot the prediction array on the corresponding model grid.
*   **Visual Toggles**: Each model's grid **MUST** support a checkbox/toggle to switch between **dots (samples representation)** or **connected continuous signals**.
