import streamlit as st
import pandas as pd
import random
import time
from utils.css_loader import load_css
from datetime import datetime, timedelta
from movie_detail import show_movie_details

def home_page():
    """
    Displays the home page content with top-rated movies and upcoming movies refreshing every 15 seconds.
    """
    load_css("style.css")  # Load specific CSS for this page
    # --- Lire les paramètres d'URL ---
    query_params = st.query_params
    movie_param = query_params.get("movie")

    # Vérifie si un film est sélectionné dans l'URL
    if movie_param:
        show_movie_details(movie_param)
        return
 

    # Charger les films
    films = pd.read_csv('datasets/raw/films.csv')

    # Vérifier la présence des colonnes nécessaires
    required_columns = ['vote_average', 'poster_path', 'original_title', 'release_date', 'genres']
    missing_columns = [col for col in required_columns if col not in films.columns]
    
    if missing_columns:
        st.error(f"Erreur : Les colonnes suivantes sont absentes du dataset : {missing_columns}")
        return

    BASE_URL = "https://image.tmdb.org/t/p/w500"

    # Convertir release_date en datetime
    films['release_date'] = pd.to_datetime(films['release_date'], errors='coerce')




    # Filtrer les films du genre drame avec une note supérieure à 8
    drama_movies = films[(films['vote_average'] > 8) & (films['poster_path'].notna()) & (films['poster_path'] != "") & (films['genres'].str.contains("Drama", case=False, na=False))]


    # Sélection aléatoire de 5 films parmi ceux filtrés
    selected_drama_movies = drama_movies.sample(n=min(len(drama_movies), 5)).copy()
    selected_drama_movies['poster_path'] = BASE_URL + selected_drama_movies['poster_path'].astype(str)
    drama = selected_drama_movies.to_dict(orient='records')

    # Affichage des films en colonnes
    st.markdown("<h2 style='color: #fff;'>Top Drames</h2>", unsafe_allow_html=True)
    cols = st.columns(min(len(drama), 5))

    for i, movie in enumerate(drama):
        with cols[i]:
            st.image(movie["poster_path"], use_container_width=True)
            st.markdown(
                 f"""<p style='color: #fff; font-weight: bold; margin-bottom: 2px;'>{movie["original_title"]}</p>
                <p style='color: #999; font-size: 12px;'>⭐ {round(movie["vote_average"], 1)} | {movie["release_date"].year} | {movie["genres"]}</p>
                """,
                unsafe_allow_html=True
            )



    # Filtrer les films du genre Comedy avec une note supérieure à 8
    comedy_movies = films[(films['vote_average'] > 8) & (films['poster_path'].notna()) & (films['poster_path'] != "") & (films['genres'].str.contains("Comedy", case=False, na=False))]


    # Sélection aléatoire de 5 films parmi ceux filtrés
    selected_comedy_movies = comedy_movies.sample(n=min(len(comedy_movies), 5)).copy()
    selected_comedy_movies['poster_path'] = BASE_URL + selected_comedy_movies['poster_path'].astype(str)
    comedy = selected_comedy_movies.to_dict(orient='records')

    # Affichage des films en colonnes
    st.markdown("<h2 style='color: #fff;'>Top Comedy</h2>", unsafe_allow_html=True)
    cols = st.columns(min(len(comedy), 5))

    for i, movie in enumerate(comedy):
        with cols[i]:
            st.image(movie["poster_path"], use_container_width=True)
            st.markdown(
                 f"""<p style='color: #fff; font-weight: bold; margin-bottom: 2px;'>{movie["original_title"]}</p>
                <p style='color: #999; font-size: 12px;'>⭐ {round(movie["vote_average"], 1)} | {movie["release_date"].year} | {movie["genres"]}</p>
                """,
                unsafe_allow_html=True
            )


