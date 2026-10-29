import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "spotify_tracks.csv"
OUTPUT_FILE = BASE_DIR / "output" / "cleaned_spotify_tracks.csv"

# 1. Extract
df = pd.read_csv(INPUT_FILE)

# 2. Transform
# Standardize column headers
df.columns = df.columns.str.strip().str.lower()

# Remove duplicate songs based on track_id
df = df.drop_duplicates(subset=["track_id"])

# Clean text fields
df["track_name"] = df["track_name"].str.strip()
df["artist_name"] = df["artist_name"].str.strip()
df["album"] = df["album"].str.strip()
df["genre"] = df["genre"].str.strip().str.title()

# Numeric conversions & calculations
df["streams"] = pd.to_numeric(df["streams"], errors="coerce")
df["duration_ms"] = pd.to_numeric(df["duration_ms"], errors="coerce")
df["danceability"] = pd.to_numeric(df["danceability"], errors="coerce")
df["energy"] = pd.to_numeric(df["energy"], errors="coerce")

df = df.dropna(subset=["track_id", "streams", "artist_name"])

# Calculate Duration in Minutes & Estimated Royalty Revenue ($0.0035 per stream avg)
df["duration_min"] = (df["duration_ms"] / 60000).round(2)
df["estimated_revenue_usd"] = (df["streams"] * 0.0035).round(2)

# Sort by Top Streams
df = df.sort_values(by="streams", ascending=False)

# 3. Load
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print("Spotify AWS ETL pipeline completed successfully!")
print("Total Unique Tracks:", len(df))
print("Total Streams:", f"{df['streams'].sum():,}")
print("Estimated Revenue (USD):", f"${df['estimated_revenue_usd'].sum():,}")
print("Output file written to:", OUTPUT_FILE)
