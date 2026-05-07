"""GUI Training Callbacks manager module.

Implements asynchronous models training loss updates and test set evaluations.
Strictly adheres to the 150-line limit.
"""

import threading
from typing import Dict, Any
import plotly.graph_objs as go
from dash import Input, Output, State, dash
from homework_1.services import FCNModel, LSTMModel, RNNModel, train_neural_network
from homework_1.services.models.trainer import evaluate_loss, partition_dataset
from homework_1.shared.gui.app import app, sdk

# Persistent model storage keys for callback caching
trained_models: dict = {}

# Global thread-safe cache stores tracking training threads progress concurrently
training_caches: Dict[str, Dict[str, Any]] = {
    "FCN": {"epoch": 0, "history": {}, "test_mse": 0.0, "complete": False},
    "RNN": {"epoch": 0, "history": {}, "test_mse": 0.0, "complete": False},
    "LSTM": {"epoch": 0, "history": {}, "test_mse": 0.0, "complete": False},
}


def background_training_thread(model_type: str, model: Any, dataset: list, epochs: int, train: float, val: float, test: float) -> None:
    """Target function executing BPTT models training loop in a separate background thread."""
    global training_caches

    # Centralized custom trainer handles progress metrics increments of 10 epochs
    history = train_neural_network(
        model=model,
        dataset=dataset,
        epochs=epochs,
        train_pct=train,
        val_pct=val,
        test_pct=test,
        learning_rate=0.1 if model_type == "LSTM" else 0.05
    )

    # Extract final computed Test Set MSE (which trainer isolates to the end)
    final_test_mse = history["test_loss"][-1]

    training_caches[model_type]["history"] = history
    training_caches[model_type]["test_mse"] = final_test_mse
    training_caches[model_type]["complete"] = True


@app.callback(
    [
        Output("plot-fcn-training", "figure"),
        Output("plot-rnn-training", "figure"),
        Output("plot-lstm-training", "figure"),
        Output("lbl-fcn-test-mse", "children"),
        Output("lbl-rnn-test-mse", "children"),
        Output("lbl-lstm-test-mse", "children"),
        Output("training-status-text", "children"),
        Output("btn-go-to-playground", "disabled"),
        Output("btn-go-to-playground", "style"),
    ],
    Input("training-interval", "n_intervals"),
)
def monitor_training_progress(n_intervals: int) -> tuple:
    """Pipes and handles throttled metrics updates dynamically from concurrent background threads."""
    global trained_models, training_caches

    model_cfg = sdk.config_manager.get("models", {})
    epochs = model_cfg.get("epochs", 20)
    hidden = model_cfg.get("hidden_layers", [3, 5, 3])
    rnn_lay = model_cfg.get("rnn_layers", [8])
    lstm_lay = model_cfg.get("lstm_layers", [6])
    train_pct = model_cfg.get("train_percentage", 70.0)
    val_pct = model_cfg.get("val_percentage", 15.0)
    test_pct = model_cfg.get("test_percentage", 15.0)

    # Kick off separate threads for FCN, RNN, and LSTM loops in parallel on first click
    if not trained_models:
        dataset = sdk._get_or_create_dataset()
        
        fcn = FCNModel(input_size=14, hidden_layers=hidden, output_size=10)
        rnn = RNNModel(input_size=5, hidden_layers=rnn_lay, output_size=1)
        lstm = LSTMModel(input_size=5, hidden_layers=lstm_lay, output_size=1)

        trained_models = {"FCN": fcn, "RNN": rnn, "LSTM": lstm}

        # Instantiate and start background threads concurrently
        threading.Thread(target=background_training_thread, args=("FCN", fcn, dataset, epochs, train_pct, val_pct, test_pct), daemon=True).start()
        threading.Thread(target=background_training_thread, args=("RNN", rnn, dataset, epochs, train_pct, val_pct, test_pct), daemon=True).start()
        threading.Thread(target=background_training_thread, args=("LSTM", lstm, dataset, epochs, train_pct, val_pct, test_pct), daemon=True).start()

    # Check concurrency completion status
    f_cache = training_caches["FCN"]
    r_cache = training_caches["RNN"]
    l_cache = training_caches["LSTM"]

    all_complete = f_cache["complete"] and r_cache["complete"] and l_cache["complete"]

    # Build throttled Plotly figures (metrics are updated dynamically)
    def build_throttled_figure(cache: dict) -> go.Figure:
        fig = go.Figure()
        if cache["history"]:
            train_loss = cache["history"]["train_loss"]
            val_loss = cache["history"]["val_loss"]
            # Throttle visual curve coordinates plot to 10-epoch increments
            x_epochs = [1] + [k for k in range(10, len(train_loss) + 1, 10)]
            if len(train_loss) not in x_epochs:
                x_epochs.append(len(train_loss))

            y_train = [train_loss[ep - 1] for ep in x_epochs]
            y_val = [val_loss[ep - 1] for ep in x_epochs]

            fig.add_trace(go.Scatter(x=x_epochs, y=y_train, name="Train"))
            fig.add_trace(go.Scatter(x=x_epochs, y=y_val, name="Val"))
        fig.update_layout(margin={"l": 10, "r": 10, "t": 20, "b": 20})
        return fig

    f_fig = build_throttled_figure(f_cache)
    r_fig = build_throttled_figure(r_cache)
    l_fig = build_throttled_figure(l_cache)

    f_lbl = f"{f_cache['test_mse']:.5f}" if f_cache["complete"] else "Waiting..."
    r_lbl = f"{r_cache['test_mse']:.5f}" if r_cache["complete"] else "Waiting..."
    l_lbl = f"{l_cache['test_mse']:.5f}" if l_cache["complete"] else "Waiting..."

    status_txt = "Models successfully trained!" if all_complete else "Training all models concurrently..."
    btn_disabled = not all_complete

    btn_style = {
        "padding": "15px 65px",
        "fontSize": "20px",
        "fontWeight": "bold",
        "borderRadius": "8px",
        "border": "none",
        "backgroundColor": "#0d6efd" if all_complete else "#6c757d",
        "color": "#ffffff",
        "cursor": "pointer" if all_complete else "not-allowed",
        "boxShadow": "0 4px 6px rgba(13, 110, 253, 0.3)" if all_complete else "none",
    }

    return f_fig, r_fig, l_fig, f_lbl, r_lbl, l_lbl, status_txt, btn_disabled, btn_style


@app.callback(
    Output("url", "pathname", allow_duplicate=True),
    Input("btn-go-to-playground", "n_clicks"),
    prevent_initial_call=True,
)
def route_to_playground(n_clicks: int) -> str:
    """Redirects successfully to Screen 3."""
    return "/playground"
