
import pickle
import streamlit as st
import pandas as pd
import requests
import time
session = requests.Session()

def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=cd84f53f44eb8ee1ac3e240ff0e95d2e",
            timeout=20
        )
        data = response.json()
        if data.get("poster_path"):
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    except Exception as e:
        print(f"Error for {movie_id}: {e}")

    # Fallback image
    return "data:image/jpeg;base64,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"

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        movie_name = movies.iloc[i[0]].title
        print("Movie:", movie_name)
        print("Movie ID:", movie_id)
        recommended_movies.append(movie_name)
        # fetch posters from Api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters



movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')
selected_movie_name=st.selectbox(
    'select movie',movies['title'].values)
if st.button('Recommended'):
    name, posters=recommend(selected_movie_name)

    col1, col2, col3, col4, col5=st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])
    with col3:
        st.text(name[2])
        st.image(posters[2])
    with col4:
       st.text(name[3])
       st.image(posters[3])
    with col5:
        st.text(name[4])
        st.image(posters[4])
