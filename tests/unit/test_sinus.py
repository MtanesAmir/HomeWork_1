"""Unit tests for the Sinus Wave Creation Engine.

Validates mathematical precision, noise boundary compliance, list and wave
summation correctness, and standard constraints.
"""

import math
from pathlib import Path

import pytest
from homework_1.services.sinus import (
    SinusWave,
    generate_sinus_samples,
    sum_sinus_lists,
    sum_sinus_waves,
)


def test_sinus_wave_evaluation() -> None:
    """Validates core SinusWave mathematical evaluation."""
    wave = SinusWave(amplitude=2.0, frequency=5.0, phase=math.pi / 2)

    # y(0) = A * sin(phi) = 2.0 * sin(pi / 2) = 2.0
    assert math.isclose(wave.evaluate(0.0), 2.0, abs_tol=1e-7)

    # y(t) for a full period T = 1/f = 0.2s: y(0.2) should equal y(0)
    assert math.isclose(wave.evaluate(0.2), 2.0, abs_tol=1e-7)

    # Invalid values input assertions
    with pytest.raises(ValueError, match="Frequency must be positive"):
        SinusWave(amplitude=1.0, frequency=-1.0, phase=0.0)
    with pytest.raises(ValueError, match="Amplitude must be non-negative"):
        SinusWave(amplitude=-1.0, frequency=1.0, phase=0.0)


def test_sinus_sample_generation_clean() -> None:
    """Validates clean sample generation matching reference points."""
    # 1000 samples per second, 2 seconds = 2000 samples
    samples = generate_sinus_samples(
        amplitude=1.0,
        frequency=10.0,
        phase=0.0,
        samples_per_second=1000,
        seconds=2.0,
        noise_factor=0.0,
    )
    assert len(samples) == 2000
    # At t = 0.0, y(0.0) = 1.0 * sin(0.0) = 0.0
    assert math.isclose(samples[0], 0.0, abs_tol=1e-7)


def test_sinus_sample_generation_noised() -> None:
    """Validates that noised samples strictly respect mathematical boundaries."""
    amplitude = 2.5
    frequency = 50.0
    phase = 1.0
    noise_factor = 0.05  # 5% noise

    clean_samples = generate_sinus_samples(
        amplitude=amplitude,
        frequency=frequency,
        phase=phase,
        samples_per_second=100,
        seconds=1.0,
        noise_factor=0.0,
    )

    noised_samples = generate_sinus_samples(
        amplitude=amplitude,
        frequency=frequency,
        phase=phase,
        samples_per_second=100,
        seconds=1.0,
        noise_factor=noise_factor,
    )

    assert len(clean_samples) == len(noised_samples)

    # Ensure every noised sample X_noisy resides strictly in range [X*(1-noise), X*(1+noise)]
    for clean, noised in zip(clean_samples, noised_samples):
        if math.isclose(clean, 0.0, abs_tol=1e-9):
            # If the clean value is zero, noised value should also be zero
            assert math.isclose(noised, 0.0, abs_tol=1e-9)
        else:
            lower_bound = min(clean * (1 - noise_factor), clean * (1 + noise_factor))
            upper_bound = max(clean * (1 - noise_factor), clean * (1 + noise_factor))
            assert lower_bound - 1e-9 <= noised <= upper_bound + 1e-9


def test_sum_sinus_lists() -> None:
    """Validates element-wise summation of lists and handles error boundaries."""
    list1 = [1.0, 2.0, 3.0]
    list2 = [10.0, 20.0, 30.0]
    list3 = [100.0, 200.0, 300.0]

    # Valid sum
    res = sum_sinus_lists([list1, list2, list3])
    assert res == [111.0, 222.0, 333.0]

    # Invalid limits: > 4 lists
    with pytest.raises(ValueError, match="Can only sum up to 4 lists"):
        sum_sinus_lists([list1] * 5)

    # Invalid formats: mismatched lengths
    with pytest.raises(ValueError, match="All lists must be of identical length"):
        sum_sinus_lists([[1.0], [1.0, 2.0]])


