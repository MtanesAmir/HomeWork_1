# Implementation Plan: Dataset Generator Engine

This document outlines the technical roadmap for implementing the **Dataset Generator Engine** within the **HomeWork_1** package, ensuring complete compliance with architectural and modular standards.

---

## Phase 1: Setup & Configurations

### 1. Configuration Layer (`config/setup.json`)
We will extend `config/setup.json` to hold the configurations for the 4 base sinus waves, and a target output path for the completed dataset database:
*   **`waves`**: An array containing parameter dicts (amplitude, frequency, phase) for 4 separate waves.
*   **`dataset_output_path`**: The file path where the completed dataset will be stored (e.g., `results/dataset.json`).

### 2. Environment Setup
*   Verify that the `ConfigManager` in `src/homework_1/shared/config.py` handles parsing these new nested settings automatically.
*   Confirm the existence of the `results/` folder for saving output databases.

---

## Phase 2: Modular Domain Development

### 1. Directory & Namespace Registration
*   Create a new service file `src/homework_1/services/generator.py`.
*   Export generator functions in `src/homework_1/services/__init__.py` for clean package imports.
*   Expose pipeline methods in `src/homework_1/sdk/sdk.py` to keep the SDK as the single logic gateway.

### 2. Method Specifications (`generator.py`)

#### Method A: Base Signal Preparation (`prepare_base_signals`)
*   **Input**: `noise_factor` (float)
*   **Process**:
    *   Load the 4 wave configurations from the config file using `ConfigManager`.
    *   Generate 4 clean waves (10K samples each) and 1 clean sum wave (10K samples).
    *   Generate 4 noised waves (10K samples each) and 1 noised sum wave (10K samples).
*   **Output**: A dictionary containing the 10 base lists of size 10,000:
    *   `clean_waves`: `list[list[float]]` (size 4x10K)
    *   `clean_sum`: `list[float]` (size 10K)
    *   `noised_waves`: `list[list[float]]` (size 4x10K)
    *   `noised_sum`: `list[float]` (size 10K)

#### Method B: Dataset Map Generation (`generate_dataset`)
*   **Inputs**: `num_rows` (int), `noise_factor` (float)
*   **Process**:
    *   Invoke `prepare_base_signals(noise_factor)` to get the 10 base signal lists.
    *   Run a loop `num_rows` times. In each iteration:
        1.  Select a random index $X$ uniformly in range $[0, 9990]$.
        2.  Select a random target wave index $I \in [0, 3]$ uniformly.
        3.  Generate the one-hot `chosen_array` of size 4 (e.g. `[1.0, 0.0, 0.0, 0.0]` if $I=0$).
        4.  Slice a window of size 10 from `noised_sum` from index $X$ to $X+9$ $\rightarrow$ `noise_sum_sample_list`.
        5.  Slice a window of size 10 from `clean_waves[I]` from index $X$ to $X+9$ $\rightarrow$ `origin_sinus_sample_list`.
        6.  Assemble the labeled row:
            *   `key`: `chosen_array` (4) + `noise_sum_sample_list` (10) = List of size 14.
            *   `value`: `origin_sinus_sample_list` = List of size 10.
*   **Output**: A dictionary/map representing the dataset, e.g. `{"dataset": [{"key": [...], "value": [...]}, ...]}`.

#### Method C: Dataset Storage Serialization (`save_dataset`)
*   **Inputs**: `dataset` (dict), `output_path` (string/path)
*   **Process**:
    *   Serialize the dataset dictionary to disk in JSON format.
    *   Ensure parent directories are created automatically if they do not exist.

---

## Phase 3: Verification & Unit Tests

We will verify the implementation by writing automated unit tests in `tests/unit/test_generator.py`:

### Test Scenarios:
1.  **Configuration Loading Test**: Ensure the 4 waves and database path config are loaded correctly by the config helper.
2.  **Base Signals Dimensions Test**: Ensure `prepare_base_signals` outputs exactly 10 lists of size 10,000.
3.  **Dataset Row Dimension Assertions**:
    *   Generate a dataset map of 10 rows.
    *   Assert that the generated list has length 10.
    *   Assert that each row's key list has size exactly 14.
    *   Assert that each row's value list has size exactly 10.
    *   Assert that `chosen_array` is a valid one-hot vector (contains exactly one `1` and three `0`s).
4.  **Database Storage Check**:
    *   Verify that saving the dataset outputs a valid JSON file at the configured results path.
    *   Verify the JSON file can be parsed back without errors.
5.  **Logical Line Limit Assertion**:
    *   Ensure `src/homework_1/services/generator.py` stays strictly under **150 logical lines of code**.
