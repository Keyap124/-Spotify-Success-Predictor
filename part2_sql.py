import pandas as pd
import sqlite3

api_data = pd.read_csv("spotify_tracks_artists.csv")
static_data = pd.read_csv("spotify_dataset.csv")

audio_features = static_data[[
    'track_id', 'track_name', 'artists',
    'danceability', 'energy', 'key', 'loudness', 'mode',
    'speechiness', 'acousticness', 'instrumentalness',
    'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature'
]].copy()

audio_features.rename(columns={
    'artists': 'artist_name_static',
    'duration_ms': 'duration'
}, inplace=True)

audio_features.drop_duplicates(subset=['track_id'], inplace=True)
audio_features.dropna(subset=['track_id'], inplace=True)
audio_features['track_id'] = audio_features['track_id'].astype(str).str.strip()
audio_features.to_csv("audio_features_2023_cleaned.csv", index=False)

tracks = api_data[['track_id','track_name','album_name','release_date','explicit',
                   'track_popularity','artist_id','artist_name']].copy()

artists = api_data[['artist_id','artist_name','artist_popularity','artist_genres']]\
          .drop_duplicates(subset=['artist_id'])

conn = sqlite3.connect("spotify_2023_database.db")

tracks.to_sql("Tracks", conn, if_exists="replace", index=False)
artists.to_sql("Artists", conn, if_exists="replace", index=False)
audio_features.to_sql("AudioFeatures", conn, if_exists="replace", index=False)

merge_query = """
CREATE VIEW merged_dataset AS
SELECT 
    t.*,
    a.artist_popularity,
    a.artist_genres,
    af.danceability,
    af.energy,
    af.loudness,
    af.acousticness,
    af.instrumentalness,
    af.liveness,
    af.valence,
    af.tempo,
    af.duration,
    af.speechiness,
    af.key,
    af.mode,
    af.time_signature
FROM Tracks t
JOIN Artists a ON t.artist_id = a.artist_id
LEFT JOIN AudioFeatures af ON t.track_id = af.track_id
"""

conn.execute("DROP VIEW IF EXISTS merged_dataset;")
conn.execute(merge_query)

final = pd.read_sql_query("SELECT * FROM merged_dataset", conn)
final.to_csv("spotify_2023_complete_dataset.csv", index=False)

conn.close()
