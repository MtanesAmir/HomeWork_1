# Deep Learning Models Engine - Granular Developer Tasks

## Phase 1: Configuration Integration
- [x] Extend `config/setup.json` with a dedicated `models` parameters block
  - [x] Add `epochs` parameter (integer representing total train iterations)
  - [x] Add dataset split percentages parameters:
    * [x] `train_percentage` (float, representing train set ratio)
    * [x] `val_percentage` (float, representing validation set ratio)
    * [x] `test_percentage` (float, representing test set ratio)
  - [x] Add list-based architecture mapping: `hidden_layers` (list of integers representing hidden layers widths, e.g., `[3, 5, 3]`)

## Phase 2: Environment & Package Initialization
- [x] Initialize model directories under `src/homework_1/services/models/`:
  * [x] Create directory `src/homework_1/services/models/fcn/`
  * [x] Create directory `src/homework_1/services/models/rnn/`
  * [x] Create directory `src/homework_1/services/models/lstm/`
- [x] Create packages initialization files:
  * [x] Create empty `src/homework_1/services/models/__init__.py`
  * [x] Create empty `src/homework_1/services/models/fcn/__init__.py`
  * [x] Create empty `src/homework_1/services/models/rnn/__init__.py`
  * [x] Create empty `src/homework_1/services/models/lstm/__init__.py`
- [x] Register package-level exports:
  * [x] Expose FCN, RNN, and LSTM classes inside `src/homework_1/services/models/__init__.py`

## Phase 3: Core Domain Development (`services/models/`)

### 1. Fully Connected Network (FCN / MLP)
- [x] Create `src/homework_1/services/models/fcn/model.py`
- [x] Implement `FCNModel` class structure
  - [x] Define constructor signature taking `input_size` (14), `hidden_layers` list, and `output_size` (10)
  - [x] Implement dynamic layers generation builder mapping the `hidden_layers` list width profile
  - [x] Implement forward pass logic taking key input (size 14) and returning predictions vector (size 10)

### 2. Recurrent Neural Network (RNN)
- [x] Create `src/homework_1/services/models/rnn/model.py`
- [x] Implement `RNNModel` class structure
  - [x] Define constructor signature taking input size (14), hidden state shapes, and output size (10)
  - [x] Implement dynamic recurrent layers builder mapping configured sequence states
  - [x] Implement sequence feed-forward loop returning predictions vector (size 10)

### 3. Long Short-Term Memory (LSTM)
- [x] Create `src/homework_1/services/models/lstm/model.py`
- [x] Implement `LSTMModel` class structure
  - [x] Define constructor signature taking input size (14), cell/hidden state shapes, and output size (10)
  - [x] Implement gated cell dynamics (forget, input, output gates) dynamically constructed
  - [x] Implement feed-forward sequence evaluations returning final prediction vector (size 10)

### 4. Centralized Trainer Module
- [x] Create trainer coordinator service `src/homework_1/services/models/trainer.py`
- [x] Implement splits validation utility `validate_splits(train_pct, val_pct, test_pct)`
  * [x] Calculate sum $S = \text{train\_pct} + \text{val\_pct} + \text{test\_pct}$
  * [x] Trigger a clear warning message using terminal print/logger if $S \ne 100.0$
- [x] Implement `train_model(model, dataset, config)` pipeline execution:
  * [x] Partition the input dataset map strictly according to configured percentages
  * [x] Run epochs loop loaded from configuration
  * [x] **Periodic Evaluation**: Every 10 epochs, calculate error percentage (MSE or similar) on Train, Validation, and Test sets
  * [x] Print diagnostic status log to the terminal (e.g. `[Epoch 10/50] Train Loss: X.XX | Val Loss: Y.YY | Test Loss: Z.ZZ`)
  * [x] Print final evaluation loss summary at completion of the final epoch

## Phase 4: SDK Integration (`sdk.py`)
- [x] Import deep learning services in `src/homework_1/sdk/sdk.py`
- [x] Expose `train_fcn(self)` wrapper in `HomeWorkSDK` running under the rate-limiting Gatekeeper
- [x] Expose `train_rnn(self)` wrapper in `HomeWorkSDK` running under the rate-limiting Gatekeeper
- [x] Expose `train_lstm(self)` wrapper in `HomeWorkSDK` running under the rate-limiting Gatekeeper

## Phase 5: Verification & Unit Tests (`tests/`)
- [x] Create test module `tests/unit/test_models.py`
- [x] **Test splits validation warning**: Test with sum $\ne$ 100.0 and assert warning logs are printed to stdout
- [x] **Test layer shape generator**:
  * [x] Instantiate model with hidden layer config `[4, 8, 4]`
  * [x] Assert that layers match depths and sizes programmatically
- [x] **Test FCN training execution**:
  * [x] Synthesize miniature dataset using generator service
  * [x] Train FCN model for 20 epochs
  * [x] Assert that loss decreases over epochs and outputs match target dimensions (size 10)
- [x] **Test RNN training execution**:
  * [x] Train RNN model for 20 epochs
  * [x] Assert that recurrent training completes and loss decreases
- [x] **Test LSTM training execution**:
  * [x] Train LSTM model for 20 epochs
  * [x] Assert that LSTM training completes and loss decreases
- [x] **Test Code Style & Constraints**:
  * [x] Write helper assertions to verify that `fcn/model.py` is $\le 150$ logical lines
  * [x] Write helper assertions to verify that `rnn/model.py` is $\le 150$ logical lines
  * [x] Write helper assertions to verify that `lstm/model.py` is $\le 150$ logical lines
  * [x] Write helper assertions to verify that `trainer.py` is $\le 150$ logical lines

## Phase 6: E2E Bootstrap Integration Check
- [x] Update `src/main.py` to:
  * [x] Generate 100 dataset rows using the generator pipeline
  * [x] Instantiate FCN, RNN, and LSTM networks
  * [x] Trigger training boot for each model
  * [x] Verify diagnostic prints (epoch 10, 20, etc.) show up in terminal stdout
- [x] Run `python3 src/main.py` to confirm clean execution of all bootstrap processes

