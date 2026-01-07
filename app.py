from __future__ import annotations

import os
import pandas as pd
import streamlit as st

from src.data_loader import read_processed_parquet, find_source_files, load_streaming_history
from src.data_processor import process_streaming_history
from src.analytics import kpis, top_artists, daily_trend, hours_by_hour_dow
from src.visualizations import gauge_avg_hours, bar_top_artists, line_daily, heatmap_hour_dow

st.set_page_config(page_title="Spotify Analytics", layout="wide")

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    # Prefer processed parquet
    parquet_path = os.path.join("data", "processed", "streaming_history.parquet")
    df = read_processed_parquet(parquet_path)
    if df is not None and not df.empty:
        return df

    # Fallback to raw JSON from discovered folder
    paths = find_source_files()
    df_raw = load_streaming_history(paths.streaming_music)
    return process_streaming_history(df_raw)


def sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")
    if df.empty:
        st.sidebar.info("No data available. Prepare data first.")
        return df

    min_d = pd.to_datetime(df["date"]).min().date()
    max_d = pd.to_datetime(df["date"]).max().date()
    date_range = st.sidebar.date_input("Date range", [min_d, max_d])
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start, end = date_range
        mask = (pd.to_datetime(df["date"]) >= pd.to_datetime(start)) & (pd.to_datetime(df["date"]) <= pd.to_datetime(end))
        dff = df.loc[mask].copy()
    else:
        dff = df.copy()

    artists = sorted([a for a in dff["artistName"].unique() if a])
    picked = st.sidebar.multiselect("Artists", artists, default=[])
    if picked:
        dff = dff[dff["artistName"].isin(picked)]

    return dff


def main() -> None:
    st.title("Spotify Listening Analytics")
    df = load_data()
    dff = sidebar_filters(df)

    # KPIs
    m = kpis(dff)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Plays", f"{m['plays']:,}")
    c2.metric("Listening Hours", f"{m['hours']:.1f}")
    c3.metric("Unique Artists", f"{m['unique_artists']:,}")
    c4.metric("Unique Tracks", f"{m['unique_tracks']:,}")

    # Gauge for avg hours/day
    daily = daily_trend(dff)
    avg = float(daily["hoursPlayed"].mean()) if not daily.empty else 0.0
    st.plotly_chart(gauge_avg_hours(avg), use_container_width=True)

    # Charts row
    colA, colB = st.columns(2)
    colA.plotly_chart(bar_top_artists(top_artists(dff, 10)), use_container_width=True)
    colB.plotly_chart(line_daily(daily), use_container_width=True)

    # Heatmap section
    st.subheader("When do you listen?")
    heat_df = hours_by_hour_dow(dff)
    st.plotly_chart(heatmap_hour_dow(heat_df), use_container_width=True)

    with st.expander("Preview Data"):
        st.dataframe(dff.head(500))


if __name__ == "__main__":
    main()
