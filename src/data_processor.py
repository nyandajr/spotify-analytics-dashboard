from __future__ import annotations

import os
import pandas as pd


def process_streaming_history(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich the raw streaming history frame.

    Input columns: endTime (str), artistName (str), trackName (str), msPlayed (int)
    Output columns include parsed datetime features and derived metrics.
    """
    if df.empty:
        return df.assign(
            endTime=pd.to_datetime(pd.Series([], dtype="datetime64[ns]")),
            date=pd.Series([], dtype="datetime64[ns]"),
            year=pd.Series([], dtype="Int64"),
            month=pd.Series([], dtype="Int64"),
            day=pd.Series([], dtype="Int64"),
            hour=pd.Series([], dtype="Int64"),
            minutesPlayed=pd.Series([], dtype="float"),
            hoursPlayed=pd.Series([], dtype="float"),
        )

    out = df.copy()
    out["endTime"] = pd.to_datetime(out["endTime"], errors="coerce")
    out = out.dropna(subset=["endTime"]).reset_index(drop=True)

    out["date"] = out["endTime"].dt.date
    out["year"] = out["endTime"].dt.year.astype("Int64")
    out["month"] = out["endTime"].dt.month.astype("Int64")
    out["day"] = out["endTime"].dt.day.astype("Int64")
    out["hour"] = out["endTime"].dt.hour.astype("Int64")

    out["msPlayed"] = pd.to_numeric(out["msPlayed"], errors="coerce").fillna(0).astype(int)
    out["minutesPlayed"] = out["msPlayed"] / 60000.0
    out["hoursPlayed"] = out["msPlayed"] / 3_600_000.0

    # Clean strings
    for col in ["artistName", "trackName"]:
        if col in out.columns:
            out[col] = out[col].fillna("").astype(str).str.strip()

    return out


def save_parquet(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, index=False)
