"""GUI Screen 2 layout module.

Provides FCN, RNN, and LSTM Cartesian metric training curves plots,
diagnostic progress indicators, and Test Set MSE display elements.
"""

from dash import dcc, html


def get_model_training_box(model_name: str, graph_id: str, mse_label_id: str) -> html.Div:
    """Creates an individual grid box for a specific model training plot and test MSE output."""
    return html.Div(
        style={
            "width": "31%",
            "backgroundColor": "#ffffff",
            "padding": "20px",
            "borderRadius": "10px",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)",
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
        },
        children=[
            html.H4(f"{model_name} Training Diagnostics", style={"fontWeight": "bold", "color": "#495057"}),
            dcc.Graph(id=graph_id, style={"width": "100%", "height": "300px"}),
            html.Div(
                style={"marginTop": "15px", "padding": "10px", "borderRadius": "5px", "backgroundColor": "#f8f9fa", "width": "100%", "textAlign": "center", "border": "1px dashed #ced4da"},
                children=[
                    html.Span("Test Set MSE: ", style={"fontWeight": "bold", "color": "#6c757d"}),
                    html.Span("Waiting...", id=mse_label_id, style={"fontWeight": "bold", "color": "#dc3545", "fontSize": "16px"}),
                ],
            ),
        ],
    )


def get_screen2_layout() -> html.Div:
    """Returns the visual layout structure for Screen 2 (Training Progress Metrics)."""
    return html.Div(
        style={"padding": "30px", "backgroundColor": "#f8f9fa", "minHeight": "100vh", "display": "flex", "flexDirection": "column", "alignItems": "center"},
        children=[
            # Header & Progress Spinner
            html.Div(
                style={"textAlign": "center", "marginBottom": "30px"},
                children=[
                    html.H2("Asynchronous Deep Learning Model Training", style={"fontWeight": "bold", "color": "#212529"}),
                    html.Div(
                        style={"display": "flex", "justifyContent": "center", "alignItems": "center", "marginTop": "15px"},
                        children=[
                            html.Div(style={"border": "4px solid #f3f3f3", "borderTop": "4px solid #0d6efd", "borderRadius": "50%", "width": "30px", "height": "30px", "animation": "spin 1s linear infinite", "marginRight": "15px"}),
                            html.H5("Training in progress...", id="training-status-text", style={"color": "#0d6efd", "margin": "0"}),
                        ],
                    ),
                ],
            ),
            # Hidden interval to fetch training updates asynchronously
            dcc.Interval(id="training-interval", interval=500, n_intervals=0, disabled=False),
            # Hidden stores to track metrics progress asynchronously
            dcc.Store(id="store-epoch-progress", data=0),
            dcc.Store(id="store-training-history", data={}),
            # Cartesian Plots Row
            html.Div(
                style={"display": "flex", "justifyContent": "space-between", "width": "100%", "maxWidth": "1200px", "marginTop": "10px"},
                children=[
                    get_model_training_box("FCN", "plot-fcn-training", "lbl-fcn-test-mse"),
                    get_model_training_box("RNN", "plot-rnn-training", "lbl-rnn-test-mse"),
                    get_model_training_box("LSTM", "plot-lstm-training", "lbl-lstm-test-mse"),
                ],
            ),
            # Navigation Row
            html.Div(
                style={"display": "flex", "justifyContent": "center", "marginTop": "40px", "width": "100%"},
                children=[
                    html.Button(
                        "Lets play",
                        id="btn-go-to-playground",
                        n_clicks=0,
                        disabled=True,  # Start disabled, enabled via callback once complete
                        style={
                            "padding": "15px 65px",
                            "fontSize": "20px",
                            "fontWeight": "bold",
                            "borderRadius": "8px",
                            "border": "none",
                            "backgroundColor": "#6c757d",  # Start grey, transitions to blue once active
                            "color": "#ffffff",
                            "cursor": "not-allowed",
                            "boxShadow": "0 4px 6px rgba(0,0,0,0.05)",
                        },
                    )
                ],
            ),
            # Embed simple spin visual keyframes animation
            html.Div(
                children=[
                    html.Iframe(
                        style={"display": "none"},
                        srcDoc="<style>@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }</style>"
                    )
                ]
            ),
        ],
    )
