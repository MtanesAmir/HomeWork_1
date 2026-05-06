# Deep Learning Models Engine - Granular Developer Tasks

## Phase 1: Configuration Integration
- [ ] Extend `config/setup.json` with a dedicated `models` parameters block
  - [ ] Add `epochs` parameter (integer representing total train iterations)
  - [ ] Add dataset split percentages parameters:
    * `train_percentage` (float, representing train set ratio)
    * `val_percentage` (float, representing validation set ratio)
    * `test_percentage` (float, representing test set ratio)
  - [ ] Add list-based architecture mapping: `hidden_layers` (list of integers representing hidden layers widths, e.g., `[3, 5, 3]`)

## Phase 2: Environment & Package Initialization
- [ ] Initialize model directories under `src/homework_1/services/models/`:
  * [ ] Create directory `src/homework_1/services/models/fcn/`
  * [ ] Create directory `src/homework_1/services/models/rnn/`
  * [ ] Create directory `src/homework_1/services/models/lstm/`
- [ ] Create packages initialization files:
  * [ ] Create empty `src/homework_1/services/models/__init__.py`
  * [ ] Create empty `src/homework_1/services/models/fcn/__init__.py`
  * [ ] Create empty `src/homework_1/services/models/rnn/__init__.py`
  * [ ] Create empty `src/homework_1/services/models/lstm/__init__.py`
- [ ] Register package-level exports:
  * [ ] Expose FCN, RNN, and LSTM classes inside `src/homework_1/services/models/__init__.py`

## Phase 3: Core Domain Development (`services/models/`)

### 1. Fully Connected Network (FCN / MLP)
- [ ] Create `src/homework_1/services/models/fcn/model.py`
- [ ] Implement `FCNModel` class structure
  - [ ] Define constructor signature taking `input_size` (14), `hidden_layers` list, and `output_size` (10)
  - [ ] Implement dynamic layers generation builder mapping the `hidden_layers` list width profile
  - [ ] Implement forward pass logic taking key input (size 14) and returning predictions vector (size 10)

### 2. Recurrent Neural Network (RNN)
- [ ] Create `src/homework_1/services/models/rnn/model.py`
- [ ] Implement `RNNModel` class structure
  - [ ] Define constructor signature taking input size (14), hidden state shapes, and output size (10)
  - [ ] Implement dynamic recurrent layers builder mapping configured sequence states
  - [ ] Implement sequence feed-forward loop returning predictions vector (size 10)

### 3. Long Short-Term Memory (LSTM)
- [ ] Create `src/homework_1/services/models/lstm/model.py`
- [ ] Implement `LSTMModel` class structure
  - [ ] Define constructor signature taking input size (14), cell/hidden state shapes, and output size (10)
  - [ ] Implement gated cell dynamics (forget, input, output gates) dynamically constructed
  - [ ] Implement feed-forward sequence evaluations returning final prediction vector (size 10)

### 4. Centralized Trainer Module
- [ ] Create trainer coordinator service `src/homework_1/services/models/trainer.py`
- [ ] Implement splits validation utility `validate_splits(train_pct, val_pct, test_pct)`
  * [ ] Calculate sum $S = \text{train\_pct} + \text{val\_pct} + \text{test\_pct}$
  * [ ] Trigger a clear warning message using terminal print/logger if $S \ne 100.0$
- [ ] Implement `train_model(model, dataset, config)` pipeline execution:
  * [ ] Partition the input dataset map strictly according to configured percentages
  * [ ] Run epochs loop loaded from configuration
  * [ ] **Periodic Evaluation**: Every 10 epochs, calculate error percentage (MSE or similar) on Train, Validation, and Test sets
  * [ ] Print diagnostic status log to the terminal (e.g. `[Epoch 10/50] Train Loss: X.XX | Val Loss: Y.YY | Test Loss: Z.ZZ`)
  * [ ] Print final evaluation loss summary at completion of the final epoch

## Phase 4: SDK Integration (`sdk.py`)
- [ ] Import deep learning services in `src/homework_1/sdk/sdk.py`
- [ ] Expose `train_and_evaluate_fcn(self)` wrapper in `HomeWorkSDK` running under the rate-limiting Gatekeeper
- [ ] Expose `train_and_evaluate_rnn(self)` wrapper in `HomeWorkSDK` running under the rate-limiting Gatekeeper
- [ ] Expose `train_and_evaluate_lstm(self)` wrapper in `HomeWorkSDK` running under the rate-limiting Gatekeeper

## Phase 5: Verification & Unit Tests (`tests/`)
- [ ] Create test module `tests/unit/test_models.py`
- [ ] **Test splits validation warning**: Test with sum $\ne$ 100.0 and assert warning logs are printed to stdout
- [ ] **Test layer shape generator**:
  * [ ] Instantiate model with hidden layer config `[4, 8, 4]`
  * [ ] Assert that layers match depths and sizes programmatically
- [ ] **Test FCN training execution**:
  * [ ] Synthesize miniature dataset using generator service
  * [ ] Train FCN model for 20 epochs
  * [ ] Assert that loss decreases over epochs and outputs match target dimensions (size 10)
- [ ] **Test RNN training execution**:
  * [ ] Train RNN model for 20 epochs
  * [ ] Assert that recurrent training completes and loss decreases
- [ ] **Test LSTM training execution**:
  * [ ] Train LSTM model for 20 epochs
  * [ ] Assert that LSTM training completes and loss decreases
- [ ] **Test Code Style & Constraints**:
  * [ ] Write helper assertions to verify that `fcn/model.py` is $\le 150$ logical lines
  * [ ] Write helper assertions to verify that `rnn/model.py` is $\le 150$ logical lines
  * [ ] Write helper assertions to verify that `lstm/model.py` is $\le 150$ logical lines
  * [ ] Write helper assertions to verify that `trainer.py` is $\le 150$ logical lines

## Phase 6: E2E Bootstrap Integration Check
- [ ] Update `src/main.py` to:
  * [ ] Generate 100 dataset rows using the generator pipeline
  * [ ] Instantiate FCN, RNN, and LSTM networks
  * [ ] Trigger training boot for each model
  * [ ] Verify diagnostic prints (epoch 10, 20, etc.) show up in terminal stdout
- [ ] Run `python3 src/main.py` to confirm clean execution of all bootstrap processes
