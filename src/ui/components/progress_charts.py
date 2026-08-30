"""Figuras analíticas da tela de progresso."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import plotly.graph_objects as go


def subject_progress_figure(summary: Sequence[dict[str, Any]]) -> go.Figure:
    """Cria comparação de minutos planejados e concluídos por disciplina."""
    labels = [row["disciplina"] for row in summary]
    figure = go.Figure(
        data=[
            go.Bar(
                name="Planejados",
                x=[row["planejados"] for row in summary],
                y=labels,
                orientation="h",
                hovertemplate="%{y}<br>Planejados: %{x} min<extra></extra>",
            ),
            go.Bar(
                name="Concluídos",
                x=[row["concluídos"] for row in summary],
                y=labels,
                orientation="h",
                hovertemplate="%{y}<br>Concluídos: %{x} min<extra></extra>",
            ),
        ]
    )
    figure.update_layout(
        barmode="group",
        height=max(260, 70 * len(summary)),
        margin={"l": 8, "r": 8, "t": 12, "b": 12},
        legend={"orientation": "h", "y": 1.08, "x": 0},
        xaxis_title="Minutos",
        yaxis_title=None,
    )
    return figure


def weekly_progress_figure(summary: Sequence[dict[str, Any]]) -> go.Figure:
    """Cria a evolução diária de minutos planejados e concluídos."""
    figure = go.Figure(
        data=[
            go.Scatter(
                name="Planejados",
                x=[row["dia"] for row in summary],
                y=[row["planejados"] for row in summary],
                mode="lines+markers",
                hovertemplate="%{x}<br>Planejados: %{y} min<extra></extra>",
            ),
            go.Scatter(
                name="Concluídos",
                x=[row["dia"] for row in summary],
                y=[row["concluídos"] for row in summary],
                mode="lines+markers",
                hovertemplate="%{x}<br>Concluídos: %{y} min<extra></extra>",
            ),
        ]
    )
    figure.update_layout(
        height=320,
        margin={"l": 8, "r": 8, "t": 12, "b": 12},
        legend={"orientation": "h", "y": 1.08, "x": 0},
        yaxis_title="Minutos",
        xaxis_title=None,
    )
    return figure
