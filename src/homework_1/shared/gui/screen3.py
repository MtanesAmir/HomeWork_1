"""GUI Screen 3 layout module.

Signal Reconstruction interactive playground displaying slice generators,
continuous-dots switches, one-hot segmented bars, three prediction grids,
and safe exit server termination controls.
"""

from dash import dcc, html


def get_playground_prediction_box(model_name: str, graph_id: str) -> html.Div:
    """Creates an individual Cartesian plot grid box for a model reconstruction prediction."""
    return html.Div(
        style={
            "width": "31%",
            "backgroundColor": "#ffffff",
            "padding": "15px",
            "borderRadius": "10px",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)",
        },
        children=[
            html.H5(f"{model_name} Reconstruction", style={"fontWeight": "bold", "textAlign": "center", "color": "#495057"}),
            dcc.Graph(id=graph_id, style={"height": "260px"}),
        ],
    )


def get_screen3_layout() -> html.Div:
    """Returns the visual layout structure for Screen 3 (Interactive Signal Playground)."""
    return html.Div(
        style={"padding": "20px", "backgroundColor": "#f8f9fa", "minHeight": "100vh", "display": "flex", "flexDirection": "column", "alignItems": "center"},
        children=[
            # Header Section
            html.H2("Interactive Signal Reconstruction Playground", style={"fontWeight": "bold", "color": "#212529", "marginBottom": "20px"}),
            # Top Section (Slice Input Sum plot and Selector options)
            html.Div(
                style={"display": "flex", "flexDirection": "row", "width": "100%", "maxWidth": "1100px", "justifyContent": "space-between", "marginBottom": "25px"},
                children=[
                    # Sliced Sum Graph Box
                    html.Div(
                        style={"width": "60%", "backgroundColor": "#ffffff", "padding": "15px", "borderRadius": "10px", "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)"},
                        children=[
                            html.Div(
                                style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "10px"},
                                children=[
                                    html.H5("Composite Summed Signal Window (Input)", style={"fontWeight": "bold", "margin": "0"}),
                                    html.Button("Generate Slice", id="btn-playground-generate", n_clicks=0, style={"padding": "8px 20px", "fontWeight": "bold", "backgroundColor": "#198754", "color": "#ffffff", "border": "none", "borderRadius": "5px", "cursor": "pointer"}),
                                ],
                            ),
                            dcc.Graph(id="plot-playground-sum-slice", style={"height": "250px"}),
                        ],
                    ),
                    # One-Hot Mask Selector Box
                    html.Div(
                        style={"width": "36%", "backgroundColor": "#ffffff", "padding": "20px", "borderRadius": "10px", "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)", "display": "flex", "flexDirection": "column", "justifyContent": "space-between"},
                        children=[
                            html.Div(
                                children=[
                                    html.H5("Target Component Selector", style={"fontWeight": "bold"}),
                                    html.P("Choose the clean sinus component wave you want the models to extract blindly from the composite mixture:", style={"color": "#6c757d", "fontSize": "13px"}),
                                    # Segmented Bar Choice (1 to 4)
                                    dcc.RadioItems(
                                        id="choice-one-hot-mask",
                                        options=[
                                            {"label": "Sinusoid 1 (Selector [1,0,0,0])", "value": "1"},
                                            {"label": "Sinusoid 2 (Selector [0,1,0,0])", "value": "2"},
                                            {"label": "Sinusoid 3 (Selector [0,0,1,0])", "value": "3"},
                                            {"label": "Sinusoid 4 (Selector [0,0,0,1])", "value": "4"},
                                        ],
                                        value="1",
                                        labelStyle={"display": "block", "padding": "8px 12px", "margin": "8px 0", "border": "1px solid #dee2e6", "borderRadius": "5px", "cursor": "pointer", "backgroundColor": "#f8f9fa"},
                                        inputStyle={"marginRight": "10px"},
                                    ),
                                ]
                            ),
                            # Visual plot style toggle controls
                            html.Div(
                                style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginTop": "10px"},
                                children=[
                                    html.Label("Plotting Style:", style={"fontWeight": "bold", "margin": "0"}),
                                    dcc.RadioItems(id="toggle-dots-lines", options=[{"label": "Continuous lines", "value": "lines"}, {"label": "Discrete dots", "value": "markers"}], value="lines", labelStyle={"display": "inline-block", "marginRight": "15px"}),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Hidden stores to track playground slice index and data
            dcc.Store(id="store-playground-slice-idx", data=0),
            # Models Prediction Dashboards (FCN, RNN, LSTM side-by-side)
            html.Div(
                style={"display": "flex", "justifyContent": "space-between", "width": "100%", "maxWidth": "1100px"},
                children=[
                    get_playground_prediction_box("FCN", "plot-predict-fcn"),
                    get_playground_prediction_box("RNN", "plot-predict-rnn"),
                    get_playground_prediction_box("LSTM", "plot-predict-lstm"),
                ],
            ),
            # Exit safe server shutdown action row
            html.Div(
                style={"marginTop": "35px", "display": "flex", "justifyContent": "center", "width": "100%"},
                children=[
                    html.Button(
                        "Exit Dashboard",
                        id="btn-exit-dashboard",
                        n_clicks=0,
                        style={
                            "padding": "12px 45px",
                            "fontSize": "16px",
                            "fontWeight": "bold",
                            "backgroundColor": "#dc3545",
                            "color": "#ffffff",
                            "border": "none",
                            "borderRadius": "6px",
                            "cursor": "pointer",
                            "boxShadow": "0 4px 6px rgba(220, 53, 69, 0.3)",
                        },
                    )
                ],
            ),
        ],
    )


def get_screen4_layout() -> html.Div:
    """Returns the visual layout structure for Screen 4 (Delayed Safe Exit Splash View)."""
    return html.Div(
        style={"padding": "50px", "backgroundColor": "#f8f9fa", "minHeight": "100vh", "display": "flex", "flexDirection": "column", "alignItems": "center", "justifyContent": "center"},
        children=[
            html.Div(
                style={"textAlign": "center", "backgroundColor": "#ffffff", "padding": "50px", "borderRadius": "15px", "boxShadow": "0 10px 25px rgba(0, 0, 0, 0.05)", "maxWidth": "600px"},
                children=[
                    html.H1("Bye Bye, hope you enjoy!!", style={"fontWeight": "bold", "color": "#dc3545", "marginBottom": "20px"}),
                    html.P("Visual dashboard server is shutting down safely in the background.", style={"fontSize": "16px", "color": "#495057", "marginBottom": "10px"}),
                    html.P("You can now safely close this browser tab.", style={"fontSize": "14px", "color": "#6c757d"}),
                ]
            )
        ]
    )
