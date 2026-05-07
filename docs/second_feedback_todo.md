# Second Feedback Revisions - Developer Tasks

## Phase 1: Sliced Sum Wave Dynamic Styling Callback (Screen 3 Input)
- [ ] Modify `handle_slice_generation` callback inside `src/homework_1/shared/gui/callbacks_playground.py`
  * [ ] Add `Input("toggle-dots-lines", "value")` as an input dependency
  * [ ] Modify `go.Scatter` trace to render with the selected style mode (`lines` or `markers`)
- [ ] Ensure `callbacks_playground.py` stays strictly under the **150 logical lines limit**

## Phase 2: RNN & LSTM Sequence Predictions Overlays Fixes
- [ ] Review FCN, RNN, and LSTM evaluation logic inside `src/homework_1/shared/gui/callbacks_playground.py`
  * [ ] Ensure one-hot selection masks and noised sum windows are parsed correctly to sequence inputs (size 14)
  * [ ] Fix prediction models output overlay traces to ensure predicted clean waves display correctly
- [ ] Ensure `callbacks_playground.py` stays strictly under the **150 logical lines limit**

## Phase 3: Metrics Legend Sidebar Panel (Screen 2 Left Side)
- [ ] Modify `get_screen2_layout()` inside `src/homework_1/shared/gui/screen2.py`
  * [ ] Implement a sidebar column on the left side of the screen
  * [ ] Add a styled card displaying description lists for each metric:
    * [ ] **Train Loss Curve (Blue Line)**: Average prediction error on training samples, showing how the model learns.
    * [ ] **Val Loss Curve (Orange Line)**: Unbiased prediction error on validation samples to detect overfitting.
    * [ ] **Test MSE Badge (Green Text)**: Final accuracy score on unseen holdout samples after training concludes.
- [ ] Ensure `screen2.py` stays strictly under the **150 logical lines limit**

## Phase 4: Screen 4 "Bye Bye" Splash View & Delayed Exit Protocol
- [ ] Expose Screen 4 visual splash page:
  * [ ] Create a visual helper function `get_screen4_layout()` inside `src/homework_1/shared/gui/screen3.py` or a new layout module
  * [ ] Implement Screen 4 layout displaying the text: **"Bye Bye, hope you enjoy!!"**
- [ ] Integrate Screen 4 routing and delayed termination:
  * [ ] Update the pathname router inside `src/homework_1/shared/gui/app.py` to map `/exit` to the Screen 4 layout
  * [ ] Modify the `handle_server_exit` callback inside `src/homework_1/shared/gui/callbacks_playground.py`
    * [ ] Redirect the browser `pathname` immediately to `/exit`
    * [ ] Spawn a delayed, non-blocking background thread timer (1.2 seconds) allowing Flask to finish rendering Screen 4 before calling the SIGTERM process signal
- [ ] Ensure all layout and callbacks files remain strictly under the **150 logical lines limit**

## Phase 5: Automated Verification & Pytest Suite Revisions
- [ ] Create test cases inside `tests/unit/test_gui.py` and `tests/unit/test_models.py`:
  * [ ] **Test Sliced Wave style toggle**: Verify that the composite sliced wave input figure reacts correctly to "lines" or "markers" modes
  * [ ] **Test predictions plots overlays**: Verify FCN, RNN, and LSTM prediction figures render exactly 10 output values
  * [ ] **Test Legend Panel layout**: Assert Screen 2 renders the left legend panel with correct descriptions
  * [ ] **Test Screen 4 exit splash**: Assert routing to `/exit` returns the Screen 4 layout
  * [ ] **Test Delayed shutdown execution**: Assert that clicking exit redirects pathname to `/exit` and initiates a delayed timer before process shutdown
  * [ ] **Test logical code lines constraints**: Assert that all modified layout, callbacks, and test files strictly stay **under the 150 logical lines of code limit**
