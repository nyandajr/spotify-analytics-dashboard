from __future__ import annotations

import argparse
import os

import pandas as pd

from src.data_loader import find_source_files, load_streaming_history
from src.data_processor import process_streaming_history, save_parquet


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare Spotify streaming history parquet file")
    parser.add_argument("--source", type=str, default=None, help="Path to 'Spotify Account Data' directory")
    parser.add_argument("--out", type=str, default="data/processed/streaming_history.parquet", help="Output parquet path")
    args = parser.parse_args()

    paths = find_source_files(args.source)
    if not paths.streaming_music:
        raise SystemExit("No StreamingHistory_music_*.json files found. Provide --source pointing to your export.")

    raw = load_streaming_history(paths.streaming_music)
    proc = process_streaming_history(raw)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    save_parquet(proc, args.out)
    print(f"Saved {len(proc):,} rows to {args.out}")


if __name__ == "__main__":
    main()
