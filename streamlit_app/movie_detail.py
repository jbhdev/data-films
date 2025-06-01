import streamlit as st
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
    range_buffer = 2

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
                st.markdown("<span style='margin: 6px; color: #ccc;'>…</span>", unsafe_allow_html=True)
            else:
                if p == st.session_state.movie_page:
                    # Page active : bouton différent
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
    st.markdown(f"<h1 style='text-align: center; color: #fff;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    movie_data = films[films["original_title"] == title]
    if movie_data.empty:
        st.error("Film introuvable.")
        return

    movie = movie_data.iloc[0]
    trailer_url = movie.get("trailer_url")

    if "show_trailer" not in st.session_state:
        st.session_state.show_trailer = False

    vote_average = movie.get('vote_average', 0)
    stars = "★" * int(round(float(vote_average) / 2)) + "☆" * (5 - int(round(float(vote_average) / 2)))

    st.markdown(
        f"""
        <div class="movie-header">
            <img src="{movie.get('poster_url', 'https://placehold.co/300x450?text=No+Image')}" width="300" height="450">
            <div class="movie-details">
                <p>{movie.get('startYear', 'Année inconnue')} || {movie.get('genres', 'Genre inconnu')} || {movie.get('runtimeMinutes', 'Durée inconnue')} min</p>
                <p>{movie.get('overview', 'Pas de description disponible.')}</p>
                <p style="color: white;">
                    {vote_average} / 10<br>
                    <span style="color: gold; font-size: 20px;">{stars}</span>
                </p>
                <p>Avec : {movie.get('acteurs_1')}, {movie.get('acteurs_2')}, {movie.get('actrices')}</p>
                <p>Réalisateur : {movie.get('realisateurs')}</p>
                <div class="movie-actions">
                    <button>🎬 Lancer</button>
                    <button>➕ Ajouter à ma liste</button>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    youtube_id = None
    if isinstance(trailer_url, str):
        if "watch?v=" in trailer_url:
            youtube_id = trailer_url.split("watch?v=")[-1]
        elif "youtu.be/" in trailer_url:
            youtube_id = trailer_url.split("youtu.be/")[-1]

        if youtube_id:
            st.markdown(
                f"""
                <div style="position: relative; padding-bottom: 56.25%; height: 0; margin-top: 20px;">
                    <iframe src="https://www.youtube.com/embed/{youtube_id}" 
                            style="position: absolute; top: 0; left: 0; width: 50%; height: 50%;" 
                            frameborder="0" allowfullscreen>
                    </iframe>
                </div>
                """,
                unsafe_allow_html=True
            )

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
                        <p style='color: white; text-align: center;'>{row['original_title']}</p>
                    </a>
                    """,
                    unsafe_allow_html=True
                )

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
                        <p style='color: white; text-align: center;'>{row['original_title']}</p>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
    else: 
        st.info("Aucune recommandation basée sur les acteurs.")
