#!/usr/bin/env python3
"""Application main entry point.

Bootstraps and demonstrates the homework_1 package functionalities.
"""

import sys

from homework_1.sdk import HomeWorkSDK


def main() -> int:
    """Main bootstrap function."""
    print("=== Bootstrapping homework_1 SDK client ===")
    try:
        sdk = HomeWorkSDK()
        print(f"Loaded SDK Version: {sdk.get_sdk_version()}")

        # Test a successful rate-limited call
        print("\n--- Test Case 1: Valid API Call ---")
        response = sdk.process_data("Hello, World!")
        print(f"Response: {response}")

        # Test an invalid call resulting in transient failure
        print("\n--- Test Case 2: Invalid API Call ---")
        response = sdk.process_data("")
        print(f"Response: {response}")

        # Display Gatekeeper stats
        print("\n--- Gatekeeper Stats ---")
        stats = sdk.gatekeeper.get_queue_status()
        print(f"Stats: {stats}")

        print("\n=== Successful Bootstrap Execution ===")
        return 0
    except Exception as e:
        print(f"Error executing bootstrap: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
