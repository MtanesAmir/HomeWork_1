"""GUI Unit and E2E simulation tests for the Interactive Web Dashboard.

Validates page layouts, interactive sliders, splits validation, playground slicing,
model prediction plotting, safe SIGTERM exit calls, and linter code length limits.
"""

import sys
from pathlib import Path

import pytest
from homework_1.shared.gui.app import (
    handle_training_start,
    route_page,
    update_screen1_plots,
)
from homework_1.shared.gui.callbacks_playground import (
    evaluate_models_predictions,
    handle_server_exit,
    handle_slice_generation,
)
from homework_1.shared.gui.callbacks_training import monitor_training_progress
from homework_1.shared.gui.screen1 import get_screen1_layout
from homework_1.shared.gui.screen2 import get_screen2_layout
from homework_1.shared.gui.screen3 import get_screen3_layout


def test_gui_screen1_layout() -> None:
    """Validates that Screen 1 layout instantiates base structures properly."""
    layout = get_screen1_layout()
    assert layout is not None
    assert len(layout.children) == 2


def test_gui_screen2_layout() -> None:
    """Validates that Screen 2 layout instantiates progress structures properly."""
    layout = get_screen2_layout()
    assert layout is not None
    assert len(layout.children) >= 4


def test_gui_screen3_layout() -> None:
    """Validates that Screen 3 layout instantiates playgrounds correctly."""
    layout = get_screen3_layout()
    assert layout is not None
    assert len(layout.children) >= 4


def test_gui_page_routing() -> None:
    """Validates that route_page correctly resolves URI endpoints."""
    assert get_screen1_layout().style == route_page("/").style
    assert get_screen2_layout().style == route_page("/training").style
    assert get_screen3_layout().style == route_page("/playground").style


def test_gui_screen1_splits_validation() -> None:
    """Asserts that Screen 1 split ratios validation warn banner renders correctly on invalid sums."""
    # Invalid splits: 70% + 10% + 10% = 90%
    alert, path = handle_training_start(1, 20, 100, 0.05, 70.0, 10.0, 10.0)
    assert alert is not None
    assert "Error" in alert.children
    import dash
    assert path == dash.no_update

    # Valid splits: 70% + 15% + 15% = 100%
    alert_ok, path_ok = handle_training_start(1, 20, 100, 0.05, 70.0, 15.0, 15.0)
    assert alert_ok is None
    assert path_ok == "/training"  # Redirects successfully


def test_gui_screen1_sliders_plotting_callback() -> None:
    """Asserts that adjusting wave component sliders updates Plotly Cartesian overlay coordinates."""
    # Mock updates
    fig_overlay, fig_sum = update_screen1_plots(
        5.0, 0.0, 1.0,  # wave 1
        10.0, 0.5, 1.5, # wave 2
        15.0, 1.0, 2.0, # wave 3
        20.0, 1.5, 0.5  # wave 4
    )

    # Cartesian validation overlays check
    assert len(fig_overlay.data) == 4
    assert len(fig_sum.data) == 1

    assert fig_overlay.data[0].name == "Sinusoid 1"
    assert fig_sum.data[0].name == "Sum"


def test_gui_screen2_async_progress_callback() -> None:
    """Asserts that the training progress callback generates loss curves and unlocks Playground link."""
    f_fig, r_fig, l_fig, f_mse, r_mse, l_mse, status, btn_disabled, _ = monitor_training_progress(1)

    assert "trained" in status
    assert btn_disabled is False  # "Lets play" button gets enabled

    # Loss curves contain train/val traces
    assert len(f_fig.data) == 2
    assert len(r_fig.data) == 2
    assert len(l_fig.data) == 2

    assert f_fig.data[0].name == "Train"
    assert f_fig.data[1].name == "Val"


def test_gui_screen3_playground_callbacks() -> None:
    """Asserts playground slice generator, continuous-dots styles, and model evaluation prediction loops."""
    # 1. Slices generator
    fig_slice, x = handle_slice_generation(1)
    assert 0 <= x <= 9990
    assert len(fig_slice.data) == 1

    # 2. Evaluation prediction loops (FCN, RNN, LSTM plots overlays)
    f_fig, r_fig, l_fig = evaluate_models_predictions("2", x, "lines")

    # Each plot must contain the prediction curve
    assert len(f_fig.data) == 1
    assert len(r_fig.data) == 1
    assert len(l_fig.data) == 1

    assert f_fig.data[0].mode == "lines"


def test_gui_screen3_exit_callback() -> None:
    """Asserts that the exit callback receives a SIGTERM termination command gracefully."""
    with pytest.raises(SystemExit):
        # Mock os.kill using system exit in test harness context
        import os
        old_kill = os.kill
        try:
            os.kill = lambda pid, sig: sys.exit(0)
            handle_server_exit(1)
        finally:
            os.kill = old_kill


def test_gui_line_limits_constraint() -> None:
    """Asserts that screen1.py, screen2.py, screen3.py, app.py, and test_gui.py stay under 150 logical lines."""
    gui_dir = Path(__file__).resolve().parents[2] / "src" / "homework_1" / "shared" / "gui"

    files_to_check = [
        gui_dir / "screen1.py",
        gui_dir / "screen2.py",
        gui_dir / "screen3.py",
        gui_dir / "app.py",
        gui_dir / "callbacks_training.py",
        gui_dir / "callbacks_playground.py",
        Path(__file__),
    ]

    for filepath in files_to_check:
        assert filepath.exists()
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        logical_code_lines = 0
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                continue
            logical_code_lines += 1

        print(f"GUI File {filepath.name}: {logical_code_lines} logical lines")
        assert logical_code_lines <= 150
