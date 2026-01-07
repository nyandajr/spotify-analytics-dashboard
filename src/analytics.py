from __future__ import annotations

import pandas as pd


def kpis(df: pd.DataFrame) -> dict:
    plays = len(df)
    hours = float(df["hoursPlayed"].sum()) if "hoursPlayed" in df.columns else 0.0
    unique_artists = int(df["artistName"].nunique()) if "artistName" in df.columns else 0
    unique_tracks = int(df["trackName"].nunique()) if "trackName" in df.columns else 0
    return {
        "plays": plays,
        "hours": hours,
        "unique_artists": unique_artists,
        "unique_tracks": unique_tracks,
    }


def top_artists(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["artistName", "hoursPlayed"])  # empty
    return (
        df.groupby("artistName", as_index=False)["hoursPlayed"].sum()
          .sort_values("hoursPlayed", ascending=False)
          .head(n)
    )


def daily_trend(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["date", "hoursPlayed"])  # empty
    return (
        df.groupby("date", as_index=False)["hoursPlayed"].sum()
          .sort_values("date")
    )


def hours_by_hour_dow(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate hoursPlayed by hour of day and day of week.

    Returns a tidy dataframe with columns: day_of_week (Mon..Sun), hour (0-23), hoursPlayed.
    Suitable for heatmap plotting.
    """
    if df.empty:
        return pd.DataFrame(columns=["day_of_week", "hour", "hoursPlayed"])  # empty

    work = df.copy()
    # Derive day_of_week using datetime; ensure ordering Mon..Sun
    work["endTime"] = pd.to_datetime(work["endTime"], errors="coerce")
    work = work.dropna(subset=["endTime"]).copy()
    work["day_of_week"] = work["endTime"].dt.day_name()
    # Order days
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    work["day_of_week"] = pd.Categorical(work["day_of_week"], categories=order, ordered=True)

    # Ensure hour column exists/int
    if "hour" not in work.columns:
        work["hour"] = work["endTime"].dt.hour

    agg = (work.groupby(["day_of_week", "hour"], as_index=False)["hoursPlayed"].sum()
                .sort_values(["day_of_week", "hour"]))
    return agg


def artist_top_tracks(df: pd.DataFrame, artist: str, n: int = 15) -> pd.DataFrame:
    if df.empty or not artist:
        return pd.DataFrame(columns=["trackName", "hoursPlayed"])  # empty
    filt = df[df["artistName"] == artist]
    return (
        filt.groupby("trackName", as_index=False)["hoursPlayed"].sum()
            .sort_values("hoursPlayed", ascending=False)
            .head(n)
    )


def artist_daily_trend(df: pd.DataFrame, artist: str) -> pd.DataFrame:
    if df.empty or not artist:
        return pd.DataFrame(columns=["date", "hoursPlayed"])  # empty
    filt = df[df["artistName"] == artist]
    return (
        filt.groupby("date", as_index=False)["hoursPlayed"].sum()
            .sort_values("date")
    )
