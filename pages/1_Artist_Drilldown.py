from __future__ import annotations

import pandas as pd
import streamlit as st

from src.data_loader import read_processed_parquet, find_source_files, load_streaming_history
from src.data_processor import process_streaming_history
from src.analytics import top_artists, artist_top_tracks, artist_daily_trend
from src.visualizations import bar_top_artists, bar_top_tracks, line_daily

st.set_page_config(page_title="Artist Drilldown", layout="wide")

@st.cache_data(show_spinner=False)
def _load() -> pd.DataFrame:
    df = read_processed_parquet("data/processed/streaming_history.parquet")
    if df is not None and not df.empty:
        return df
    paths = find_source_files()
    return process_streaming_history(load_streaming_history(paths.streaming_music))


def main() -> None:
    st.title("Artist Drilldown")
    df = _load()
    artists = sorted([a for a in df["artistName"].unique() if a])
    artist = st.selectbox("Choose an artist", artists)

    if artist:
        col1, col2 = st.columns(2)
        col1.plotly_chart(bar_top_artists(top_artists(df[df["artistName"] == artist], 1)), use_container_width=True)
        tracks = artist_top_tracks(df, artist, 20)
        col2.plotly_chart(bar_top_tracks(tracks), use_container_width=True)

        st.subheader("Daily trend")
        st.plotly_chart(line_daily(artist_daily_trend(df, artist)), use_container_width=True)


if __name__ == "__main__":
    main()
