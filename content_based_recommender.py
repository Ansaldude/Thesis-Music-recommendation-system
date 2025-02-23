import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process, fuzz

# Load the preprocessed data
df = pd.read_csv("preprocessed_music_data.csv")

# Standardize column names
df.columns = df.columns.str.lower().str.strip()

# Create a normalized version of the track name for fuzzy matching
df["normalized_track"] = df["track name"].str.lower().str.strip()

# Convert "tags" column to string
df["tags"] = df["tags"].fillna("").astype(str)

# Vectorize 'tags' using TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
tag_matrix = vectorizer.fit_transform(df["tags"])

# Compute cosine similarity based on tags
cosine_sim = cosine_similarity(tag_matrix, tag_matrix)

def recommend_songs(song_name, top_n=5):
    """
    Recommend songs similar to the given song name based on tags.
    """
    song_norm = song_name.lower().strip()
    if song_norm not in df["normalized_track"].values:
        # Use fuzzy matching if exact match not found
        closest_match = process.extractOne(song_norm, df["normalized_track"], scorer=fuzz.ratio)
        if closest_match and closest_match[1] >= 80:
            print(f"Using fuzzy match: '{closest_match[0]}' with score {closest_match[1]}")
            song_norm = closest_match[0]
        else:
            return f"⚠️ Song '{song_name}' not found in dataset."
    
    song_idx = df[df["normalized_track"] == song_norm].index[0]
    sim_scores = list(enumerate(cosine_sim[song_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+20]
    
    recommendations = df.iloc[[i[0] for i in sim_scores]]
    recommendations = recommendations.drop_duplicates(subset=["track name", "artist"]).head(top_n)
    
    if "album_cover" in recommendations.columns:
        return recommendations[["track name", "artist", "spotify url", "album_cover"]]
    else:
        return recommendations[["track name", "artist", "spotify url"]]

if __name__ == "__main__":
    song_to_search = input("Enter a song name for recommendations: ")
    recs = recommend_songs(song_to_search, top_n=5)
    print("\nRecommended Songs:")
    print(recs)
