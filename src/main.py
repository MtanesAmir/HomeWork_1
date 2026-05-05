#!/usr/bin/env python3
"""Application main entry point.

Bootstraps and demonstrates the homework_1 package functionalities.
"""

import sys

from homework_1.sdk import HomeWorkSDK
from homework_1.services import SinusWave


def main() -> int:
    """Main bootstrap function."""
    print("=== Bootstrapping homework_1 SDK client ===")
    try:
        sdk = HomeWorkSDK()
        print(f"Loaded SDK Version: {sdk.get_sdk_version()}")

        # --- Clean Sinus Sample Generation (Method 1) ---
        print("\n--- Method 1: Clean Generated Sinus Samples ---")
        # Generate 10 samples for a 10 Hz sine wave over 0.1s
        clean_resp = sdk.generate_samples(
            amplitude=1.0,
            frequency=10.0,
            phase=0.0,
            samples_per_second=100,
            seconds=0.1,
            noise_factor=0.0,
        )
        print(f"Status: {clean_resp['status']}")
        print(f"Samples Count: {len(clean_resp['result'])}")
        print(f"First 5 Samples: {clean_resp['result'][:5]}")

        # --- Noised Sinus Sample Generation (Method 2) ---
        print("\n--- Method 2: Noised Generated Sinus Samples (10% Noise) ---")
        noised_resp = sdk.generate_samples(
            amplitude=1.0,
            frequency=10.0,
            phase=0.0,
            samples_per_second=100,
            seconds=0.1,
            noise_factor=0.1,
        )
        print(f"Status: {noised_resp['status']}")
        print(f"Samples Count: {len(noised_resp['result'])}")
        print(f"First 5 Samples: {noised_resp['result'][:5]}")

        # --- List Element-Wise Summation (Method 3) ---
        print("\n--- Method 3: List Element-wise Summation of 3 Lists ---")
        l1 = [1.0, 1.0, 1.0]
        l2 = [10.0, 10.0, 10.0]
        l3 = [100.0, 100.0, 100.0]
        sum_list_resp = sdk.sum_samples([l1, l2, l3])
        print(f"Status: {sum_list_resp['status']}")
        print(f"Summed Output List: {sum_list_resp['result']}")

        # --- Parametric Wave Summation (Method 4) ---
        print("\n--- Method 4: Parametric Summation of 4 Waves ---")
        w1 = SinusWave(amplitude=1.0, frequency=5.0, phase=0.0)
        w2 = SinusWave(amplitude=1.5, frequency=10.0, phase=0.5)
        w3 = SinusWave(amplitude=2.0, frequency=15.0, phase=1.0)
        w4 = SinusWave(amplitude=0.5, frequency=20.0, phase=1.5)
        sum_waves_resp = sdk.sum_waves(
            waves=[w1, w2, w3, w4], samples_per_second=100, seconds=0.1, noise_factor=0.05
        )
        print(f"Status: {sum_waves_resp['status']}")
        print(f"Summed Wave Count: {len(sum_waves_resp['result'])}")
        print(f"First 5 Summed Samples: {sum_waves_resp['result'][:5]}")

        print("\n=== Successful Bootstrap Execution ===")
        return 0
    except Exception as e:
        print(f"Error executing bootstrap: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
