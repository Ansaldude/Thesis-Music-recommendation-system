import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from hybrid_recommender import hybrid_recommend

st.set_page_config(page_title="Music Recommendation System", layout="wide")
st.title("Music Recommendation System")

# Create two tabs: Recommendations and Visualizations
tabs = st.tabs(["Recommendations", "Visualizations"])

with tabs[0]:
    st.header("Get Song Recommendations")
    song_name = st.text_input("Enter a Song Name", value="goosebumps")
    if st.button("Recommend"):
        recs = hybrid_recommend(song_name, top_n=5)
        if isinstance(recs, str):
            st.error(recs)
        else:
            st.subheader("Recommended Songs:")
            for idx, row in recs.iterrows():
                st.markdown(f"### {row['track name']}")
                st.markdown(f"*by {row['artist']}*")
                if "album_cover" in row and pd.notnull(row["album_cover"]) and row["album_cover"] != "":
                    st.image(row["album_cover"], width=150)
                st.markdown(f"[Listen on Spotify]({row['spotify url']})", unsafe_allow_html=True)
                st.markdown("---")

with tabs[1]:
    st.header("Tableau Visualizations")
    st.write("Below is the embedded Tableau dashboard showing data insights.")
    
    # Paste the full embed code from Tableau Public as a multiline string.
    tableau_html = """
    <div class='tableauPlaceholder' id='viz1740289859113' style='position: relative'>
      <noscript>
        <a href='#'>
          <img alt='Music Data Insight ' src='https://public.tableau.com/static/images/Mu/Music_17402894184240/MusicDataInsight/1_rss.png' style='border: none' />
        </a>
      </noscript>
      <object class='tableauViz' style='display:none;'>
        <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
        <param name='embed_code_version' value='3' />
        <param name='site_root' value='' />
        <param name='name' value='Music_17402894184240/MusicDataInsight' />
        <param name='tabs' value='no' />
        <param name='toolbar' value='yes' />
        <param name='static_image' value='https://public.tableau.com/static/images/Mu/Music_17402894184240/MusicDataInsight/1.png' />
        <param name='animate_transition' value='yes' />
        <param name='display_static_image' value='yes' />
        <param name='display_spinner' value='yes' />
        <param name='display_overlay' value='yes' />
        <param name='display_count' value='yes' />
        <param name='language' value='en-US' />
      </object>
    </div>
    <script type='text/javascript'>
      var divElement = document.getElementById('viz1740289859113');
      var vizElement = divElement.getElementsByTagName('object')[0];
      if (divElement.offsetWidth > 800) { 
        vizElement.style.width='1000px';
        vizElement.style.height='827px';
      } else if (divElement.offsetWidth > 500) { 
        vizElement.style.width='1000px';
        vizElement.style.height='827px';
      } else { 
        vizElement.style.width='100%';
        vizElement.style.height='1277px';
      }
      var scriptElement = document.createElement('script');
      scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
      vizElement.parentNode.insertBefore(scriptElement, vizElement);
    </script>
    """

    # Embed the HTML in Streamlit using an iframe component
    components.html(tableau_html, width=1000, height=850, scrolling=True)
