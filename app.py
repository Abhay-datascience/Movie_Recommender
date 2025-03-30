import streamlit as st
import pickle
import requests

# Load movie data
movies_df = pickle.load(open('movie.pkl', 'rb'))  # Keep it as a DataFrame
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDb API key (replace with your own if required)
API_KEY = "75edfde6c5b56e51029755927fd4e7a4"


def fetch_poster(movie_title):
    """Fetch movie poster URL from TMDb API."""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    response = requests.get(url)
    data = response.json()

    if data['results']:  # Check if any result exists
        poster_path = data['results'][0]['poster_path']
        full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"  # w500 gives medium-quality image
        return full_poster_url
    else:
        return "https://via.placeholder.com/200x300?text=No+Image"  # Placeholder if no poster is found


def recommend(movie):
    """Return recommended movie names and their poster URLs."""
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_title = movies_df.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))  # Fetch poster for each movie

    return recommended_movies, recommended_posters


st.title('Movie Recommender System')

# Use DataFrame for movie selection
movies_list = movies_df['title'].values

selected_movie_name = st.selectbox("Select a movie:", movies_list)

if st.button("Recommend"):
    recommendations, posters = recommend(selected_movie_name)

    # Display movies and posters in a grid layout
    cols = st.columns(5)  # Create 5 columns for 5 movies
    for idx, col in enumerate(cols):
        with col:
            st.text(recommendations[idx])  # Movie Title
            st.image(posters[idx])  # Movie Poster
