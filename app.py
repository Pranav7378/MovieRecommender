import pickle
import pandas as pd
import requests
import streamlit as st
import os
import json
import io

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Add background image from URL
def add_bg_from_url(url: str):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{url}") no-repeat center center fixed;
            background-size: cover;
        }}
        .block-container {{
            background-color: rgba(0, 0, 0, 0.55);  /* dark overlay so text stays readable */
            padding: 2rem 1rem;
            border-radius: 0.5rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

add_bg_from_url(
    "https://miro.medium.com/v2/resize:fit:1100/format:webp/1*qR08Jxq0IHdvFtBsUhCe3Q.jpeg"
)

st.title("🍿 Movie Recommendation System")

OMDB_KEY = st.secrets["OMDB_KEY"]
PLACEHOLDER_IMAGE = "https://via.placeholder.com/300x450?text=No+Image"
POSTER_CACHE_DIR = "poster_cache"
os.makedirs(POSTER_CACHE_DIR, exist_ok=True)

# Load movies dict locally
movies = pd.DataFrame(pickle.load(open("movie_dict.pkl", "rb")))

# Load similarity from Hugging Face dataset URL
HUGGINGFACE_SIMILARITY_URL = "https://huggingface.co/datasets/PranavAI/similarity/resolve/main/similarity.pkl"
LOCAL_SIMILARITY_FILE = "similarity.pkl"

@st.cache_data(ttl=86400)
def load_similarity():
    # Try loading locally first
    if os.path.exists(LOCAL_SIMILARITY_FILE):
        with open(LOCAL_SIMILARITY_FILE, "rb") as f:
            similarity = pickle.load(f)
        return similarity

    # Fallback to URL if local file doesn't exist
    response = requests.get(HUGGINGFACE_SIMILARITY_URL)
    response.raise_for_status()
    file_bytes = io.BytesIO(response.content)
    similarity = pickle.load(file_bytes)

    # Optionally save locally for future runs
    #with open(LOCAL_SIMILARITY_FILE, "wb") as f:
       # pickle.dump(similarity, f)

    return similarity


similarity = load_similarity()

@st.cache_data(ttl=86400)  # cache in memory 1 day
def fetch_metadata(title):
    safe_title = title.replace(" ", "_")
    cache_path = os.path.join(POSTER_CACHE_DIR, f"{safe_title}.json")

    # Check local file cache
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Otherwise, call OMDb API
    try:
        res = requests.get("https://www.omdbapi.com/", params={
            "apikey": OMDB_KEY, "t": title, "r": "json"
        }, timeout=10)
        res.raise_for_status()
        data = res.json()

        poster = data.get("Poster", PLACEHOLDER_IMAGE)
        year = data.get("Year", "Unknown")
        rating = data.get("imdbRating", "N/A")
        genre = data.get("Genre", "")
        plot = data.get("Plot", "No plot available.")

        result = {
            "poster": poster if poster != "N/A" else PLACEHOLDER_IMAGE,
            "year": year,
            "rating": rating,
            "genre": genre,
            "plot": plot
        }

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(result, f)

        return result
    except:
        return {
            "poster": PLACEHOLDER_IMAGE,
            "year": "N/A",
            "rating": "N/A",
            "genre": "",
            "plot": "⚠️ OMDb unreachable"
        }

def recommend(title):
    idx = movies[movies["title"] == title].index[0]
    distances = similarity[idx]
    top5 = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:6]

    recommendations = []
    for i, _ in top5:
        movie_title = movies.iloc[i].title
        meta = fetch_metadata(movie_title)
        recommendations.append((movie_title, meta))
    return recommendations


selected_movie = st.selectbox("🎞️ Choose a movie:", movies["title"].values)

if st.button("🔍 Recommend"):
    with st.spinner("Fetching posters and metadata..."):
        recs = recommend(selected_movie)

    cols = st.columns(5)
    for col, (title, meta) in zip(cols, recs):
        with col:
            st.image(meta["poster"], caption=title, use_container_width=True)
            st.caption(f"📅 {meta['year']} | ⭐ {meta['rating']}")
            st.markdown(f"**{meta['genre']}**")
            st.markdown(f"*{meta['plot']}*")
