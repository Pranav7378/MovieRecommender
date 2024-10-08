import streamlit as st
import pickle
import pandas as pd
import requests

import requests
from requests.exceptions import ConnectTimeout, RequestException

import requests
from requests.exceptions import ConnectTimeout, RequestException

# Path to a placeholder image
PLACEHOLDER_IMAGE = "path/to/placeholder_image.png"  # Change this to the correct path of your placeholder image


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=4a96b8b2760c2a74fa4d5ae37a8c81a2&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Correctly fetching movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))  # Passing movie_id directly
    return recommended_movies, recommended_movie_posters

# Load the movie dictionary from a pickle file
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit title
st.title('Movie Recommendation System')

# Create a dropdown (selectbox) to select a movie title
selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values  # Use .values to get the list of movie titles
)

if st.button("Recommend"):
   names, posters = recommend(selected_movie_name)
   col1, col2, col3, col4, col5 = st.columns(5)

   with col1:
       st.text(names[0])
       st.image(posters[0])

   with col2:
       st.text(names[1])
       st.image(posters[1])

   with col3:
       st.text(names[2])
       st.image(posters[2])

   with col4:
       st.text(names[3])
       st.image(posters[3])

   with col5:
       st.text(names[4])
       st.image(posters[4])
