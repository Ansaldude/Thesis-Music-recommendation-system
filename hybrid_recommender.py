import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process, fuzz
import numpy as np

# Load preprocessed data
df = pd.read_csv("preprocessed_music_data.csv")

# Standardize column names (all lowercase, stripped)
df.columns = df.columns.str.lower().str.strip()
# Rename "album cover" column to "album_cover" if needed
if "album cover" in df.columns:
    df.rename(columns={"album cover": "album_cover"}, inplace=True)

# Create a normalized track name for matching
df["normalized_track"] = df["track name"].str.lower().str.strip()

# Ensure "tags" is a string
df["tags"] = df["tags"].fillna("").astype(str)

# Vectorize 'tags' using TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
tag_matrix = vectorizer.fit_transform(df["tags"])

# Compute cosine similarity for content-based similarity
content_sim = cosine_similarity(tag_matrix, tag_matrix)

# Assume playcount is normalized from preprocessing
popularity = df["playcount"].values
popularity_sim = popularity[:, None] * popularity[None, :]

# Hybrid similarity: weighted combination of content and popularity
alpha = 0.7
hybrid_sim = alpha * content_sim + (1 - alpha) * popularity_sim

def hybrid_recommend(song_name, top_n=5, threshold=80):
    """
    Recommend songs similar to the given song name using a hybrid approach.
    If an exact match isn't found, fuzzy matching is used.
    """
    song_norm = song_name.lower().strip()
    
    if song_norm not in df["normalized_track"].values:
        closest_match = process.extractOne(song_norm, df["normalized_track"], scorer=fuzz.ratio)
        if closest_match and closest_match[1] >= threshold:
            print(f"Using fuzzy match: '{closest_match[0]}' with score {closest_match[1]}")
            song_norm = closest_match[0]
        else:
            return f"⚠️ Song '{song_name}' not found in dataset."
    
    idx = df[df["normalized_track"] == song_norm].index[0]
    sim_scores = list(enumerate(hybrid_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+20]
    
    recommendations = df.iloc[[i[0] for i in sim_scores]]
    recommendations = recommendations.drop_duplicates(subset=["track name", "artist"]).head(top_n)
    
    # Check if album_cover exists and return it if available
    if "album_cover" in recommendations.columns:
        return recommendations[["track name", "artist", "spotify url", "album_cover"]]
    else:
        return recommendations[["track name", "artist", "spotify url"]]

if __name__ == "__main__":
    song = input("Enter a song name for hybrid recommendations: ")
    recs = hybrid_recommend(song, top_n=5)
    print("\nHybrid Recommendations:")
    print(recs)
