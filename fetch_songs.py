import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load API credentials
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:5000/callback"

# Authenticate with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-read-private playlist-read-private playlist-read-collaborative user-library-read",
    cache_path=".cache"
))

def get_all_playlists():
    """Fetches all playlists from the user's library."""
    try:
        playlists = sp.current_user_playlists(limit=50)  # Fetch up to 50 playlists
        playlist_ids = [playlist["id"] for playlist in playlists["items"]]
        print(f"\n📂 Found {len(playlist_ids)} Playlists in Your Library 📂")
        return playlist_ids
    except Exception as e:
        print(f"⚠️ Error fetching playlists: {e}")
        return []

def get_playlist_tracks(playlist_id):
    """Fetches all tracks from a given Spotify playlist."""
    try:
        results = sp.playlist_tracks(playlist_id, market="NP")  # Change market if needed
        tracks = results["items"]

        if not tracks:
            print(f"⚠️ No songs found in playlist: {playlist_id}")
            return []

        song_list = []
        print(f"\n🎵 Songs in Playlist ({playlist_id}) 🎵")
        for idx, item in enumerate(tracks):
            track = item["track"]
            song_info = {
                "id": track["id"],
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "popularity": track["popularity"],
                "spotify_url": track["external_urls"]["spotify"],
                "album_cover": track["album"]["images"][0]["url"] if track["album"]["images"] else ""
            }
            song_list.append(song_info)
            print(f"{idx+1}. {song_info['name']} - {song_info['artist']} ({song_info['album']})")
            print(f"   Album Cover: {song_info['album_cover']}")
        return song_list
    except Exception as e:
        print(f"⚠️ Error fetching songs for playlist {playlist_id}: {e}")
        return []

if __name__ == "__main__":
    playlist_ids = get_all_playlists()  # Get ALL playlists dynamically

    for playlist_id in playlist_ids:
        get_playlist_tracks(playlist_id)
