"""Sinus wave service module.

Implements Single Sinus Wave representation, discrete sample generation,
and wave/list summation services with noise simulation.
"""

import math
import random
from typing import List


class SinusWave:
    """Represents a single mathematical sine wave: y(t) = A * sin(2*pi*f*t + phi)."""

    def __init__(self, amplitude: float, frequency: float, phase: float):
        if frequency <= 0:
            raise ValueError("Frequency must be positive")
        if amplitude < 0:
            raise ValueError("Amplitude must be non-negative")
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def evaluate(self, t: float) -> float:
        """Computes the instantaneous clean amplitude at time t."""
        return self.amplitude * math.sin(2 * math.pi * self.frequency * t + self.phase)


def generate_sinus_samples(
    amplitude: float,
    frequency: float,
    phase: float,
    samples_per_second: int,
    seconds: float,
    noise_factor: float = 0.0,
) -> List[float]:
    """Generates discrete samples of a single sinus wave with optional noise."""
    if samples_per_second <= 0 or seconds <= 0:
        raise ValueError("Samples per second and seconds must be positive")
    if noise_factor < 0:
        raise ValueError("Noise factor must be non-negative")

    wave = SinusWave(amplitude, frequency, phase)
    total_samples = int(samples_per_second * seconds)
    samples = []

    for k in range(total_samples):
        t = k / samples_per_second
        val = wave.evaluate(t)
        if noise_factor > 0.0:
            delta = random.uniform(-noise_factor, noise_factor)
            val *= 1.0 + delta
        samples.append(val)

    return samples


def sum_sinus_lists(lists: List[List[float]]) -> List[float]:
    """Calculates the element-wise sum of up to 4 lists of matching length."""
    if not lists:
        return []
    if len(lists) > 4:
        raise ValueError("Can only sum up to 4 lists")

    length = len(lists[0])
    for lst in lists:
        if len(lst) != length:
            raise ValueError("All lists must be of identical length")

    result = [0.0] * length
    for lst in lists:
        for i in range(length):
            result[i] += lst[i]

    return result


def sum_sinus_waves(
    waves: List[SinusWave],
    samples_per_second: int,
    seconds: float,
    noise_factor: float = 0.0,
) -> List[float]:
    """Evaluates and sums up to 4 waves at each timestep with optional noise."""
    if not waves:
        return []
    if len(waves) > 4:
        raise ValueError("Can only sum up to 4 waves")
    if samples_per_second <= 0 or seconds <= 0:
        raise ValueError("Samples per second and seconds must be positive")
    if noise_factor < 0:
        raise ValueError("Noise factor must be non-negative")

    total_samples = int(samples_per_second * seconds)
    samples = []

    for k in range(total_samples):
        t = k / samples_per_second
        val = sum(wave.evaluate(t) for wave in waves)
        if noise_factor > 0.0:
            delta = random.uniform(-noise_factor, noise_factor)
            val *= 1.0 + delta
        samples.append(val)

    return samples
