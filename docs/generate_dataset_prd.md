# Product Requirements Document (PRD): Dataset Generator Engine

## Overview
The Dataset Generator Engine is a pipeline built on top of our Sinus Wave Creation Engine. Its goal is to synthesize labeled datasets for machine learning or neural network training. The specific objective of this dataset is to train models to solve a blind-source separation or signal reconstruction task: identifying and extracting a clean, original wave component from a composite, noised signal mixture given a target selector.

---

## Objectives
1. Prepare base clean and noised sinus wave signals (original and composite summed waves).
2. Synthesize discrete dataset rows combining selector masks and noised composite windows as inputs (keys), mapped to clean original component windows as targets (values).
3. Provide a configurable pipeline method to generate a dataset map of arbitrary, developer-specified size.

---

## Detailed Dataset Generation Pipeline

### Part 1: Base Signal Preparation
The engine must initialize and populate **10 base lists** of exactly **10,000 (10K) float samples** each (representing 10 seconds of duration sampled at 1,000 Hz):

1.  **Load Wave Configurations**:
    *   Retrieve parameters (amplitude $A_i$, frequency $f_i$, phase $\phi_i$) for **4 separate waves** from the configuration file.
2.  **Generate 4 Original (Clean) Wave Lists**:
    *   Generate 10K clean samples for each wave: `clean_wave_1`, `clean_wave_2`, `clean_wave_3`, and `clean_wave_4`.
3.  **Generate 1 Composite Original Sum List**:
    *   Generate 10K samples representing the clean sum of all 4 waves using the wave summation service. Let's call this `clean_sum_wave`.
4.  **Generate 4 Noised Wave Lists**:
    *   Generate another set of 10K samples for the 4 waves, this time with a configurable `noise_factor` percentage added: `noised_wave_1`, `noised_wave_2`, `noised_wave_3`, and `noised_wave_4`.
5.  **Generate 1 Composite Noised Sum List**:
    *   Generate 10K samples representing the noised sum of all 4 waves using the wave summation service. Let's call this `noised_sum_wave`.

---

### Part 2: Labeled Dataset Row Synthesis

To generate a single data row (example) in the dataset:

1.  **Select a Random Slit Window ($X$)**:
    *   Generate a random integer index $X$ in the range $[0, 9990]$ (to allow slicing a window of size 10).
2.  **Create One-Hot Selection Mask (`chosen_array`)**:
    *   Synthesize a one-hot encoded list of size 4 containing exactly one `1` and three `0` values:
        *   `[1, 0, 0, 0]` $\rightarrow$ Selects Wave 1
        *   `[0, 1, 0, 0]` $\rightarrow$ Selects Wave 2
        *   `[0, 0, 1, 0]` $\rightarrow$ Selects Wave 3
        *   `[0, 0, 0, 1]` $\rightarrow$ Selects Wave 4
3.  **Extract input signal window (`noise_sum_sample_list`)**:
    *   Extract a slice of size 10 from the **Composite Noised Sum List (`noised_sum_wave`)** from index $X$ to $X+9$ (inclusive).
4.  **Extract target clean window (`origin_sinus_sample_list`)**:
    *   Based on the index of `1` in the one-hot `chosen_array`, extract a slice of size 10 from the corresponding **Original (Clean) Wave List** from index $X$ to $X+9$ (inclusive):
        *   If `chosen_array == [1, 0, 0, 0]`, slice `clean_wave_1`.
        *   If `chosen_array == [0, 1, 0, 0]`, slice `clean_wave_2`.
        *   If `chosen_array == [0, 0, 1, 0]`, slice `clean_wave_3`.
        *   If `chosen_array == [0, 0, 0, 1]`, slice `clean_wave_4`.
5.  **Assemble Labeled Data Row Structure**:
    *   **Key (Input)**: Concatenate the `chosen_array` (size 4) and the `noise_sum_sample_list` (size 10). Total key size = **14**.
    *   **Value (Label/Target)**: The `origin_sinus_sample_list` (size 10). Total value size = **10**.
    
    ```text
    Dataset Row Layout:
    Key (Size 14)                                     Value (Size 10)
    [One-hot Array (4)] + [Noised Sum Window (10)] => [Clean Original Window (10)]
    ```

---

## Requirements for Developers

1.  **Configurable Dataset Size**:
    *   Provide a pipeline class method `generate_dataset(num_rows: int) -> List[Dict[str, List[float]]]` (or matching structure) returning a collection of generated rows.
2.  **Randomization and Uniformity**:
    *   Ensure that $X$ is generated uniformly at random across the full bound $[0, 9990]$.
    *   Ensure the one-hot `chosen_array` selects wave indices 0 to 3 uniformly at random to provide balanced class labels in the training set.
3.  **Input Validation**:
    *   Raise exceptions if the configuration files are missing, or if `num_rows` is non-positive.
4.  **Documentation & Tests**:
    *   Implement complete unit tests verifying key and value shapes, uniform range bounds, and selector consistency.
