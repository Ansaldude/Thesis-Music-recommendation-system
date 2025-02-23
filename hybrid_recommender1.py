import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the preprocessed data
df = pd.read_csv("preprocessed_music_data.csv")

# Ensure column names are standardized (all lowercase)
df.columns = df.columns.str.lower().str.strip()

# Convert "tags" to string (if not already)
df["tags"] = df["tags"].fillna("").astype(str)

# --- Content-Based Similarity ---
# Use TF-IDF vectorization on the 'tags' column
vectorizer = TfidfVectorizer(stop_words="english")
tag_matrix = vectorizer.fit_transform(df["tags"])

# Compute cosine similarity between songs based on tags
content_sim = cosine_similarity(tag_matrix, tag_matrix)

# --- Popularity Component ---
# Assume 'playcount' is already normalized (from preprocess_data.py)
# We can create a simple popularity similarity by taking the outer product
popularity = df["playcount"].values  # values between 0 and 1
popularity_sim = np.outer(popularity, popularity)

# --- Hybrid Similarity ---
# Weight for content similarity (alpha) and popularity (1 - alpha)
alpha = 0.7
hybrid_sim = alpha * content_sim + (1 - alpha) * popularity_sim

def hybrid_recommend(song_name, top_n=5):
    """
    Recommend songs similar to the given song name using a hybrid
    of content-based similarity and popularity.
    """
    if song_name not in df["track name"].values:
        return f"⚠️ Song '{song_name}' not found in dataset."
    
    # Get the index of the song in the DataFrame
    idx = df[df["track name"] == song_name].index[0]
    # Compute similarity scores for that song against all songs
    sim_scores = list(enumerate(hybrid_sim[idx]))
    # Sort scores in descending order and ignore the first (itself)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    
    # Get the recommended song details
    recommendations = df.iloc[[i[0] for i in sim_scores]][["track name", "artist", "spotify url"]]
    # Drop duplicates if any
    recommendations = recommendations.drop_duplicates(subset=["track name", "artist"]).head(top_n)
    return recommendations

if __name__ == "__main__":
    song = input("Enter a song name for hybrid recommendations: ")
    recs = hybrid_recommend(song, top_n=5)
    print("\nHybrid Recommendations:")
    print(recs)
