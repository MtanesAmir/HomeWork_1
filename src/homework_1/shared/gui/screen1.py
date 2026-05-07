"""GUI Screen 1 layout module.

Wave configurations sidebar, sinusoid tuning sliders cards, real-time Cartesian
individual sinusoid overlays and clean sum plots layout.
"""

from dash import dcc, html


def get_sinusoid_card(idx: int, default_freq: float, default_phase: float, default_amp: float) -> html.Div:
    """Creates a clean, styled card containing tuning sliders for a single sinusoid."""
    return html.Div(
        style={
            "border": "2px solid #e9ecef",
            "borderRadius": "10px",
            "padding": "15px",
            "margin": "10px",
            "width": "22%",
            "backgroundColor": "#ffffff",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)",
        },
        children=[
            html.H5(f"Sinusoid {idx}", style={"textAlign": "center", "fontWeight": "bold", "color": "#495057"}),
            html.Label("Freq (Hz)", style={"fontWeight": "bold", "marginTop": "5px"}),
            dcc.Slider(id=f"freq-{idx}", min=0.1, max=50.0, step=0.1, value=default_freq, tooltip={"placement": "bottom"}),
            html.Label("Phase (rad)", style={"fontWeight": "bold", "marginTop": "5px"}),
            dcc.Slider(id=f"phase-{idx}", min=-6.28, max=6.28, step=0.1, value=default_phase, tooltip={"placement": "bottom"}),
            html.Label("Amp", style={"fontWeight": "bold", "marginTop": "5px"}),
            dcc.Slider(id=f"amp-{idx}", min=0.0, max=2.0, step=0.1, value=default_amp, tooltip={"placement": "bottom"}),
        ],
    )


def get_screen1_layout() -> html.Div:
    """Returns the visual structure for Screen 1 (Configuration & Tuning Dashboard)."""
    return html.Div(
        style={"display": "flex", "flexDirection": "row", "padding": "20px", "backgroundColor": "#f8f9fa", "minHeight": "100vh"},
        children=[
            # Left Sidebar Configuration Controls
            html.Div(
                style={"width": "25%", "padding": "20px", "backgroundColor": "#ffffff", "borderRadius": "10px", "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)", "marginRight": "20px"},
                children=[
                    html.H3("Global Configurations", style={"fontWeight": "bold", "color": "#343a40"}),
                    html.Hr(),
                    html.Label("Number of Epochs", style={"fontWeight": "bold"}),
                    dcc.Input(id="input-epochs", type="number", value=50, min=10, max=500, style={"width": "100%", "padding": "8px", "marginBottom": "15px", "borderRadius": "5px", "border": "1px solid #ced4da"}),
                    html.Label("Dataset Size (Rows)", style={"fontWeight": "bold"}),
                    dcc.Input(id="input-dataset-size", type="number", value=500, min=50, max=5000, style={"width": "100%", "padding": "8px", "marginBottom": "15px", "borderRadius": "5px", "border": "1px solid #ced4da"}),
                    html.Label("Noise Ratio", style={"fontWeight": "bold"}),
                    dcc.Slider(id="slider-noise", min=0.0, max=0.5, step=0.01, value=0.05, tooltip={"placement": "bottom"}),
                    html.Div(style={"height": "15px"}),
                    html.Label("Train Split (%)", style={"fontWeight": "bold"}),
                    dcc.Input(id="input-train-pct", type="number", value=70.0, style={"width": "100%", "padding": "8px", "marginBottom": "15px", "borderRadius": "5px", "border": "1px solid #ced4da"}),
                    html.Label("Val Split (%)", style={"fontWeight": "bold"}),
                    dcc.Input(id="input-val-pct", type="number", value=15.0, style={"width": "100%", "padding": "8px", "marginBottom": "15px", "borderRadius": "5px", "border": "1px solid #ced4da"}),
                    html.Label("Test Split (%)", style={"fontWeight": "bold"}),
                    dcc.Input(id="input-test-pct", type="number", value=15.0, style={"width": "100%", "padding": "8px", "marginBottom": "15px", "borderRadius": "5px", "border": "1px solid #ced4da"}),
                    html.Hr(),
                    html.Label("FCN Hidden Layers", style={"fontWeight": "bold"}),
                    dcc.Input(id="input-fcn-layers", type="text", value="3, 5, 3", style={"width": "100%", "padding": "8px", "marginBottom": "15px", "borderRadius": "5px", "border": "1px solid #ced4da"}),
                    html.Label("RNN Hidden Layers", style={"fontWeight": "bold"}),
                    dcc.Input(id="input-rnn-layers", type="text", value="8", style={"width": "100%", "padding": "8px", "marginBottom": "15px", "borderRadius": "5px", "border": "1px solid #ced4da"}),
                    html.Label("LSTM Hidden Layers", style={"fontWeight": "bold"}),
                    dcc.Input(id="input-lstm-layers", type="text", value="6", style={"width": "100%", "padding": "8px", "marginBottom": "15px", "borderRadius": "5px", "border": "1px solid #ced4da"}),
                ],
            ),
            # Right Panel Content (Cards + Plots)
            html.Div(
                style={"width": "75%", "display": "flex", "flexDirection": "column"},
                children=[
                    # Top Cards Row
                    html.Div(
                        style={"display": "flex", "justifyContent": "space-between"},
                        children=[
                            get_sinusoid_card(1, 5.0, 0.0, 1.0),
                            get_sinusoid_card(2, 10.0, 0.5, 1.5),
                            get_sinusoid_card(3, 15.0, 1.0, 2.0),
                            get_sinusoid_card(4, 20.0, 1.5, 0.5),
                        ],
                    ),
                    # Alerts Section
                    html.Div(id="validation-alert-container", style={"marginTop": "10px"}),
                    # Cartesian Plots Grid
                    html.Div(
                        style={"display": "flex", "justifyContent": "space-between", "marginTop": "20px"},
                        children=[
                            html.Div(
                                style={"width": "48%", "backgroundColor": "#ffffff", "padding": "15px", "borderRadius": "10px", "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)"},
                                children=[
                                    html.H5("Sinusoidal Wave Overlays", style={"fontWeight": "bold", "textAlign": "center"}),
                                    dcc.Graph(id="plot-components-overlay"),
                                ],
                            ),
                            html.Div(
                                style={"width": "48%", "backgroundColor": "#ffffff", "padding": "15px", "borderRadius": "10px", "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)"},
                                children=[
                                    html.H5("Clean Composite Sum Signal", style={"fontWeight": "bold", "textAlign": "center"}),
                                    dcc.Graph(id="plot-sum-signal"),
                                ],
                            ),
                        ],
                    ),
                    # Action Trigger Row
                    html.Div(
                        style={"display": "flex", "justifyContent": "center", "marginTop": "30px"},
                        children=[
                            html.Button(
                                "Let the models learn",
                                id="btn-start-training",
                                n_clicks=0,
                                style={
                                    "padding": "15px 40px",
                                    "fontSize": "18px",
                                    "fontWeight": "bold",
                                    "backgroundColor": "#0d6efd",
                                    "color": "#ffffff",
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "cursor": "pointer",
                                    "boxShadow": "0 4px 6px rgba(13, 110, 253, 0.3)",
                                },
                            )
                        ],
                    ),
                ],
            ),
        ],
    )
