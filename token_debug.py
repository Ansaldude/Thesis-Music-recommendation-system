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
    scope="user-read-private playlist-read-private playlist-read-collaborative user-library-read user-read-recently-played",
    cache_path=".cache"
))

try:
    user = sp.current_user()
    print(f"✅ Successfully Authenticated as {user['display_name']}")
    print(f"📌 Country: {user['country']}")
    print(f"🔗 Profile: {user['external_urls']['spotify']}")
except Exception as e:
    print(f"❌ Failed to authenticate: {e}")

try:
    recent_tracks = sp.current_user_recently_played(limit=5)
    print("\n🎵 Recently Played Songs 🎵")
    for item in recent_tracks['items']:
        track = item['track']
        print(f"- {track['name']} by {track['artists'][0]['name']}")
except Exception as e:
    print(f"❌ Error fetching recently played songs: {e}")

try:
    playlists = sp.current_user_playlists(limit=5)
    print("\n📂 Your Playlists 📂")
    for playlist in playlists['items']:
        print(f"- {playlist['name']} (ID: {playlist['id']})")
except Exception as e:
    print(f"❌ Error fetching your playlists: {e}")