# Filtrer les films du genre Romance avec une note supérieure à 8
    romance_movies = films[(films['vote_average'] > 8) & (films['poster_path'].notna()) & (films['poster_path'] != "") & (films['genres'].str.contains("Romance", case=False, na=False))]


    # Sélection aléatoire de 5 films parmi ceux filtrés
    selected_romance_movies = romance_movies.sample(n=min(len(romance_movies), 5)).copy()
    selected_romance_movies['poster_path'] = BASE_URL + selected_romance_movies['poster_path'].astype(str)
    romance = selected_romance_movies.to_dict(orient='records')

    # Affichage des films en colonnes
    st.markdown("<h2 style='color: #fff;'>Top Romance</h2>", unsafe_allow_html=True)
    cols = st.columns(min(len(romance), 5))

    for i, movie in enumerate(romance):
        with cols[i]:
            st.image(movie["poster_path"], use_container_width=True)
            st.markdown(
                 f"""<p style='color: #fff; font-weight: bold; margin-bottom: 2px;'>{movie["original_title"]}</p>
                <p style='color: #999; font-size: 12px;'>⭐ {round(movie["vote_average"], 1)} | {movie["release_date"].year} | {movie["genres"]}</p>
                """,
                unsafe_allow_html=True
            )




    # Filtrer les films avec une note supérieure à 9 et avec une image disponible
    top_movies = films[(films['vote_average'] > 9) & (films['poster_path'].notna()) & (films['poster_path'] != "")]


       # Sélection aléatoire de 5 films parmi ceux filtrés
    selected_movies = top_movies.sample(n=min(len(top_movies), 5)).copy()
    selected_movies['poster_path'] = BASE_URL + selected_movies['poster_path'].astype(str)
    movies = selected_movies.to_dict(orient='records')

    # Affichage des films en colonnes
    st.markdown("<h2 style='color: #fff;'>Notre sélection pour vous</h2>", unsafe_allow_html=True)
    cols = st.columns(min(len(movies), 5))

    for i, movie in enumerate(movies):
        with cols[i]:
            with st.container():
                st.image(movie["poster_path"], use_container_width=True)
                st.markdown(
                     f"""<a href="?movie={movie['original_title']}" style="text-decoration: none;"> </a>
                     <p style='color: #fff; font-weight: bold; margin-bottom: 2px;'>{movie["original_title"]}</p>
                     <p style='color: #999; font-size: 12px;'>⭐ {round(movie["vote_average"], 1)} | {movie["release_date"].year} | {movie["genres"]}</p>
                    """,
                    unsafe_allow_html=True
                )
                







    # ------ AJOUT : Films à venir ------
    st.markdown("<h2 style='color: #fff;'>À venir prochainement</h2>", unsafe_allow_html=True)

    # Définir la plage des 30 prochains jours et filtrer les films parmi ceux qui ont une date de sortie dans cette plage et qui ont une image disponible
    today = datetime.today()
    upcoming_movies = films[(films['release_date'] > today) & (films['release_date'] <= today + timedelta(days=30)) & (films['poster_path'].notna()) & (films['poster_path'] != "")]


    if upcoming_movies.empty:
        st.warning("Aucun film prévu dans les 30 prochains jours.")
    else:
        selected_upcoming = upcoming_movies.sample(n=min(len(upcoming_movies), 5)).copy()
        selected_upcoming['poster_path'] = BASE_URL + selected_upcoming['poster_path'].astype(str)
        upcoming_list = selected_upcoming.to_dict(orient='records')

        cols_upcoming = st.columns(min(len(upcoming_list), 5))

        for i, movie in enumerate(upcoming_list):
            with cols_upcoming[i]:
                st.image(movie["poster_path"], use_container_width=True)
                st.markdown(
                    f"""
                    <p style='color: #fff; font-weight: bold; margin-bottom: 2px;'>{movie["original_title"]}</p>
                    <p style='color: #999; font-size: 12px;'>📅 Sortie le {movie["release_date"].strftime('%d %b %Y')} | {movie["genres"]}</p>
                    """,
                    unsafe_allow_html=True
                )

                
    # Rafraîchir automatiquement toutes les 15 secondes
    time.sleep(15)
    st.rerun()

