import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load API credentials
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:5000/callback"

lastfm_api_key = "bb172821d987cc8834d38d68be998fd8"  # Your Last.fm API Key

# Authenticate with Spotify to fetch songs
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-read-private playlist-read-private playlist-read-collaborative",
    cache_path=".cache"
))

def get_audio_features_lastfm(artist, track):
    """Fetches audio features from Last.fm."""
    url = "https://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getInfo",
        "api_key": lastfm_api_key,
        "artist": artist,
        "track": track,
        "format": "json"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "track" in data:
            return {
                "listeners": data["track"].get("listeners", "N/A"),
                "playcount": data["track"].get("playcount", "N/A"),
                "album": data["track"].get("album", {}).get("title", "Unknown Album"),
                "tags": [tag["name"] for tag in data["track"].get("toptags", {}).get("tag", [])][:5],
                "summary": data["track"].get("wiki", {}).get("summary", "No description available.")
            }
    except Exception as e:
        print(f"⚠️ Error fetching audio features for {track} by {artist}: {e}")
    return None

def get_playlist_tracks(playlist_id):
    """Fetches all tracks from a Spotify playlist, including album cover."""
    try:
        results = sp.playlist_tracks(playlist_id, market="NP")  # Change market if needed
        tracks = results["items"]

        if not tracks:
            print(f"⚠️ No songs found in playlist: {playlist_id}")
            return []

        song_list = []
        print(f"\n🎵 Songs with Audio Features in Playlist ({playlist_id}) 🎵")
        for idx, item in enumerate(tracks):
            track = item["track"]
            song_info = {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "spotify_url": track["external_urls"]["spotify"],
                # Extract album cover URL (largest image if available)
                "album_cover": track["album"]["images"][0]["url"] if track["album"]["images"] else ""
            }

            # Fetch audio features from Last.fm
            audio_features = get_audio_features_lastfm(song_info["artist"], song_info["name"])
            if audio_features:
                song_info.update(audio_features)

            song_list.append(song_info)
            print(f"{idx+1}. {song_info['name']} - {song_info['artist']} | 🔗 {song_info['spotify_url']} | Album Cover: {song_info['album_cover']} | 🎵 Features: {audio_features}")

        return song_list
    except Exception as e:
        print(f"⚠️ Error fetching songs for playlist {playlist_id}: {e}")
        return []

def get_all_playlists():
    """Fetches all playlists from the user's Spotify library."""
    try:
        playlists = sp.current_user_playlists(limit=50)
        playlist_ids = [playlist["id"] for playlist in playlists["items"]]
        print(f"\n📂 Found {len(playlist_ids)} Playlists in Your Library 📂")
        return playlist_ids
    except Exception as e:
        print(f"⚠️ Error fetching playlists: {e}")
        return []

if __name__ == "__main__":
    playlist_ids = get_all_playlists()
    for playlist_id in playlist_ids:
        get_playlist_tracks(playlist_id)
