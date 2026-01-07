from __future__ import annotations

"""
Generate a simple static image from processed data to include in README.
This avoids needing a running server for the screenshot.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

p = Path('data/processed/streaming_history.parquet')
df = pd.read_parquet(p)

if 'hoursPlayed' not in df and 'msPlayed' in df:
    df['hoursPlayed'] = df['msPlayed'] / 3_600_000.0

et = pd.to_datetime(df.get('endTime', df.get('date')), errors='coerce')
df = df[~et.isna()].copy()
df['hour'] = et.dt.hour
by_hour = df.groupby('hour', as_index=False)['hoursPlayed'].sum()

sns.set_theme(style='darkgrid')
plt.figure(figsize=(9,4))
sns.barplot(data=by_hour, x='hour', y='hoursPlayed', color='#1DB954')
plt.title('Listening Hours by Hour of Day')
plt.xlabel('Hour')
plt.ylabel('Hours')
plt.tight_layout()
Path('assets').mkdir(exist_ok=True)
plt.savefig('assets/overview.png', dpi=140)
print('Saved assets/overview.png')
