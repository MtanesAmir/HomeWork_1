"""Visual plots generator helper module.

Offloads figure drawing matrix operations to keep GUI entry points lightweight.
"""

import math
from typing import Any, Tuple, List
import plotly.graph_objs as go


def compute_and_draw_screen1_plots(*args: Any) -> Tuple[go.Figure, go.Figure, List[List[float]], List[float]]:
    """Computes sinusoid coordinate curves and returns Cartesian components and summed Plotly Figures."""
    waves = []
    for i in range(4):
        waves.append((args[i * 3 + 2], args[i * 3], args[i * 3 + 1]))

    t_samples = [k / 100.0 for k in range(1000)]
    base_signals = []
    for amp, freq, phase in waves:
        base_signals.append([amp * math.sin(2 * math.pi * freq * t + phase) for t in t_samples])

    sum_signal = [sum(base_signals[i][k] for i in range(4)) for k in range(1000)]

    fig_overlay = go.Figure()
    for idx, sig in enumerate(base_signals):
        fig_overlay.add_trace(go.Scatter(x=t_samples, y=sig, name=f"Sinusoid {idx + 1}"))
    fig_overlay.update_layout(
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        height=220,  # Restricts height to fit on a single screen
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
    )

    fig_sum = go.Figure()
    fig_sum.add_trace(go.Scatter(x=t_samples, y=sum_signal, line_color="#0d6efd", name="Sum"))
    fig_sum.update_layout(
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        height=220,  # Restricts height to fit on a single screen
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
    )

    return fig_overlay, fig_sum, base_signals, sum_signal
