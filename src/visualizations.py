from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def gauge_avg_hours(avg_hours: float) -> go.Figure:
    rng = max(2.0, (avg_hours or 0) * 2)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_hours or 0,
        title={"text": "Avg Hours / Day"},
        gauge={
            "axis": {"range": [0, rng]},
            "bar": {"color": "#1DB954"},
            "bgcolor": "#222",
        },
    ))
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


def bar_top_artists(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(df, x="artistName", y="hoursPlayed", title="Top Artists (Hours)")
    fig.update_layout(xaxis_title="Artist", yaxis_title="Hours", margin=dict(l=10, r=10, t=40, b=10))
    return fig


def line_daily(df: pd.DataFrame) -> go.Figure:
    fig = px.line(df, x="date", y="hoursPlayed", title="Daily Listening Hours")
    fig.update_layout(xaxis_title="Date", yaxis_title="Hours", margin=dict(l=10, r=10, t=40, b=10))
    return fig


def heatmap_hour_dow(df: pd.DataFrame) -> go.Figure:
    """Draw a heatmap with day_of_week on y, hour on x, color=hoursPlayed."""
    if df.empty:
        # Build an empty figure
        fig = go.Figure()
        fig.update_layout(title="Listening Heatmap (Hour x Day)")
        return fig
    # Pivot for heatmap
    pivot = df.pivot(index="day_of_week", columns="hour", values="hoursPlayed").fillna(0)
    fig = px.imshow(
        pivot,
        labels=dict(x="Hour", y="Day of Week", color="Hours"),
        title="Listening Heatmap (Hour x Day)",
        color_continuous_scale=["#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#1DB954"],
        aspect="auto",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


def bar_top_tracks(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(df, x="trackName", y="hoursPlayed", title="Top Tracks (Hours)")
    fig.update_layout(xaxis_title="Track", yaxis_title="Hours", margin=dict(l=10, r=10, t=40, b=10))
    fig.update_xaxes(tickangle=45)
    return fig
