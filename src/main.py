#!/usr/bin/env python3
"""Application main entry point.

Bootstraps raw CLI executions OR boots up the interactive Dash visual server.
"""

import argparse
import sys

from homework_1.sdk import HomeWorkSDK
from homework_1.services import SinusWave


def run_cli(sdk: HomeWorkSDK) -> None:
    """Runs the E2E simulation pipelines on the console."""
    print(f"Loaded SDK Version: {sdk.get_sdk_version()}")
    # Generate base signals
    clean_resp = sdk.generate_samples(1.0, 10.0, 0.0, 100, 0.1, 0.0)
    print(f"Clean sinus count: {len(clean_resp['result'])}")

    # Generate dataset
    dataset_resp = sdk.generate_and_save_dataset(num_rows=50, noise_factor=0.05)
    print(f"Dataset Pipeline Status: {dataset_resp['status']}")

    # Train models
    sdk.config_manager._setup_config["models"]["epochs"] = 20
    fcn_train = sdk.train_fcn()
    print(f"FCN Train Status: {fcn_train['status']}")


def main() -> int:
    """Main bootstrap entrypoint routing CLI pipelines or Visual Server boots."""
    parser = argparse.ArgumentParser(description="homework_1 CLI & GUI Launcher")
    parser.add_argument("--mode", type=str, default="cli", choices=["cli", "ui"], help="Launcher mode: cli or ui")
    parser.add_argument("--port", type=int, default=8050, help="Dash visual server local port")
    args = parser.parse_args()

    print("=== Bootstrapping homework_1 System ===")
    try:
        sdk = HomeWorkSDK()
        if args.mode == "ui":
            print(f"\n🚀 Starting visual dashboard server on: http://127.0.0.1:{args.port}")
            from homework_1.shared.gui.app import app
            app.run(debug=False, port=args.port)
        else:
            run_cli(sdk)
        print("\n=== Clean Exit ===")
        return 0
    except Exception as e:
        print(f"Error executing homework_1 bootstrap: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
