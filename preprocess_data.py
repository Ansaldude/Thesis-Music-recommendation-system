import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the dataset
df = pd.read_csv("music_data.csv")

# Convert column names to lowercase and remove extra spaces
df.columns = df.columns.str.lower().str.strip()

print("📌 Updated Column Names:", df.columns.tolist())

# Rename columns to remove spaces (e.g., "play count" -> "playcount")
if 'play count' in df.columns:
    df.rename(columns={'play count': 'playcount'}, inplace=True)
if 'listeners' in df.columns:
    df.rename(columns={'listeners': 'listeners'}, inplace=True)

# Convert numeric columns properly
df["listeners"] = pd.to_numeric(df["listeners"], errors="coerce").fillna(0)
df["playcount"] = pd.to_numeric(df["playcount"], errors="coerce").fillna(0)

# Normalize numerical features
scaler = MinMaxScaler()
df[['listeners', 'playcount']] = scaler.fit_transform(df[['listeners', 'playcount']])

# Save preprocessed data
df.to_csv("preprocessed_music_data.csv", index=False)

print("✅ Data preprocessing completed. File saved as 'preprocessed_music_data.csv'.")
