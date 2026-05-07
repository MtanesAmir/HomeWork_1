# Interactive Web Dashboard - Developer Tasks

## Phase 1: Environment Setup & Directory Initialization
- [ ] Initialize the dashboard subdirectory `src/homework_1/shared/gui/`
- [ ] Create empty packages layout files:
  * [ ] Create empty `src/homework_1/shared/gui/__init__.py`
  * [ ] Create empty `src/homework_1/shared/gui/screen1.py` (Wave configurations)
  * [ ] Create empty `src/homework_1/shared/gui/screen2.py` (Training curves)
  * [ ] Create empty `src/homework_1/shared/gui/screen3.py` (Playground panels)
  * [ ] Create empty `src/homework_1/shared/gui/app.py` (Routing and boot entrypoint)

## Phase 2: Screen 1 Development (`gui/screen1.py` - Sliders & Controls)
- [ ] Define the layout function `get_screen1_layout()`
  * [ ] Implement Left Sidebar parameters form (epochs, dataset size, noise, split percentage inputs)
  * [ ] Implement Sinusoid tune cards (4 cards, each containing sliders for Freq, Phase, and Amp)
  * [ ] Implement Plot grids (Plot A: clean waves overlay, Plot B: clean sum wave)
  * [ ] Implement "Let the models learn" submit button
  * [ ] Implement hidden split-validation warning alert banner
- [ ] Implement interactive Cartesian update callbacks:
  * [ ] Update individual component waves plot in real-time on slider moves
  * [ ] Update composite summed wave plot in real-time on slider moves
- [ ] Implement Split percentages verification callback:
  * [ ] Calculate split sum. Display warning alert if $train + val + test \ne 100.0$ and halt
  * [ ] If valid, trigger background sinus preparation and route to Screen 2

## Phase 3: Screen 2 Development (`gui/screen2.py` - Training Diagnostic Curves)
- [ ] Define the layout function `get_screen2_layout()`
  * [ ] Implement three Cartesian loss plots (FCN, RNN, LSTM grids)
  * [ ] Implement progress spinner, train epoch status ticker, and disabled "Lets play" button
  * [ ] Implement placeholder labels for Test Set MSE adjacent to each model grid
- [ ] Implement reactive metrics update callbacks:
  * [ ] Implement background interval callback pulling epoch loss metrics dynamically
  * [ ] Plot Training MSE and Validation MSE curves live on FCN, RNN, and LSTM grids
  * [ ] Upon completion of the final epoch, write the final Test Set MSE adjacent to the plots
  * [ ] Enable the **"Lets play"** button upon completion of all training runs

## Phase 4: Screen 3 & Exit Development (`gui/screen3.py` - Playground & Shutdown)
- [ ] Define the layout function `get_screen3_layout()`
  * [ ] Implement top Cartesian grid displaying the slice summed wave
  * [ ] Implement "Generate" button and continuous-dots visual toggle switches
  * [ ] Implement segmented component mask selectors **[1, 2, 3, 4]**
  * [ ] Implement three prediction plots grids (FCN, RNN, LSTM prediction windows)
  * [ ] Implement **"Exit"** safe termination button
- [ ] Implement playground prediction callbacks:
  * [ ] Retrieve random index $X \in [0, 9990]$ on **"Generate"** click, extract, and plot the summed wave slice
  * [ ] Whenever the slice is generated or the wave selector (1-4) changes, trigger prediction models in the backend
  * [ ] Render predictions on FCN, RNN, and LSTM plots, adhering to selected dots/line visual choices
- [ ] Implement exit shutdown callback:
  * [ ] Register callback for **"Exit"** button sending `SIGTERM` to the local server process

## Phase 5: Routing, Bootstrapping & Guide Setup
- [ ] Create router application inside `src/homework_1/shared/gui/app.py`
  * [ ] Set up the Dash client coordinator and import layout layers (`get_screen1_layout`, `get_screen2_layout`, `get_screen3_layout`)
  * [ ] Implement reactive multi-page layout router coordinating page navigation
- [ ] Update `src/main.py` entrypoint:
  * [ ] Add CLI arguments parser supporting `--mode ui` and `--port <port>`
  * [ ] Bootstrap the Dash app on the requested port when `--mode ui` is active
- [ ] Update [README.md](file:///Users/amirmt/Desktop/ME/Me/MSC-ComputerScience/2025-B/agent%20AI/hw1/HomeWork_1/README.md):
  * [ ] Add clear guides detailing how to run the project using `uv` and what URL to navigate to (e.g., `http://127.0.0.1:8050`)

## Phase 6: Automated Verification & E2E Testing
- [ ] Create automated GUI test module `tests/unit/test_gui.py`
- [ ] **Test Screen 1 validations**:
  * [ ] Test with invalid split percentages and verify warning banner is rendered
  * [ ] Test with correct split percentages and verify warning is dismissed
- [ ] **Test interactive slider callbacks**:
  * [ ] Mock wave component slider changes and verify Plotly figure data updates
- [ ] **Test async trainer curves**:
  * [ ] Mock metric epochs data streams and verify that figure MSE curves update
- [ ] **Test E2E callback flow**:
  * [ ] Simulate clicking **"Let the models learn"** $\rightarrow$ verify background dataset is successfully generated
  * [ ] Simulate training completion $\rightarrow$ verify button transitions to Playground
  * [ ] Simulate clicking **"Generate"** $\rightarrow$ verify size-14 key values predict clean outputs
  * [ ] Simulate clicking **"Exit"** $\rightarrow$ verify shutdown callback receives `SIGTERM`
- [ ] **Test code style constraints**:
  * [ ] Programmatically assert `screen1.py` is $\le 150$ logical lines (excluding comments/docstrings)
  * [ ] Programmatically assert `screen2.py` is $\le 150$ logical lines (excluding comments/docstrings)
  * [ ] Programmatically assert `screen3.py` is $\le 150$ logical lines (excluding comments/docstrings)
  * [ ] Programmatically assert `app.py` is $\le 150$ logical lines (excluding comments/docstrings)
  * [ ] Programmatically assert `test_gui.py` is $\le 150$ logical lines (excluding comments/docstrings)
