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
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-read-private user-library-read playlist-read-private playlist-read-collaborative user-read-recently-played",
    cache_path=".cache"
)

sp = spotipy.Spotify(auth_manager=auth_manager)

try:
    token_info = auth_manager.get_access_token(as_dict=True)
    print("\n✅ Token Info Retrieved Successfully:")
    print(token_info)
    print("\n🔹 Token Scopes (Permissions):")
    print(token_info["scope"])
except Exception as e:
    print(f"\n❌ Failed to check token scopes: {e}")


