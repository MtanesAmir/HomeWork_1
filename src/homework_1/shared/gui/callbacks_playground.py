"""GUI Playground Callbacks manager module.

Implements slice generation, one-hot evaluation, and safe process termination.
Strictly adheres to the 150-line limit.
"""

import os
import random
import signal
from typing import Tuple

import plotly.graph_objs as go
from dash import Input, Output, State, dash, callback_context
from homework_1.services import FCNModel, LSTMModel, RNNModel
import homework_1.shared.gui.app as base_app
from homework_1.shared.gui.app import app
from homework_1.shared.gui.callbacks_training import trained_models


@app.callback(
    [
        Output("plot-playground-sum-slice", "figure"),
        Output("store-playground-slice-idx", "data"),
    ],
    [
        Input("btn-playground-generate", "n_clicks"),
        Input("toggle-dots-lines", "value"),
    ],
    State("store-playground-slice-idx", "data"),
    prevent_initial_call=True,
)
def handle_slice_generation(n_clicks: int, draw_mode: str, current_x: int) -> Tuple[go.Figure, int]:
    """Slices a random window of size 10 from noised sum wave and renders it using the active style mode."""
    # Slicing composite noised wave array
    noised_sig = base_app.current_noised_sum_signal
    if not noised_sig:
        # Fallback dynamic generation if empty to safeguard play mode
        import math
        noised_sig = [math.sin(k/10.0) for k in range(10000)]

    # Determine if we slice a new index or keep the current active index on style toggle
    try:
        ctx = callback_context
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else ""
    except Exception:
        triggered_id = ""

    if triggered_id == "toggle-dots-lines" and current_x is not None:
        x = current_x
    else:
        x = random.randint(0, 9990)

    sig_slice = noised_sig[x : x + 10]
    t_steps = list(range(10))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_steps, y=sig_slice, mode=draw_mode, line_color="#198754"))
    fig.update_layout(margin={"l": 10, "r": 10, "t": 20, "b": 20})

    return fig, x


@app.callback(
    [
        Output("plot-predict-fcn", "figure"),
        Output("plot-predict-rnn", "figure"),
        Output("plot-predict-lstm", "figure"),
    ],
    [
        Input("choice-one-hot-mask", "value"),
        Input("store-playground-slice-idx", "data"),
        Input("toggle-dots-lines", "value"),
    ],
)
def evaluate_models_predictions(choice: str, x: int, draw_mode: str) -> Tuple[go.Figure, go.Figure, go.Figure]:
    """Invokes FCN, RNN, and LSTM predictions on sliding sum window with selectors, updating playground plots."""
    global trained_models

    # 1. Form one-hot selection mask
    one_hot = [0.0] * 4
    one_hot[int(choice) - 1] = 1.0

    noised_sig = base_app.current_noised_sum_signal
    if not noised_sig:
        import math
        noised_sig = [math.sin(k/10.0) for k in range(10000)]

    # 2. Extract window size 10 from noised sum signal
    sum_slice = noised_sig[x : x + 10]
    input_vec = one_hot + sum_slice

    t_steps = list(range(10))

    # Fallback to instantiation if models aren't cached in trained_models yet (e.g. mock testing context)
    import homework_1.shared.gui.callbacks_training as cb_t
    m_cfg = base_app.sdk.config_manager.get("models", {})
    fcn_l = m_cfg.get("hidden_layers", [3, 5, 3])
    rnn_l = m_cfg.get("rnn_layers", [8])
    lstm_l = m_cfg.get("lstm_layers", [6])

    fcn = cb_t.trained_models.get("FCN", FCNModel(14, fcn_l, 10))
    rnn = cb_t.trained_models.get("RNN", RNNModel(5, rnn_l, 1))
    lstm = cb_t.trained_models.get("LSTM", LSTMModel(5, lstm_l, 1))

    f_pred = fcn.get_prediction(input_vec)
    r_pred = rnn.get_prediction(input_vec)
    l_pred = lstm.get_prediction(input_vec)

    # Predictions visual render curves
    f_fig = go.Figure()
    f_fig.add_trace(go.Scatter(x=t_steps, y=f_pred, mode=draw_mode, line_color="#0d6efd"))
    f_fig.update_layout(margin={"l": 10, "r": 10, "t": 20, "b": 20})

    r_fig = go.Figure()
    r_fig.add_trace(go.Scatter(x=t_steps, y=r_pred, mode=draw_mode, line_color="#dc3545"))
    r_fig.update_layout(margin={"l": 10, "r": 10, "t": 20, "b": 20})

    l_fig = go.Figure()
    l_fig.add_trace(go.Scatter(x=t_steps, y=l_pred, mode=draw_mode, line_color="#ffc107"))
    l_fig.update_layout(margin={"l": 10, "r": 10, "t": 20, "b": 20})

    return f_fig, r_fig, l_fig


@app.callback(
    Output("url", "pathname", allow_duplicate=True),
    Input("btn-exit-dashboard", "n_clicks"),
    prevent_initial_call=True,
)
def handle_server_exit(n_clicks: int) -> str:
    """Safe exit callback transition page to Screen 4 and schedules delayed shutdown in background."""
    if not n_clicks or n_clicks <= 0:
        return dash.no_update

    print("\n🛑 Safe exit requested. Routing to splash Screen 4...")

    # Spawn delayed termination daemon thread to let Dash render splash Screen 4
    def delayed_kill() -> None:
        import time
        time.sleep(1.2)
        print("🛑 Shutting down visual Dash dashboard server process safely...")
        os.kill(os.getpid(), signal.SIGTERM)

    import threading
    threading.Thread(target=delayed_kill, daemon=True).start()

    return "/exit"