def test_sum_sinus_waves() -> None:
    """Validates parametric wave summation at each timestep."""
    w1 = SinusWave(amplitude=1.0, frequency=10.0, phase=0.0)
    w2 = SinusWave(amplitude=2.0, frequency=10.0, phase=0.0)
    w3 = SinusWave(amplitude=3.0, frequency=10.0, phase=0.0)

    # Combined mathematical wave: y(t) = (1+2+3) * sin(20*pi*t) = 6 * sin(20*pi*t)
    res_waves = sum_sinus_waves([w1, w2, w3], samples_per_second=100, seconds=1.0)

    res_single = generate_sinus_samples(
        amplitude=6.0,
        frequency=10.0,
        phase=0.0,
        samples_per_second=100,
        seconds=1.0,
        noise_factor=0.0,
    )

    assert len(res_waves) == len(res_single)
    for w_sum, s_val in zip(res_waves, res_single):
        assert math.isclose(w_sum, s_val, abs_tol=1e-7)


def test_line_limit_service_file() -> None:
    """Asserts that src/homework_1/services/sinus.py strictly stays below 140 logical lines of code."""
    service_path = Path(__file__).resolve().parents[2] / "src" / "homework_1" / "services" / "sinus.py"
    assert service_path.exists()

    with open(service_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    logical_code_lines = 0
    for line in lines:
        stripped = line.strip()
        # Skip empty lines and lines that are entirely comments (or docstring start/end markers if simple)
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        logical_code_lines += 1

    print(f"Logical code line count of sinus.py: {logical_code_lines}")
    # Strictly stays below the 140-line limit
    assert logical_code_lines <= 140


def test_sdk_sinus_integration() -> None:
    """Validates the SDK client integration, API Gatekeeper handling, and configuration."""
    from homework_1.sdk import HomeWorkSDK

    sdk = HomeWorkSDK()
    assert sdk.get_sdk_version() == "1.0.0"

    # 1. Test generate_samples wrapper
    res_gen = sdk.generate_samples(
        amplitude=1.0,
        frequency=5.0,
        phase=0.0,
        samples_per_second=100,
        seconds=1.0,
        noise_factor=0.0,
    )
    assert res_gen["status"] == "success"
    assert len(res_gen["result"]) == 100

    # 2. Test sum_samples wrapper
    res_sum = sdk.sum_samples([[1.0, 2.0], [3.0, 4.0]])
    assert res_sum["status"] == "success"
    assert res_sum["result"] == [4.0, 6.0]

    # 3. Test sum_waves wrapper
    w1 = SinusWave(amplitude=1.0, frequency=1.0, phase=0.0)
    w2 = SinusWave(amplitude=2.0, frequency=1.0, phase=0.0)
    res_waves = sdk.sum_waves([w1, w2], samples_per_second=100, seconds=1.0)
    assert res_waves["status"] == "success"
    assert len(res_waves["result"]) == 100


def test_sdk_additional_coverage() -> None:
    """Validates additional SDK paths, secrets, rate limit queuing, and error handling to reach 100% verification."""
    from homework_1.sdk import HomeWorkSDK

    sdk = HomeWorkSDK()

    # 1. Cover process_data clean and empty input paths
    res_proc = sdk.process_data("Valid input payload")
    assert res_proc["status"] == "success"
    assert res_proc["result"]["processed"] is True
    assert res_proc["result"]["payload"] == "VALID INPUT PAYLOAD"

    res_proc_empty = sdk.process_data("")
    assert res_proc_empty["status"] == "failed"
    assert "Input data cannot be empty" in res_proc_empty["error"]

    # 2. Cover ConfigManager.get and get_secret
    assert sdk.config_manager.get("app_name") == "homework_1"
    assert sdk.config_manager.get_secret("API_KEY") is None

    # 3. Cover rate limiting queue & history cleanup
    # Trigger rate limit by executing 31 calls (limit is 30 per min)
    results = []
    for i in range(31):
        res = sdk.generate_samples(1.0, 1.0, 0.0, 10, 1.0)
        results.append(res)

    # The 31st call should be queued
    assert results[-1]["status"] == "queued"
    assert "Rate limit reached" in results[-1]["message"]

    # Check queue depth is at least 1
    status = sdk.gatekeeper.get_queue_status()
    assert status["queue_depth"] >= 1


