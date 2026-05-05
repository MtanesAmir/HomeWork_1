# Product Requirements Document (PRD): Sinus Wave Creation Engine

## Overview
The Sinus Wave Creation Engine is a core mathematical and signal-processing utility. Its purpose is to generate high-fidelity simulated discrete samples of sinus (sine) waves. The engine is designed to be a flexible base for subsequent computer science and AI tasks, such as data synthesis, model testing, and signal simulation.

---

## Objectives
1. Provide a highly configurable mathematical generator for standard sine waves.
2. Support optional noise injection (e.g., Gaussian/random noise) to simulate real-world signal transmission.
3. Enable composite signal synthesis by allowing developers to sum up to 4 distinct sine wave samples at any given time step.

---

## Core Mathematical Formula
The generated value of a single sinus wave sample at a specific time $t$ is defined by the function:

$$y(t) = A \sin(2\pi f t + \phi)$$

### Variable Definitions:
* **$y(t)$**: The instantaneous value of the wave at any given moment in time $t$.
* **$A$ (Amplitude)**: The peak deviation of the function from zero. Represents the signal "strength" or "loudness".
* **$f$ (Frequency)**: The number of complete oscillations per second, measured in Hertz (Hz).
* **$t$ (Time)**: The independent variable representing the specific timestamp in seconds.
* **$\phi$ (Phase)**: The phase shift (in radians), determining where in its cycle the oscillation starts at $t = 0$.
* **$2\pi f$ (Angular Frequency)**: Converts the rate of oscillation into angular velocity (radians per second).

---

## Functional Requirements

### FR-1: Basic Sinusoidal Sample Generation
* The system **MUST** accept configuration parameters for a single sine wave:
  * Amplitude ($A$, float, default = 1.0)
  * Frequency ($f$, float, default = 1.0 Hz)
  * Phase Shift ($\phi$, float, default = 0.0 radians)
* The system **MUST** calculate and return the discrete value $y(t)$ for any given moment in time $t$ (seconds).

### FR-2: Noise Injection
* The system **MUST** provide the option to generate either clean or noisy samples.
* **Clean Mode**: Generates the exact mathematical wave value $y(t)$.
* **Noisy Mode**: Adds random noise (Gaussian white noise) to the sample:
  $$y_{noisy}(t) = y(t) + \epsilon$$
  Where $\epsilon \sim \mathcal{N}(0, \sigma^2)$ represents a random variable drawn from a normal distribution with configurable standard deviation $\sigma$ (noise amplitude/intensity).
* The noise standard deviation ($\sigma$, float) **MUST** be configurable by the developer.

### FR-3: Multi-Wave Summation (Composite Wave Synthesis)
* The system **MUST** support combining multiple waves.
* The system **MUST** allow the developer to specify parameters ($A_i, f_i, \phi_i$) for up to **4 separate sinus waves** ($N \le 4$).
* The system **MUST** compute the cumulative sum of the waves at each discrete time step $t$:
  $$Y_{sum}(t) = \sum_{i=1}^{N} A_i \sin(2\pi f_i t + \phi_i)$$
* The multi-wave summation **MUST** also support optional noise injection applied to the final composite wave.

---

## Developer Guidelines & Architecture Notes

### Modular "Building Block" Design
Conforming to our project's architectural standards, the implementation should be structured around clean, isolated components:
1. **`SinusWave` Building Block**: An object representing a single mathematical sine wave, containing its parameters and a `.evaluate(t)` method.
2. **`SignalGenerator` Service**: Integrates multiple `SinusWave` objects, handles the sum calculations, and implements the noise-addition logic.

### Input Validation
* Frequencies ($f$) **MUST** be positive values ($f > 0$).
* Amplitude ($A$) and noise standard deviation ($\sigma$) **MUST** be non-negative.
* Graceful error handling with clear exception messages must be implemented for out-of-bounds parameters.
