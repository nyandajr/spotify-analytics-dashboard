from __future__ import annotations

import os
import glob
import json
from dataclasses import dataclass
from typing import List, Optional

import pandas as pd


@dataclass
class SourcePaths:
    streaming_music: List[str]
    streaming_podcast: List[str]


def _default_source_dir() -> str:
    # Prefer env var, else default relative path
    return os.getenv("SPOTIFY_DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "Spotify Account Data"))


def find_source_files(source_dir: Optional[str] = None) -> SourcePaths:
    base = source_dir or _default_source_dir()
    music = sorted(glob.glob(os.path.join(base, "StreamingHistory_music_*.json")))
    podcast = sorted(glob.glob(os.path.join(base, "StreamingHistory_podcast_*.json")))
    return SourcePaths(streaming_music=music, streaming_podcast=podcast)


def load_streaming_history(paths: List[str]) -> pd.DataFrame:
    frames = []
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                frames.append(pd.DataFrame(data))
        except Exception as e:
            print(f"Failed to read {p}: {e}")
    if not frames:
        return pd.DataFrame(columns=["endTime", "artistName", "trackName", "msPlayed"])  # Spotify export schema
    df = pd.concat(frames, ignore_index=True)
    # Normalize schema
    keep = ["endTime", "artistName", "trackName", "msPlayed"]
    for col in keep:
        if col not in df.columns:
            df[col] = pd.NA
    df = df[keep]
    return df


def read_processed_parquet(parquet_path: str) -> Optional[pd.DataFrame]:
    if os.path.exists(parquet_path):
        try:
            return pd.read_parquet(parquet_path)
        except Exception as e:
            print(f"Could not read parquet {parquet_path}: {e}")
    return None
