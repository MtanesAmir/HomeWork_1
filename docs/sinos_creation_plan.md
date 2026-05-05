# Implementation Plan: Sinus Wave Creation Engine

This document outlines the implementation roadmap for adding standard and composite sinus wave generation services with optional noise injection to the **HomeWork_1** package.

---

## Phase 1: Architectural Analysis & Setup

### Alignment with Guidelines
Adhering to the **Guidelines for Writing Professional Software (V3)**, we will isolate the mathematical domain logic from the entrypoint client layer:
1. **Service Domain Layer (`src/homework_1/services/sinus.py`)**: Houses the core object-oriented model `SinusWave` and mathematical generation services.
2. **SDK Interface Layer (`src/homework_1/sdk/sdk.py`)**: Exposes clean wrapper functions to external clients, maintaining the SDK as the single point of entry.
3. **Boilerplate packaging (`src/homework_1/services/__init__.py`)**: Exports new service models for neat namespace inclusion.

---

## Phase 2: Object-Oriented Design & Development

### Guideline & Code Constraints
* **Modularity**: High cohesion, low coupling. All sinus logic resides inside `homework_1.services.sinus`.
* **Line Limit Constraint**: The total implementation in `sinus.py` **MUST NOT exceed 140 lines of logical code** (excluding blank lines and docstrings).
* **Shared Code Strategy**: To satisfy the line limit, clean samples (Method 1) and noised samples (Method 2) **must share a single generator core**, using a default `noise_factor = 0.0`.

### Class Design: `SinusWave`
A single sinus wave represents an isolated mathematical building block:

```python
class SinusWave:
    """Represents a single mathematical sine wave: y(t) = A * sin(2*pi*f*t + phi)."""
    
    def __init__(self, amplitude: float, frequency: float, phase: float):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def evaluate(self, t: float) -> float:
        """Computes the instantaneous clean amplitude at time t."""
        ...
```

### The 4 Core Method Specifications

#### Method 1 & 2: Single Wave Sample Generation (With & Without Noise)
Exposed to the SDK as a single shared generator function:
* **Inputs**: 
  * `amplitude` ($A$): Peak deviation (float)
  * `frequency` ($f$): Oscillations per second in Hz (float)
  * `phase` ($\phi$): Starting phase shift at $t=0$ (float)
  * `samples_per_second` ($S_r$): Sampling rate (int)
  * `seconds` ($D$): Total signal duration (float)
  * `noise_factor` (optional, float, default = `0.0`)
* **Formulations**:
  * Total samples to generate: $K = \text{samples\_per\_second} \times \text{seconds}$.
  * Timesteps: $t_k = \frac{k}{S_r}$ for $k \in [0, K-1]$.
  * **Method 1 (Clean)**: If `noise_factor == 0.0`, value is $X = A \sin(2\pi f t_k + \phi)$.
  * **Method 2 (Noised)**: If `noise_factor > 0.0`, value is random-noised in range $[X \times (1 - \text{noise\_factor}), X \times (1 + \text{noise\_factor})]$. 
    * Implementation: $X_{noised} = X \times (1 + \delta)$ where $\delta \sim \mathcal{U}(-\text{noise\_factor}, \text{noise\_factor})$.
* **Output**: A `list[float]` of length $K$ (e.g. 10 seconds at 1000 samples/sec = list of 10,000 floats).

#### Method 3: List Element-Wise Summation
Combines pre-computed samples from multiple waves:
* **Inputs**: `lists`: A list of up to 4 lists of floats representing sinus wave samples. All input lists must be of identical length.
* **Behavior**: Computes the element-wise summation at each index.
* **Output**: A single `list[float]` of the same length.

#### Method 4: Parametric Wave Summation (Composite Signal Synthesis)
Enables mathematical summation prior to generating samples:
* **Inputs**:
  * `waves`: A list of up to 4 `SinusWave` instances.
  * `samples_per_second` (int)
  * `seconds` (float)
  * `noise_factor` (optional, float, default = `0.0`)
* **Behavior**: Evaluates each wave mathematically at timestep $t_k$, sums their amplitudes, and optionally applies noise to the final sum.
* **Output**: A single `list[float]` of length $K$.

---

## Phase 3: Verification & Test Suite Design

To ensure absolute correctness, we will implement unit tests under [tests/unit/test_sinus.py](file:///Users/amirmt/Desktop/ME/Me/MSC-ComputerScience/2025-B/agent%20AI/hw1/HomeWork_1/tests/unit/test_sinus.py):

### Test Scenarios:
1. **Mathematical Integrity**:
   * Verify $y(0) = A \sin(\phi)$.
   * Verify $y(t) = A$ at peak values.
2. **Noised Bounds Compliance**:
   * Generate samples with `noise_factor = 0.05` and assert that all generated values lie strictly in range $[y(t) \times 0.95, y(t) \times 1.05]$.
3. **Element-wise Summation**:
   * Verify summing lists $[1.0, 2.0]$ and $[3.0, 4.0]$ correctly returns $[4.0, 6.0]$.
   * Validate error handling when lists of mismatched lengths are provided.
4. **Parametric Multi-Wave Summation**:
   * Verify that summing waves $y_1(t) = 1\sin(2\pi t)$ and $y_2(t) = 2\sin(2\pi t)$ generates identical output to $y(t) = 3\sin(2\pi t)$.
5. **Logical Line Limit Verification**:
   * Verify that the logical line count of `homework_1/services/sinus.py` does not exceed **140 lines** (excluding comments/docstrings).
