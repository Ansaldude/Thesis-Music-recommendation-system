import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from hybrid_recommender import hybrid_recommend

# Configure the Streamlit page
st.set_page_config(page_title="Music Recommendation System", layout="wide")
st.title("Music Recommendation System")

# Create two tabs: one for recommendations, one for visualizations
tabs = st.tabs(["Recommendations", "Visualizations"])

with tabs[0]:
    st.header("Get Song Recommendations")
    # Input field for the song name
    song_name = st.text_input("Enter a Song Name", value="goosebumps")
    if st.button("Recommend"):
        recs = hybrid_recommend(song_name, top_n=5)
        if isinstance(recs, str):
            st.error(recs)
        else:
            st.subheader("Recommended Songs:")
            # Display each recommended song with album cover and clickable link
            for idx, row in recs.iterrows():
                st.markdown(f"### {row['track name']}")
                st.markdown(f"*by {row['artist']}*")
                # Display album cover if available
                if "album_cover" in row and pd.notnull(row["album_cover"]) and row["album_cover"] != "":
                    st.image(row["album_cover"], width=150)
                # Display clickable Spotify link
                st.markdown(f"[Listen on Spotify]({row['spotify url']})", unsafe_allow_html=True)
                st.markdown("---")

with tabs[1]:
    st.header("Tableau Visualizations")
    st.write("Below is the embedded Tableau dashboard showing data insights.")
    # Replace the URL below with your actual Tableau Public dashboard URL
    tableau_url = "https://public.tableau.com/views/Music_17402894184240/MusicDataInsight?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
    components.iframe(tableau_url, width=1000, height=800, scrolling=True)
