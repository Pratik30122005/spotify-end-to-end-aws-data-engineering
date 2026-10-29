# 🎵 Spotify End-to-End AWS Data Engineering Pipeline

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://spotify-end-to-end-aws-data-engineering.streamlit.app/)

An automated, serverless streaming music analytics data engineering pipeline built on AWS and Python.

## 🌟 Architecture Overview
1. **Raw Ingestion (Amazon S3)**: Raw track streaming event logs (`data/spotify_tracks.csv`) ingested from the Spotify Web API.
2. **Serverless ETL (AWS Lambda & Pandas)**: Automated event trigger executes deduplication, feature extraction (duration in minutes, acoustic scores), and royalty calculations ($0.0035 / stream).
3. **Data Lake Storage (Amazon S3)**: Processed, analytics-ready datasets stored in the S3 processed bucket.
4. **Interactive Analytics (Amazon Athena & Streamlit UI)**: Real-time SQL querying and streaming analytics dashboard.

## 📊 Dataset Schema
- `track_id`: Unique track identifier
- `track_name`: Track title
- `artist_name`: Performing artist
- `album`: Album name
- `genre`: Music genre (Pop, R&B, Hip-Hop, etc.)
- `streams`: Total global streams
- `duration_ms`: Duration in milliseconds
- `danceability`: Audio metric (0.0 to 1.0)
- `energy`: Acoustic intensity (0.0 to 1.0)
- `release_date`: Official release date

## 🚀 Running Locally
```bash
# Clone the repository
git clone https://github.com/Pratik30122005/spotify-end-to-end-aws-data-engineering.git
cd spotify-end-to-end-aws-data-engineering

# Install dependencies
pip install -r requirements.txt

# Run ETL script
python scripts/transform.py

# Launch Spotify Analytics Dashboard
streamlit run app.py
```
