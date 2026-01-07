# Spotify Analytics Dashboard

Interactive Streamlit dashboard for exploring your Spotify listening history. It parses the exported "Spotify Account Data" JSON files and presents KPIs, trends, and insights.

## Features
- KPIs: total plays, listening hours, unique artists/tracks
- Filters: date range and artist selection
- Charts: top artists, daily listening trend, and a gauge for avg hours/day
- Caching and pre-processing to keep it snappy

## Project Structure
```
spotify-analytics-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_processor.py
│   ├── analytics.py
│   └── visualizations.py
└── scripts/
    └── prepare_data.py
```

## Quickstart

1) Ensure your exported folder exists. In this workspace it's at:
`../Spotify Account Data` (relative to this project folder).

Optionally set the environment variable `SPOTIFY_DATA_DIR` to a custom path.

2) Create a virtual environment and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3) Prepare data (first run only). This will build `data/processed/streaming_history.parquet`:

```bash
python scripts/prepare_data.py --source "../Spotify Account Data"
```

4) Run the app:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal.

## Notes
- The app will try to use `data/processed/streaming_history.parquet` if it exists. If not, it will attempt to parse raw JSON from `SPOTIFY_DATA_DIR` or `../Spotify Account Data`.
- For large datasets, parquet is faster and smaller than CSV (requires `pyarrow`).

## License
MIT
