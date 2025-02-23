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
    scope="user-read-private user-library-read playlist-read-private playlist-read-collaborative",
    cache_path=".cache"
))

# Test fetching audio features
test_track_id = "2takcwOaAZWiXQijPHIx7B"  # City and Colour - The Girl

try:
    analysis = sp.audio_analysis(test_track_id)
    print(f"\n✅ Audio Analysis for {test_track_id}: {analysis}")
except Exception as e:
    print(f"\n❌ Error fetching audio analysis: {e}")
