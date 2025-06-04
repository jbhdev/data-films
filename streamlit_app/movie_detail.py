import streamlit as st
import pandas as pd 
import ast
from utils.css_loader import load_css
import string
from recommendation import (
    get_recommendations_by_title,
    recommend_by_actors,
    films,
    get_film_index_by_title,
)

def movie_detail_page():
    load_css("movie_style.css")
    st.markdown("<h1 style='text-align: center; color: #fff;'>Tous les films</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- LETTRES ALPHABÉTIQUES ---
    all_letters = list(string.ascii_uppercase) + ['#']
    st.markdown(""" <style>div[class*="stRadio"] > label {font-size: 100px !important;padding: 50px 100px;
    }div[class*="stRadio"] > div {gap: 20px;} </style>
                """, unsafe_allow_html=True)

    selected_letter = st.radio("Filtrer par lettre", all_letters,label_visibility="hidden", horizontal=True)

    def starts_with_letter(title):
        if not title or not isinstance(title, str):
            return False
        if selected_letter == '#':
            return not title[0].upper() in string.ascii_uppercase
        return title.upper().startswith(selected_letter)

    filtered_movies = films[["original_title", "poster_url"]].dropna(subset=["original_title"])
    filtered_movies = filtered_movies[filtered_movies["original_title"].apply(starts_with_letter)]
    sorted_movies = filtered_movies.sort_values("original_title")

    films_per_page = 20
    total_pages = max(1, (len(sorted_movies) - 1) // films_per_page + 1)

    if "movie_page" not in st.session_state:
        st.session_state.movie_page = 1
    if "last_letter" not in st.session_state:
        st.session_state.last_letter = selected_letter

    if st.session_state.last_letter != selected_letter:
        st.session_state.movie_page = 1
        st.session_state.last_letter = selected_letter

    start_idx = (st.session_state.movie_page - 1) * films_per_page
    end_idx = start_idx + films_per_page
    page_movies = sorted_movies.iloc[start_idx:end_idx]

    cols = st.columns(5)
    for i, (_, row) in enumerate(page_movies.iterrows()):
        with cols[i % 5]:
            st.markdown(
                f"""
                <div style='display: flex; flex-direction: column; align-items: center; height: 340px; margin-bottom: 10px;'>
                    <a href="?movie={row['original_title']}" style="text-decoration: none; width: 100%;">
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

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'><p style='color: white;'>Pages :</p></div>", unsafe_allow_html=True)

    max_visible = 10
    current = st.session_state.movie_page

    pages = []
    num_start_pages = 4
    num_end_pages = 4
    range_buffer = 4

    if total_pages <= (num_start_pages + num_end_pages + 2 * range_buffer + 2):
        pages = list(range(1, total_pages + 1))
    else:
        pages.extend(range(1, num_start_pages + 1))
        if current > num_start_pages + range_buffer + 1:
            pages.append("...")
        start = max(current - range_buffer, num_start_pages + 1)
        end = min(current + range_buffer, total_pages - num_end_pages)
        pages.extend(i for i in range(start, end + 1) if i not in pages)
        if current < total_pages - num_end_pages - range_buffer:
            pages.append("...")
        pages.extend(range(total_pages - num_end_pages + 1, total_pages + 1))

    pagination_cols = st.columns(len(pages))
    for idx, p in enumerate(pages):
        with pagination_cols[idx]:
            if p == "...":
                st.markdown("<span style='margin: 8px; color: #red;'>…</span>", unsafe_allow_html=True)
            else:
                if p == st.session_state.movie_page:
                    st.markdown(
                        f"""
                        <div style="padding: 8px 16px; background-color: gold; color: black; 
                                    font-weight: bold; border-radius: 6px; text-align: center;">
                            {p}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    if st.button(str(p), key=f"page_{p}"):
                        st.session_state.movie_page = p
                        st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

def show_movie_details(title):
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
        stars = "⭐" * int(round(vote_average)/2) + "☆" * (5 - int(round(vote_average / 2)))

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

    acteurs = [
        {"nom": movie.get("acteurs_1", ""), "poster": movie.get("actors_1_posters", "")},
        {"nom": movie.get("acteurs_2", ""), "poster": movie.get("actors_2_posters", "")},
        {"nom": movie.get("actrices", ""), "poster": movie.get("actress_1_posters", "")},
    ]

    acteur_cols = st.columns(len(acteurs))
    for i, acteur in enumerate(acteurs):
        poster_path = acteur['poster'].strip() if acteur['poster'] else ''
        if poster_path and not poster_path.startswith("http"):
            poster_url = base_url + poster_path
        else:
            poster_url = poster_path or 'https://placehold.co/150x225?text=No+Image'

        with acteur_cols[i]:
            st.markdown(
                f"""
                <div style='text-align: center;'>
                    <a href="?actor={acteur['nom']}" style="text-decoration: none; color: inherit;">
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

    ### --------- Bloc réalisateur sous les acteurs---------
    st.markdown("<h2 style='color: #fff; margin-top: 40px;'>Réalisateur</h2>", unsafe_allow_html=True)
    
    # Récupération du poster du réalisateur depuis les données du film
    realisateur_nom = movie.get('realisateurs', 'Inconnu')
    realisateur_poster = movie.get('directors_1_posters', '')  # À adapter si on a une url ou un chemin d'image pour le réalisateur
    
    # Gestion robuste de l'URL du poster
    if pd.isna(realisateur_poster) or realisateur_poster == '':
        realisateur_poster = "https://placehold.co/150x225?text=No+Image"
    else:
        realisateur_poster = str(realisateur_poster)
        if not realisateur_poster.startswith("https://"):
            realisateur_poster = base_url + realisateur_poster

    col_real = st.columns(1)
    with col_real[0]:
        st.markdown(
            f"""
            <div style='text-align: center; margin-bottom: 40px;'>
                    <img src="{realisateur_poster}" 
                        style="
                            width: 300px;
                            height: 300px;
                            object-fit: cover;
                            border-radius: 10%;
                            border: 1px solid white;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                        ">
                    <p style='color: white; font-weight: bold; margin-top: 8px;font-size: 18px;'>{realisateur_nom}</p> 
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
                    <a href="?movie={row['original_title']}" style="text-decoration: none;">
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
                    <a href="?movie={row['original_title']}" style="text-decoration: none;">
                        <img src="{row.get('poster_url', 'https://placehold.co/300x450?text=No+Image')}" style="width:100%; border-radius: 10px;">
                        <p style='color: white; font-weight: bold; font-size: 18px; text-align: center;'>{row['original_title']}</p>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
    else: 
        st.info("Aucune recommandation basée sur les acteurs.")

