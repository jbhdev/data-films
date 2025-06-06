import streamlit as st
import pandas as pd 
import ast
import time
from utils.css_loader import load_css
import string
from recommendation import (
    get_recommendations_by_title,
    recommend_by_actors,
    films,
    get_film_index_by_title,
    get_films_by_actor
)

def movie_detail_page():

    load_css("movie_style.css")
    st.markdown("<h1 style='color: #fff;'>Recherche</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


    # Barre de recherche
    search_query = st.text_input("Rechercher un film par titre", value="",placeholder="Quel est le titre de votre film?", label_visibility="collapsed")

    filtered_movies = films[["original_title", "poster_url"]].dropna(subset=["original_title"])

    if search_query.strip() == "":
        # Aucune recherche : affichage aléatoire de 20 films
        sampled_movies = filtered_movies.sample(n=min(20, len(filtered_movies)), random_state=None)
    else:
        # Filtrer par recherche (contient, insensible à la casse)
        mask = filtered_movies["original_title"].str.contains(search_query, case=False, na=False)
        sampled_movies = filtered_movies[mask].sort_values("original_title")

    # Affichage 5 colonnes
    cols = st.columns(5)
    for i, (_, row) in enumerate(sampled_movies.iterrows()):
        with cols[i % 5]:
            st.markdown(
                f"""
                <div style='display: flex; flex-direction: column; align-items: center; height: 340px; margin-bottom: 10px;'>
                    <a href="?movie={row['original_title']}" target="_self" style="text-decoration: none; width: 100%;">
                        <img src="{row.get('poster_url', 'https://placehold.co/300x450?text=No+Image')}"
                            style="width: 100%; height: 270px; object-fit: cover; border-radius: 10px;">
                        <div style='height: 50px; color: white; font-weight: bold; text-align: center; 
                                    display: flex; align-items: center; justify-content: center; padding: 0 5px; overflow: hidden;'>
                            {row['original_title']}
                        </div>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Auto-refresh toutes les 20 secondes
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = time.time()
    if time.time() - st.session_state.last_refresh > 20:
        st.session_state.last_refresh = time.time()
        st.rerun()

def show_movie_details(title):
            # Bouton retour aux films
    if st.button("⬅ Retour aux films"):
        # Nettoyer query params et retourner à la liste
        st.session_state.current_page = 'movie'
        st.query_params.clear()
        st.rerun()

    load_css("movie_style.css")

    movie_data = films[films["original_title"] == title]
    if movie_data.empty:
        st.error("Film introuvable.")
        return

    movie = movie_data.iloc[0]
    trailer_url = movie.get("trailer_url")

    st.markdown(f"<h1 style='text-align: center; color: #fff;'>{title} ({movie.get('startYear', 'Année inconnue')})</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if "show_trailer" not in st.session_state:
        st.session_state.show_trailer = False

    # Structure principale : affiche + détails côte à côte
    cols = st.columns([1, 2])

    with cols[0]:
        st.image(movie.get('poster_url', 'https://placehold.co/300x450?text=No+Image'), width=450)

    with cols[1]:
        # Convertir genres (liste) en chaîne
        genres = movie.get('genres', 'Genre inconnu')
        try:
            # Tenter de transformer la string en liste Python
            genres_list = ast.literal_eval(genres) if isinstance(genres, str) else genres
            if isinstance(genres_list, list):
                genres = ", ".join(genres_list)
            else:
                genres = str(genres)
        except:
            genres = str(genres)

        # Calcul note, couleur et emoji
        vote_average = movie.get("vote_average", 0)
        if vote_average >= 7:
            note_color = "limegreen"
        elif vote_average >= 5:
            note_color = "orange"
        else:
            note_color = "crimson"

        # Convertir la note en étoiles
        filled_stars = int(round(vote_average / 2))  # Convertir sur 5 étoiles
        stars = "⭐" * filled_stars + "☆" * (5 - filled_stars)

        # Affichage final
        st.markdown(f"""
            <div style="color: white; font-size: 20px;">
                <p style="margin-bottom: 0;">
                    {movie.get('release_date', 'Date de sortie inconnue')} | {genres} | {movie.get('runtimeMinutes', 'Durée inconnue')} min
                </p>
                <p></p>
                <p style="color:white; font-size: 18px;font-weight: bold; margin-bottom: 8px;">Synopsis :</p>
                <p style="color:white; margin-top: 0;text-align: justify;">{movie.get('overview', 'Pas de description disponible.')}</p>
                <p style="font-size: 18px; font-weight: bold; margin-bottom: 5px;">Notes :</p>
                <p style="color:{note_color}; font-size: 24px; font-weight: bold; margin: 0;">
                {vote_average:.2f} / 10 
                </p>
                <p style="font-size: 28px; color: {note_color}; margin: 5px 0 0 0;">
                    {stars}</p>
            </div>
        """, unsafe_allow_html=True)

        # Boutons côte à côte
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎬 Bande Annonce"):
                st.session_state.show_trailer = not st.session_state.show_trailer
        with col2:
            st.button("➕ Ajouter à ma liste")


    # Bande annonce sous les boutons si activé
    if st.session_state.show_trailer and trailer_url:
        youtube_id = None

        if isinstance(trailer_url, str) and"watch?v=" in trailer_url:
            youtube_id = trailer_url.split("watch?v=")[-1]
        elif isinstance(trailer_url, str) and "youtu.be/" in trailer_url:
            youtube_id = trailer_url.split("youtu.be/")[-1]

        if youtube_id:
            st.markdown(
                f"""
                <div style="position: relative; padding-bottom: 56.25%; height: 0; margin-top: 20px;">
                    <iframe src="https://www.youtube.com/embed/{youtube_id}" 
                            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
                            frameborder="0" allowfullscreen>
                    </iframe>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Pas de trailer ou URL non reconnue, on affiche un message à la place
            st.markdown("### Bande annonce indisponible 😞", unsafe_allow_html=True)

    # Acteurs principaux
    st.markdown("<h2 style='color: #fff; margin-top: 30px;'>Acteurs principaux</h2>", unsafe_allow_html=True)
    base_url = "https://image.tmdb.org/t/p/w500"

    # Fonction réutilisable pour sécuriser une URL d'image
    def get_clean_url(poster, base_url, placeholder_url="https://placehold.co/150x225?text=No+Image"):
        if not isinstance(poster, str) or pd.isna(poster) or poster.strip() == '':
            return placeholder_url
        poster = poster.strip()
        if not poster.startswith("http"):
            return base_url + poster
        return poster

    # Liste des acteurs
    acteurs = [
        {"nom": movie.get("acteurs_1", ""), "poster": movie.get("actors_1_posters", "")},
        {"nom": movie.get("acteurs_2", ""), "poster": movie.get("actors_2_posters", "")},
        {"nom": movie.get("actrices", ""), "poster": movie.get("actress_1_posters", "")},
    ]

    # Affichage dans des colonnes
    acteur_cols = st.columns(len(acteurs))
    for i, acteur in enumerate(acteurs):
        poster_url = get_clean_url(acteur['poster'], base_url)

        with acteur_cols[i]:
            st.markdown(
                f"""
                <div style='text-align: center;'>
                    <a href="?actor={acteur['nom']}" target="_self" style="text-decoration: none; color: inherit;">
                        <img src="{poster_url}" 
                            style="
                                width: 300px;
                                height: 300px;
                                object-fit: cover;
                                border-radius: 10%;
                                border: 1px solid white;
                                box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                            ">
                        <p style='color: white; font-weight: bold; margin-top: 8px;font-size: 18px;'>{acteur['nom']}</p>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

    ### --------- Bloc réalisateur -----------------------------
    st.markdown("<h2 style='color: #fff; margin-top: 40px;'>Réalisateur</h2>", unsafe_allow_html=True)
    
    # Récupération du poster du réalisateur depuis les données du film
    realisateur_nom = movie.get('realisateurs', 'Inconnu')
    realisateur_poster = movie.get('directors_1_posters', '')  # À adapter si on a une url ou un chemin d'image pour le réalisateur
    
    # Gestion robuste de l'URL du poster
    # Fonction pour nettoyer et sécuriser une URL d'image
    def get_clean_url(poster, base_url, placeholder_url="https://placehold.co/150x225?text=No+Image"):
        if not isinstance(poster, str) or pd.isna(poster) or poster.strip() == '':
            return placeholder_url
        poster = poster.strip()
        if not poster.startswith("http"):
            return base_url + poster
        return poster

    # Application de la fonction
    realisateur_poster = get_clean_url(realisateur_poster, base_url)

    # Affichage du bloc
    col_real = st.columns(1)
    with col_real[0]:
        st.markdown(
            f"""
            <div style='text-align: center; margin-bottom: 40px;'>
            <a href="?director={realisateur_nom}" target="_self" style="text-decoration: none; color: white;">
                    <img src="{realisateur_poster}" 
                        style="
                            width: 300px;
                            height: 300px;
                            object-fit: cover;
                            border-radius: 10%;
                            border: 1px solid white;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                        ">
                    <p style='font-weight: bold; margin-top: 8px;font-size: 18px;'>{realisateur_nom}</p>
                    </a>            
            </div>
            """,
            unsafe_allow_html=True
        )

## ___________________________________________________________________________________________________________________________
## ----------------------------- Recommandations -----------------------------------------------------------------------------
## ___________________________________________________________________________________________________________________________


## Recommandations par titre

    st.markdown("<h2 style='color: #fff;'>Titres similaires</h2>", unsafe_allow_html=True)
    recommendations = get_recommendations_by_title(title, n=5)
    if not recommendations.empty:
        cols = st.columns(len(recommendations))
        for i, (_, row) in enumerate(recommendations.iterrows()):
            with cols[i]:
                st.markdown(
                    f"""
                    <a href="?movie={row['original_title']}" target="_self" style="text-decoration: none;">
                        <img src="{row.get('poster_url', 'https://placehold.co/300x450?text=No+Image')}" style="width:100%; border-radius: 10px;">
                        <p style='color: white; font-weight: bold; font-size: 18px; text-align: center;'>{row['original_title']}</p>
                    </a>
                    """,
                    unsafe_allow_html=True
                )

## Recommandations par acteurs

    st.markdown("<h2 style='color: #fff;'>Autres films avec vos acteurs préférés</h2>", unsafe_allow_html=True)
    index = get_film_index_by_title(title)
    actor_recs = recommend_by_actors(index=index, top_n=5)
    if not actor_recs.empty:
        cols = st.columns(len(actor_recs))
        for i, (_, row) in enumerate(actor_recs.iterrows()):
            with cols[i]:
                st.markdown(
                    f"""
                    <a href="?movie={row['original_title']}" target="_self" style="text-decoration: none;">
                        <img src="{row.get('poster_url', 'https://placehold.co/300x450?text=No+Image')}" style="width:100%; border-radius: 10px;">
                        <p style='color: white; font-weight: bold; font-size: 18px; text-align: center;'>{row['original_title']}</p>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
    else: 
        st.info("Aucune recommandation basée sur les acteurs.")

## ___________________________________________________________________________________________________________________________
## ----------------------------- Liste de Films par acteurs -----------------------------------------------------------------------------
## ___________________________________________________________________________________________________________________________
def show_actor_page(actor_name):
    st.markdown(f"<h1 style='text-align: center; color: #fff;'>Films avec {actor_name}</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    df = get_films_by_actor(actor_name)

    if df.empty:
        st.info("Aucun film trouvé pour cet acteur.")
        return

    cols = st.columns(5)
    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i % 5]:
            st.markdown(
                f"""
                <div style='display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;'>
                    <a href="?movie={row['original_title']}" target="_self" style="text-decoration: none; color: inherit;">
                        <img src="{row.get('poster_url', 'https://placehold.co/300x450?text=No+Image')}"
                            style="width: 100%; height: 270px; object-fit: cover; border-radius: 10px;">
                        <div style='color: white; font-weight: bold; text-align: center; margin-top: 8px;'>{row['original_title']}</div>
                        <div style='color: gold; text-align: center;'>⭐ {row['vote_average']:.1f}</div>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
        # Bouton retour aux films
    if st.button("⬅ Retour aux films"):
        # Nettoyer query params et retourner à la liste
        st.session_state.current_page = 'movie'
        st.query_params.clear()
        st.rerun()

## ___________________________________________________________________________________________________________________________
## ----------------------------- Liste de Films par réalisateurs -----------------------------------------------------------------------------
## ___________________________________________________________________________________________________________________________

def show_director_page(director_name):
    load_css("movie_style.css")
    st.markdown(f"<h1 style='text-align: center; color: #fff;'>Films réalisés par {director_name}</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Fonction de nettoyage du nom
    def normalize_name(name):
        return name.strip().lower().replace("é", "e").replace("-", " ").replace("è", "e").replace("ê", "e")

    # Normalisation pour filtrage
    normalized = normalize_name(director_name)
    films['realisateurs'] = films['realisateurs'].fillna('').astype(str).apply(normalize_name)

    matched = films[films['realisateurs'] == normalized]

    if matched.empty:
        st.warning("Aucun film trouvé pour ce réalisateur.")
        return

    cols = st.columns(5)
    for i, (_, row) in enumerate(matched.iterrows()):
        with cols[i % 5]:
            st.markdown(
                f"""
                <a href="?movie={row['original_title']}" target="_self" style="text-decoration: none;">
                    <img src="{row.get('poster_url', 'https://placehold.co/300x450?text=No+Image')}" 
                         style="width:100%; height: 270px; object-fit: cover; border-radius: 10px;">
                    <p style='color: white; font-weight: bold; font-size: 16px; text-align: center;'>
                        {row['original_title']}
                    </p>
                </a>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br><hr>", unsafe_allow_html=True)
    if st.button("⬅ Retour aux films"):
        st.session_state.current_page = 'movie'
        st.query_params.clear()
        st.rerun()
