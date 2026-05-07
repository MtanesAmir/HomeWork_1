# First Feedback Revisions - Developer Tasks

## Phase 1: Screen 1 Slider Range Tuning (Frequency Scale)
- [ ] Locate the `get_sinusoid_card` layout helper inside `src/homework_1/shared/gui/screen1.py`
- [ ] Change the frequency slider's maximum value from `100.0` to `50.0`
- [ ] Ensure `screen1.py` stays strictly under the **150 logical lines limit**

## Phase 2: Deep Learning Engine Training Optimization (Test Set Isolation)
- [ ] Modify the training loop inside `src/homework_1/services/models/trainer.py`
  * [ ] Remove the test set evaluation `evaluate_loss(model, test_set)` from the active epoch training loop
  * [ ] Populate intermediate epochs `history["test_loss"]` list elements with `0.0` placeholders
  * [ ] Compute the test set loss exactly once, strictly at the completion of the final epoch, and write it to `history["test_loss"][-1]`
- [ ] Ensure `trainer.py` stays strictly under the **150 logical lines limit**

## Phase 3: LSTM Learning Convergence Optimization & Math Fixes
- [ ] Inspect the LSTM backpropagation parameter updates inside `src/homework_1/services/models/lstm/model.py`
  * [ ] Implement a robust, mathematically correct backpropagation sequence to guarantee convergence
  * [ ] Calculate gradients for all gates weights matrices (`W_f`, `W_i`, `W_c`, `W_o`, `W_y`) based on output target MSE errors
  * [ ] Apply gradient updates scaled by the learning rate to all gate weights and biases
  * [ ] Ensure `lstm/model.py` stays strictly under the **150 logical lines limit**

## Phase 4: Throttled Metrics Progress Diagnostics & Plotting
- [ ] Modify console logging in `src/homework_1/services/models/trainer.py`:
  * [ ] Output print statements strictly when `epoch == 1 or epoch % 10 == 0 or epoch == epochs`
- [ ] Modify Dash visual update callbacks inside `src/homework_1/shared/gui/callbacks_training.py`:
  * [ ] Restrict plotted coordinate arrays to update figures in **10-epoch increments**

## Phase 5: Back-End Multi-Threaded Parallel Model Training
- [ ] Implement parallel background execution inside `src/homework_1/shared/gui/callbacks_training.py`
  * [ ] Set up multi-threaded training executors utilizing Python's `threading.Thread` library
  * [ ] Click "Let the models learn" $\rightarrow$ launch separate background threads for FCN, RNN, and LSTM training concurrently
  * [ ] Implement a thread-safe shared global cache or store to record training metrics epoch-by-epoch
  * [ ] Asynchronously poll and fetch progress updates from these shared caches to redraw curves concurrently in real-time
- [ ] Ensure `callbacks_training.py` stays strictly under the **150 logical lines limit**

## Phase 6: Safe Exit Playground Boundary Protection
- [ ] Review all playground callbacks inside `src/homework_1/shared/gui/callbacks_playground.py`
  * [ ] Ensure `handle_slice_generation` and `evaluate_models_predictions` states are mathematically isolated from `handle_server_exit`
  * [ ] Confirm that process SIGTERM calls occur strictly when the red **"Exit Dashboard"** button is clicked
- [ ] Ensure `callbacks_playground.py` stays strictly under the **150 logical lines limit**

## Phase 7: Automated Verification & Pytest Suite Revisions
- [ ] Expose test cases inside `tests/unit/test_models.py` and `tests/unit/test_gui.py`:
  * [ ] **Test Frequency scale range**: Verify sinusoid sliders card maximum inputs do not exceed `50.0` Hz
  * [ ] **Test Test Loss Isolation**: Assert that intermediate epoch test losses in `history["test_loss"]` are placeholder `0.0`s, and only the final index holds the completed test set MSE
  * [ ] **Test LSTM Convergence**: Train LSTM for 30 epochs and assert programmatically that the final training loss decreases by at least 15% compared to initial loss (validating that the LSTM model learns as expected)
  * [ ] **Test Throttling figures updates**: Verify Plotly coordinate points update strictly in 10-epoch increments
  * [ ] **Test Parallel Training Threads**: Verify FCN, RNN, and LSTM background threads execute concurrently without blocking the main dashboard thread
  * [ ] **Test Sandbox Safety Boundaries**: Simulate multiple consecutive slice generation clicks and verify the visual server remains active without early shutdowns
  * [ ] **Test logical code lines constraints**: Assert that all modified layout, callbacks, models, and test files strictly stay **under the 150 logical lines of code limit**
