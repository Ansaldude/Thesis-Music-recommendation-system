import csv
import os
from dotenv import load_dotenv
from fetch_audio_features import get_all_playlists, get_playlist_tracks

load_dotenv()
csv_filename = "music_data.csv"

def save_to_csv(data):
    """Saves song data into a CSV file."""
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Updated headers including Album Cover
        writer.writerow(["Track Name", "Artist", "Spotify URL", "Listeners", "Play Count", "Album", "Tags", "Album Cover"])
        for song in data:
            writer.writerow([
                song["name"],
                song["artist"],
                song["spotify_url"],
                song.get("listeners", "N/A"),
                song.get("playcount", "N/A"),
                song.get("album", "Unknown Album"),
                ", ".join(song.get("tags", [])),
                song.get("album_cover", "")
            ])
    print(f"\n✅ Data saved to {csv_filename} successfully!")

if __name__ == "__main__":
    playlist_ids = get_all_playlists()
    all_songs = []
    for playlist_id in playlist_ids:
        songs = get_playlist_tracks(playlist_id)
        all_songs.extend(songs)
    save_to_csv(all_songs)
