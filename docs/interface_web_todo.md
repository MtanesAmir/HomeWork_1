# Interactive Web Dashboard - Developer Tasks

## Phase 1: Environment Setup & Directory Initialization
- [x] Initialize the dashboard subdirectory `src/homework_1/shared/gui/`
- [x] Create empty packages layout files:
  * [x] Create empty `src/homework_1/shared/gui/__init__.py`
  * [x] Create empty `src/homework_1/shared/gui/screen1.py` (Wave configurations)
  * [x] Create empty `src/homework_1/shared/gui/screen2.py` (Training curves)
  * [x] Create empty `src/homework_1/shared/gui/screen3.py` (Playground panels)
  * [x] Create empty `src/homework_1/shared/gui/app.py` (Routing and boot entrypoint)

## Phase 2: Screen 1 Development (`gui/screen1.py` - Sliders & Controls)
- [x] Define the layout function `get_screen1_layout()`
  * [x] Implement Left Sidebar parameters form (epochs, dataset size, noise, split percentage inputs)
  * [x] Implement Sinusoid tune cards (4 cards, each containing sliders for Freq, Phase, and Amp)
  * [x] Implement Plot grids (Plot A: clean waves overlay, Plot B: clean sum wave)
  * [x] Implement "Let the models learn" submit button
  * [x] Implement hidden split-validation warning alert banner
- [x] Implement interactive Cartesian update callbacks:
  * [x] Update individual component waves plot in real-time on slider moves
  * [x] Update composite summed wave plot in real-time on slider moves
- [x] Implement Split percentages verification callback:
  * [x] Calculate split sum. Display warning alert if $train + val + test \ne 100.0$ and halt
  * [x] If valid, trigger background sinus preparation and route to Screen 2

## Phase 3: Screen 2 Development (`gui/screen2.py` - Training Diagnostic Curves)
- [x] Define the layout function `get_screen2_layout()`
  * [x] Implement three Cartesian loss plots (FCN, RNN, LSTM grids)
  * [x] Implement progress spinner, train epoch status ticker, and disabled "Lets play" button
  * [x] Implement placeholder labels for Test Set MSE adjacent to each model grid
- [x] Implement reactive metrics update callbacks:
  * [x] Implement background interval callback pulling epoch loss metrics dynamically
  * [x] Plot Training MSE and Validation MSE curves live on FCN, RNN, and LSTM grids
  * [x] Upon completion of the final epoch, write the final Test Set MSE adjacent to the plots
  * [x] Enable the **"Lets play"** button upon completion of all training runs

## Phase 4: Screen 3 & Exit Development (`gui/screen3.py` - Playground & Shutdown)
- [x] Define the layout function `get_screen3_layout()`
  * [x] Implement top Cartesian grid displaying the slice summed wave
  * [x] Implement "Generate" button and continuous-dots visual toggle switches
  * [x] Implement segmented component mask selectors **[1, 2, 3, 4]**
  * [x] Implement three prediction plots grids (FCN, RNN, LSTM prediction windows)
  * [x] Implement **"Exit"** safe termination button
- [x] Implement playground prediction callbacks:
  * [x] Retrieve random index $X \in [0, 9990]$ on **"Generate"** click, extract, and plot the summed wave slice
  * [x] Whenever the slice is generated or the wave selector (1-4) changes, trigger prediction models in the backend
  * [x] Render predictions on FCN, RNN, and LSTM plots, adhering to selected dots/line visual choices
- [x] Implement exit shutdown callback:
  * [x] Register callback for **"Exit"** button sending `SIGTERM` to the local server process

## Phase 5: Routing, Bootstrapping & Guide Setup
- [x] Create router application inside `src/homework_1/shared/gui/app.py`
  * [x] Set up the Dash client coordinator and import layout layers (`get_screen1_layout`, `get_screen2_layout`, `get_screen3_layout`)
  * [x] Implement reactive multi-page layout router coordinating page navigation
- [x] Update `src/main.py` entrypoint:
  * [x] Add CLI arguments parser supporting `--mode ui` and `--port <port>`
  * [x] Bootstrap the Dash app on the requested port when `--mode ui` is active
- [x] Update [README.md](file:///Users/amirmt/Desktop/ME/Me/MSC-ComputerScience/2025-B/agent%20AI/hw1/HomeWork_1/README.md):
  * [x] Add clear guides detailing how to run the project using `uv` and what URL to navigate to (e.g., `http://127.0.0.1:8050`)

## Phase 6: Automated Verification & E2E Testing
- [x] Create automated GUI test module `tests/unit/test_gui.py`
- [x] **Test Screen 1 validations**:
  * [x] Test with invalid split percentages and verify warning banner is rendered
  * [x] Test with correct split percentages and verify warning is dismissed
- [x] **Test interactive slider callbacks**:
  * [x] Mock wave component slider changes and verify Plotly figure data updates
- [x] **Test async trainer curves**:
  * [x] Mock metric epochs data streams and verify that figure MSE curves update
- [x] **Test E2E callback flow**:
  * [x] Simulate clicking **"Let the models learn"** $\rightarrow$ verify background dataset is successfully generated
  * [x] Simulate training completion $\rightarrow$ verify button transitions to Playground
  * [x] Simulate clicking **"Generate"** $\rightarrow$ verify size-14 key values predict clean outputs
  * [x] Simulate clicking **"Exit"** $\rightarrow$ verify shutdown callback receives `SIGTERM`
- [x] **Test code style constraints**:
  * [x] Programmatically assert `screen1.py` is $\le 150$ logical lines (excluding comments/docstrings)
  * [x] Programmatically assert `screen2.py` is $\le 150$ logical lines (excluding comments/docstrings)
  * [x] Programmatically assert `screen3.py` is $\le 150$ logical lines (excluding comments/docstrings)
  * [x] Programmatically assert `app.py` is $\le 150$ logical lines (excluding comments/docstrings)
  * [x] Programmatically assert `test_gui.py` is $\le 150$ logical lines (excluding comments/docstrings)
