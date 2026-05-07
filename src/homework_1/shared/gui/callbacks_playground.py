"""GUI Playground Callbacks manager module.

Implements slice generation, one-hot evaluation, and safe process termination.
Strictly adheres to the 150-line limit.
"""

import os
import random
import signal
from typing import Tuple

import plotly.graph_objs as go
from dash import Input, Output, State
from homework_1.services import FCNModel, LSTMModel, RNNModel
from homework_1.shared.gui.app import app, current_noised_sum_signal
from homework_1.shared.gui.callbacks_training import trained_models


@app.callback(
    [
        Output("plot-playground-sum-slice", "figure"),
        Output("store-playground-slice-idx", "data"),
    ],
    Input("btn-playground-generate", "n_clicks"),
    prevent_initial_call=True,
)
def handle_slice_generation(n_clicks: int) -> Tuple[go.Figure, int]:
    """Slices a random window of size 10 from noised sum wave and renders it."""
    global current_noised_sum_signal
    x = random.randint(0, 9990)

    # Slicing composite noised wave array
    sig_slice = current_noised_sum_signal[x : x + 10]
    t_steps = list(range(10))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_steps, y=sig_slice, mode="lines+markers", line_color="#198754"))
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
    global current_noised_sum_signal, trained_models

    # 1. Form one-hot selection mask
    one_hot = [0.0] * 4
    one_hot[int(choice) - 1] = 1.0

    # 2. Extract window size 10 from noised sum signal
    sum_slice = current_noised_sum_signal[x : x + 10]
    input_vec = one_hot + sum_slice

    t_steps = list(range(10))

    # Fallback to instantiation if models aren't cached in trained_models yet (e.g. mock testing context)
    fcn = trained_models.get("FCN", (FCNModel(14, [4], 10), None, None))[0]
    rnn = trained_models.get("RNN", (RNNModel(5, 8, 1), None, None))[0]
    lstm = trained_models.get("LSTM", (LSTMModel(5, 6, 1), None, None))[0]

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
    """Safe exit callback sending SIGTERM process signal to close the Dash server."""
    print("\n🛑 Safe exit requested. Shutting down visual Dash dashboard server process...")
    os.kill(os.getpid(), signal.SIGTERM)
    return "/"
