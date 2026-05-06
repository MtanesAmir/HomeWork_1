# Dataset Generator Engine - Developer Tasks

## Phase 1: Configuration Setup
- [ ] Add configurations for 4 base sinus waves in `config/setup.json`
- [ ] Add `dataset_output_path` setting in `config/setup.json`

## Phase 2: Environment & Package Setup
- [ ] Create service module `src/homework_1/services/generator.py`
- [ ] Register and export new generator functions in `src/homework_1/services/__init__.py`

## Phase 3: Core Service Development (`generator.py`)
- [ ] Implement base signal preparation: `prepare_base_signals(noise_factor: float)`
  * Load configurations via `ConfigManager`
  * Generate 4 clean waves and 1 clean sum wave (10K samples each)
  * Generate 4 noised waves and 1 noised sum wave (10K samples each)
- [ ] Implement dataset row synthesis: `generate_dataset(num_rows: int, noise_factor: float)`
  * Loop `num_rows` times
  * Uniformly select random sliding index $X \in [0, 9990]$
  * Uniformly select random selector index $I \in [0, 3]$
  * Construct one-hot encoded `chosen_array` of size 4
  * Extract size 10 window from noised sum wave $\rightarrow$ `noise_sum_sample_list`
  * Extract size 10 window from target clean wave $I$ $\rightarrow$ `origin_sinus_sample_list`
  * Package row: Key = `chosen_array` + `noise_sum_sample_list` (size 14); Value = `origin_sinus_sample_list` (size 10)
- [ ] Implement database storage serialization: `save_dataset(dataset: dict, output_path: str)`
  * Serialize data dict to JSON format and write to disk
  * Ensure target directories are auto-created if missing

## Phase 4: SDK Interface Integration (`sdk.py`)
- [ ] Import generator services inside `src/homework_1/sdk/sdk.py`
- [ ] Expose `generate_and_save_dataset(num_rows: int, noise_factor: float)` in `HomeWorkSDK` wrapped inside the API Gatekeeper safety envelope

## Phase 5: Verification & Unit Tests (`tests/`)
- [ ] Create unit test suite `tests/unit/test_generator.py`
- [ ] Write test validating that configurations parse and load correctly
- [ ] Write test asserting `prepare_base_signals` outputs 10 lists of exactly 10K float samples
- [ ] Write test asserting dataset row dimensions:
  * Key list is exactly size 14
  * Value list is exactly size 10
  * Selector list is a valid size 4 one-hot vector
- [ ] Write test validating that `save_dataset` successfully serializes and writes a valid, parseable JSON file to disk
- [ ] Write programmatic test asserting that `src/homework_1/services/generator.py` strictly stays **under 150 logical lines of code** (excluding comments)

## Phase 6: E2E Bootstrap Integration Check
- [ ] Update `src/main.py` to bootstrap the SDK, run a 50-row dataset generation, and write the database output to disk
- [ ] Run `python3 src/main.py` and verify successful execution logs
