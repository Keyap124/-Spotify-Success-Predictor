import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

def main():
    print("Starting Spotify metadata script...")

    # ---- AUTHENTICATION ----
    auth_manager = SpotifyClientCredentials(
        client_id="8617b8f3e944f483c886cf252032e0789",
        client_secret="08292efd1974415be3dfe0ba1e4ef99"
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    print("Authenticated with Spotify successfully.")

    # ---- SEARCH FOR TRACKS ----
    query = "year:2023"
    print(f"Searching for tracks with query: {query!r} ...")

    results = sp.search(q=query, type="track", limit=50)
    items = results["tracks"]["items"]
    print("Number of tracks returned from search:", len(items))

    # ---- COLLECT BASIC TRACK INFO + PRIMARY ARTIST ID ----
    track_rows = []
    artist_ids = set()

    for track in items:
        if track is None:
            continue

        track_id = track["id"]
        if track_id is None:
            continue

        track_name = track["name"]
        album_name = track["album"]["name"]
        release_date = track["album"]["release_date"]
        explicit = track.get("explicit", False)
        track_popularity = track.get("popularity", None)

        primary_artist = track["artists"][0]
        artist_id = primary_artist["id"]
        artist_name = primary_artist["name"]

        if artist_id:
            artist_ids.add(artist_id)

        track_rows.append({
            "track_id": track_id,
            "track_name": track_name,
            "album_name": album_name,
            "release_date": release_date,
            "explicit": explicit,
            "track_popularity": track_popularity,
            "artist_id": artist_id,
            "artist_name": artist_name
        })

    print("Collected basic info for", len(track_rows), "tracks.")
    print("Unique artists found:", len(artist_ids))

    # ---- FETCH ARTIST-LEVEL INFO (POPULARITY + GENRES) ----
    artist_info = {}
    artist_ids_list = list(artist_ids)
    for i in range(0, len(artist_ids_list), 50):
        batch = artist_ids_list[i:i+50]
        artists_data = sp.artists(batch)["artists"]
        for artist in artists_data:
            if artist:
                artist_info[artist["id"]] = {
                    "artist_popularity": artist["popularity"],
                    "artist_genres": ", ".join(artist["genres"])
                }

    # Add artist info to each track row
    for row in track_rows:
        info = artist_info.get(row["artist_id"], 
                              {"artist_popularity": None, "artist_genres": None})
        row.update(info)

    # Save to CSV
    df = pd.DataFrame(track_rows)
    df.to_csv("data/spotify_tracks_artists.csv", index=False)
    print("Part 1 complete! CSV saved to data/spotify_tracks_artists.csv")

if __name__ == "__main__":
    main()
