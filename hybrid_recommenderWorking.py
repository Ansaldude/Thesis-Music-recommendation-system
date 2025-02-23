import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load preprocessed data
df = pd.read_csv("preprocessed_music_data.csv")

# Ensure column names are standardized (all lowercase)
df.columns = df.columns.str.lower().str.strip()

# Create a normalized version of the track name for fuzzy matching
df["normalized_track"] = df["track name"].str.lower().str.strip()

# Convert "tags" to string (if not already)
df["tags"] = df["tags"].fillna("").astype(str)

# Vectorize the "tags" column using TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
tag_matrix = vectorizer.fit_transform(df["tags"])

# Compute cosine similarity between songs based on tags
content_sim = cosine_similarity(tag_matrix, tag_matrix)

# Assume 'playcount' is normalized from preprocessing
popularity = df["playcount"].values
popularity_sim = popularity[:, None] * popularity[None, :]

# Hybrid similarity: weighted combination of content similarity and popularity similarity
alpha = 0.7
hybrid_sim = alpha * content_sim + (1 - alpha) * popularity_sim

def hybrid_recommend(song_name, top_n=5):
    """
    Recommend songs similar to the given song name using a hybrid of content-based
    similarity (tags) and popularity (playcount).
    """
    song_norm = song_name.lower().strip()
    if song_norm not in df["normalized_track"].values:
        return f"⚠️ Song '{song_name}' not found in dataset."
    
    # Get the index of the song
    idx = df[df["normalized_track"] == song_norm].index[0]
    sim_scores = list(enumerate(hybrid_sim[idx]))
    # Increase candidate pool to account for duplicates
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+20]
    
    recommendations = df.iloc[[i[0] for i in sim_scores]]
    # Drop duplicates based on track name and artist
    recommendations = recommendations.drop_duplicates(subset=["track name", "artist"]).head(top_n)
    
    # If album_cover column exists, include it; otherwise, only return available columns.
    if "album_cover" in recommendations.columns:
        return recommendations[["track name", "artist", "spotify url", "album_cover"]]
    else:
        return recommendations[["track name", "artist", "spotify url"]]

if __name__ == "__main__":
    song = input("Enter a song name for hybrid recommendations: ")
    recs = hybrid_recommend(song, top_n=5)
    print("\nHybrid Recommendations:")
    print(recs)
