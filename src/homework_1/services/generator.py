"""Dataset Generator Engine Service module.

Handles preparing base signal arrays, executing uniform sliding window dataset row
synthesis, and serializing complete dataset databases to disk.
"""

import json
import random
from pathlib import Path
from typing import Any, Dict, List

from homework_1.services.sinus import SinusWave, generate_sinus_samples, sum_sinus_lists
from homework_1.shared.config import ConfigManager


def prepare_base_signals(noise_factor: float = 0.0) -> Dict[str, Any]:
    """Prepares 10 base sinus signals of size 10K samples (4 clean, 1 sum, 4 noised, 1 sum)."""
    config = ConfigManager()
    waves_config = config.get("waves", [])

    if not waves_config or len(waves_config) != 4:
        raise ValueError("Configuration must define exactly 4 base waves")

    waves = [
        SinusWave(w["amplitude"], w["frequency"], w["phase"])
        for w in waves_config
    ]

    # 1. Generate clean samples (10 seconds, 1000 samples/sec = 10,000 samples)
    clean_waves = []
    for wave in waves:
        samples = generate_sinus_samples(
            amplitude=wave.amplitude,
            frequency=wave.frequency,
            phase=wave.phase,
            samples_per_second=1000,
            seconds=10.0,
            noise_factor=0.0,
        )
        clean_waves.append(samples)

    clean_sum = sum_sinus_lists(clean_waves)

    # 2. Generate noised samples
    noised_waves = []
    for wave in waves:
        samples = generate_sinus_samples(
            amplitude=wave.amplitude,
            frequency=wave.frequency,
            phase=wave.phase,
            samples_per_second=1000,
            seconds=10.0,
            noise_factor=noise_factor,
        )
        noised_waves.append(samples)

    noised_sum = sum_sinus_lists(noised_waves)

    return {
        "clean_waves": clean_waves,
        "clean_sum": clean_sum,
        "noised_waves": noised_waves,
        "noised_sum": noised_sum,
    }


def generate_dataset(num_rows: int, noise_factor: float) -> Dict[str, Any]:
    """Generates num_rows of dataset training row samples from base signals."""
    if num_rows <= 0:
        raise ValueError("Dataset rows count must be positive")

    signals = prepare_base_signals(noise_factor=noise_factor)
    clean_waves = signals["clean_waves"]
    noised_sum = signals["clean_sum"]  # Wait, should we slice from clean sum or noised sum?
    # Wait, let's check what the PRD says:
    # "from the noise sum list we take a sample from index X to X+9..."
    # Yes! "noise sum list" is indeed noised_sum! Let's change this to noised_sum.
    noised_sum = signals["noised_sum"]

    dataset = []

    for _ in range(num_rows):
        # 1. Generate random window starting index X
        x = random.randint(0, 9990)

        # 2. Generate uniform one-hot target selector
        chosen_index = random.randint(0, 3)
        chosen_array = [0.0] * 4
        chosen_array[chosen_index] = 1.0

        # 3. Extract noise sum sample (size 10)
        noise_sum_sample_list = noised_sum[x : x + 10]

        # 4. Extract origin clean sinus sample (size 10)
        origin_sinus_sample_list = clean_waves[chosen_index][x : x + 10]

        # Assemble row: key (size 14) and value (size 10)
        key = chosen_array + noise_sum_sample_list
        value = origin_sinus_sample_list

        dataset.append({"key": key, "value": value})

    return {"dataset": dataset}


def save_dataset(dataset: Dict[str, Any], output_path: str) -> None:
    """Writes dataset database in JSON format to configured path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
