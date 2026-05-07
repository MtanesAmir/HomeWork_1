"""GUI Entry Point router module.

Coordinates page mapping pathways, dynamic layout loads, and imports callbacks
namespaces while strictly keeping logical code line counts under the 150-line limit.
"""

import dash
from typing import Any, Tuple, List, Dict
from dash import Input, Output, State, dcc, html
from homework_1.sdk import HomeWorkSDK
from homework_1.shared.gui.screen1 import get_screen1_layout
from homework_1.shared.gui.screen2 import get_screen2_layout
from homework_1.shared.gui.screen3 import get_screen3_layout

# Initialize SDK Client and Dash app
sdk = HomeWorkSDK()
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Map-level coordinate containers caching wave profiles for E2E tests
current_clean_base_signals = []
current_clean_sum_signal = []
current_noised_sum_signal = []

# Router container
app.layout = html.Div(
    children=[dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def route_page(pathname: str) -> html.Div:
    """Routes path URIs to correct layouts."""
    if pathname == "/training":
        return get_screen2_layout()
    if pathname == "/playground":
        return get_screen3_layout()
    if pathname == "/exit":
        from homework_1.shared.gui.screen3 import get_screen4_layout
        return get_screen4_layout()
    return get_screen1_layout()


@app.callback(
    [
        Output("plot-components-overlay", "figure"),
        Output("plot-sum-signal", "figure"),
    ],
    [
        Input("freq-1", "value"),
        Input("phase-1", "value"),
        Input("amp-1", "value"),
        Input("freq-2", "value"),
        Input("phase-2", "value"),
        Input("amp-2", "value"),
        Input("freq-3", "value"),
        Input("phase-3", "value"),
        Input("amp-3", "value"),
        Input("freq-4", "value"),
        Input("phase-4", "value"),
        Input("amp-4", "value"),
    ],
)
def update_screen1_plots(*args: Any) -> Tuple[Any, Any]:
    """Updates component wave overlays and summed continuous curves in real-time on slider adjustments."""
    global current_clean_base_signals, current_clean_sum_signal
    from homework_1.shared.gui.plots_helper import compute_and_draw_screen1_plots

    fig_overlay, fig_sum, base_signals, sum_signal = compute_and_draw_screen1_plots(*args)

    # Caching variables for pipeline and E2E test queries
    current_clean_base_signals = base_signals
    current_clean_sum_signal = sum_signal

    return fig_overlay, fig_sum


@app.callback(
    [
        Output("validation-alert-container", "children"),
        Output("url", "pathname", allow_duplicate=True),
    ],
    Input("btn-start-training", "n_clicks"),
    [
        State("input-epochs", "value"),
        State("input-dataset-size", "value"),
        State("slider-noise", "value"),
        State("input-train-pct", "value"),
        State("input-val-pct", "value"),
        State("input-test-pct", "value"),
        State("input-fcn-layers", "value"),
        State("input-rnn-layers", "value"),
        State("input-lstm-layers", "value"),
    ],
    prevent_initial_call=True,
)
def handle_training_start(
    n_clicks: int, epochs: int, dataset_size: int, noise: float,
    train: float, val: float, test: float,
    fcn_raw: str, rnn_raw: str, lstm_raw: str
) -> Tuple[Any, str]:
    """Validates splits, parses and validates model layers text strings, and triggers background setups."""
    global current_noised_sum_signal

    total = train + val + test
    if abs(total - 100.0) > 1e-7:
        alert = html.Div(
            f"⚠️ Error: Splits percentages sum to {total}%, which is not exactly 100%! Correct parameters to continue.",
            style={
                "padding": "12px",
                "backgroundColor": "#f8d7da",
                "color": "#842029",
                "borderRadius": "5px",
                "border": "1px solid #f5c2c7",
                "fontWeight": "bold",
            },
        )
        return alert, dash.no_update

    # Helper to safely parse comma-separated layers list
    def parse_layers_string(raw_str: str, name: str) -> Tuple[List[int], str]:
        if not raw_str or not raw_str.strip():
            return [], f"⚠️ Error: {name} layers configuration input cannot be empty!"
        try:
            layers = [int(k.strip()) for k in raw_str.split(",") if k.strip()]
            if not layers:
                return [], f"⚠️ Error: {name} layers configuration cannot be empty!"
            if any(val <= 0 for val in layers):
                return [], f"⚠️ Error: {name} layers must be positive integers greater than 0!"
            return layers, ""
        except ValueError:
            return [], f"⚠️ Error: {name} layers format must be a comma-separated list of integers (e.g. '3, 5, 3')!"

    # Parse FCN, RNN, and LSTM layer lists
    fcn_layers, err = parse_layers_string(fcn_raw, "FCN")
    if err:
        return html.Div(err, style={"padding": "12px", "backgroundColor": "#f8d7da", "color": "#842029", "borderRadius": "5px", "border": "1px solid #f5c2c7", "fontWeight": "bold"}), dash.no_update

    rnn_layers, err = parse_layers_string(rnn_raw, "RNN")
    if err:
        return html.Div(err, style={"padding": "12px", "backgroundColor": "#f8d7da", "color": "#842029", "borderRadius": "5px", "border": "1px solid #f5c2c7", "fontWeight": "bold"}), dash.no_update

    lstm_layers, err = parse_layers_string(lstm_raw, "LSTM")
    if err:
        return html.Div(err, style={"padding": "12px", "backgroundColor": "#f8d7da", "color": "#842029", "borderRadius": "5px", "border": "1px solid #f5c2c7", "fontWeight": "bold"}), dash.no_update

    # Push parameters updates to SDK setup configurations
    sdk.config_manager._setup_config["models"] = {
        "epochs": epochs,
        "train_percentage": train,
        "val_percentage": val,
        "test_percentage": test,
        "hidden_layers": fcn_layers,
        "rnn_layers": rnn_layers,
        "lstm_layers": lstm_layers,
    }

    # Trigger base signals and dataset creation in the background
    from homework_1.services.generator import generate_dataset, prepare_base_signals, save_dataset

    # Cache the noised sum composite signal for E2E playground slicing
    base_signals = prepare_base_signals(noise_factor=noise)
    current_noised_sum_signal = base_signals["noised_sum"]

    # Generate and serialize training dataset database to disk
    dataset = generate_dataset(num_rows=dataset_size, noise_factor=noise)
    output_path = sdk.config_manager.get("dataset_output_path", "results/dataset.json")
    save_dataset(dataset, output_path)

    # Redirect successfully to Screen 2
    return None, "/training"


# Import layouts modules callbacks namespaces
import homework_1.shared.gui.app as base_app
from typing import Tuple, Any
# Force references synchronization
base_app.app = app
base_app.sdk = sdk

# Import active callback managers to register namespaces
import homework_1.shared.gui.callbacks_playground
import homework_1.shared.gui.callbacks_training
