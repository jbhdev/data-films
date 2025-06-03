import streamlit as st
import os
from home import home_page
from search import search_page
from movie_detail import movie_detail_page, show_movie_details
from utils.css_loader import load_css

st.set_page_config(
        page_title="Moviestar App",
        layout="wide",
        page_icon="assets/moviestar.png",
    )

def init_session_state():
    defaults = {
        'current_page': 'home',
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def main():
    
    init_session_state()
    load_css("style.css")
    load_css("sidebar_style.css")

    # --- Lire les paramètres d'URL ---
    query_params = st.query_params
    movie_param = query_params.get("movie")

    # Vérifie si un film est sélectionné dans l'URL
    if movie_param:
        show_movie_details(movie_param)
        return

    # --- Sidebar ---
    with st.sidebar:
        st.image("assets/moviestar.png")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("ACCUEIL", key="nav_accueil_sidebar"):
            st.session_state.current_page = 'home'
            st.query_params.clear()
        if st.button("RECHERCHE", key="nav_recherche_sidebar"):
            st.session_state.current_page = 'search'
            st.query_params.clear()
        if st.button("MA LISTE", key="nav_ma_liste_sidebar"):
            st.session_state.current_page = 'favoris' # <-- ce nom représente la page Ma Liste
            st.info("La page 'MA LISTE' n'est pas encore implémentée.")
        if st.button("FILMS", key="nav_films_sidebar"):
            st.session_state.current_page = 'movie'
            st.query_params.clear()

        st.markdown('<div class="sidebar-profile-container">', unsafe_allow_html=True)
        user_pic_url = st.session_state.get("user_pic_url", "https://placehold.co/60x60/663399/ffffff?text=User")
        st.image(user_pic_url, width=60, clamp=True)
        st.markdown("<p class='sidebar-profile-name'>Johnbie</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Main content ---
    if st.session_state.current_page == 'search':
        search_page()
    elif st.session_state.current_page == 'movie':
        movie_detail_page()  # la page qui liste les films (posters cliquables)
    else:
        home_page()

    # --- Footer ---
    st.markdown(
        """
        <footer class="footer">
            <p>&copy; 2024 Moviestar App. Tous droits réservés.</p>
            <p>
                <a href="#" class="footer-link">Règles de Respect de la Vie Privée</a> |
                <a href="#" class="footer-link">Conditions d'utilisation</a> |
                <a href="#" class="footer-link">Politique de cookies</a>
            </p>
        </footer>
        """,
        unsafe_allow_html=True
    )
if __name__ == "__main__":
    main()
