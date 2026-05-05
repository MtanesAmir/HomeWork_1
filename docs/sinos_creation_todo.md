# Sinus Wave Creation Engine - Developer Tasks

## Phase 1: Environment & Setup
- [x] Create service module `src/homework_1/services/sinus.py`
- [x] Update package exports in `src/homework_1/services/__init__.py` to expose `SinusWave` and generator helpers

## Phase 2: Core Domain Development (`sinus.py`)
- [x] Implement `SinusWave` class with parameters: `amplitude` ($A$), `frequency` ($f$), and `phase` ($\phi$)
- [x] Implement `SinusWave.evaluate(t: float)` mathematically: $A \sin(2\pi f t + \phi)$
- [x] Implement core generator: `generate_sinus_samples(amplitude, frequency, phase, samples_per_second, seconds, noise_factor=0.0)`
  - [x] Implement clean sinusoidal generation logic (Method 1)
  - [x] Implement Uniform noise bounds calculation: $X_{noised} = X \times (1 + \delta)$ (Method 2)
- [x] Implement list summation helper: `sum_sinus_lists(lists)` (Method 3)
  - [x] Add list length matching checks
  - [x] Implement element-wise index summation for up to 4 lists
- [x] Implement parametric summation: `sum_sinus_waves(waves, samples_per_second, seconds, noise_factor=0.0)` (Method 4)
  - [x] Evaluate up to 4 waves mathematically at each timestep
  - [x] Sum active amplitudes at time $t$ and apply noise bounds (Method 4)

## Phase 3: SDK Integration (`sdk.py`)
- [x] Import sinus services into `src/homework_1/sdk/sdk.py`
- [x] Expose clean sample generation wrapper in `HomeWorkSDK`
- [x] Expose element-wise list summation wrapper in `HomeWorkSDK`
- [x] Expose parametric summation wrapper in `HomeWorkSDK`

## Phase 4: Verification & Unit Tests (`tests/`)
- [x] Create unit test suite `tests/unit/test_sinus.py`
- [x] Implement mathematical integrity assertions for clean wave evaluations
- [x] Implement noise boundaries checks ensuring values reside in $[y(t) \times (1 \pm \text{noise\_factor})]$
- [x] Implement list summation assertion tests (handles matching lists, fails on mismatched lengths)
- [x] Implement multi-wave summation assertion tests
- [x] Write simple helper check to assert that `src/homework_1/services/sinus.py` strictly stays **under 140 lines of logical code** (excluding comments)

## Phase 5: End-to-End Bootstrap Execution
- [x] Update `src/main.py` to bootstrap and print results for:
  * Clean generated wave (Method 1)
  * Noised generated wave (Method 2)
  * List element-wise summation of 4 wave signals (Method 3)
  * Parametric summation of 4 waves (Method 4)
- [x] Execute `python3 src/main.py` to run integration sanity tests successfully

