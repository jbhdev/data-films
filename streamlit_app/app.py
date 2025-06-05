import streamlit as st
import os
from home import home_page
from search import search_page 
from mylist import my_list_page
from movie_detail import movie_detail_page, show_movie_details, show_actor_page, show_director_page
from utils.css_loader import load_css


st.set_page_config(
        page_title="Moviestar App",
        layout="wide",
        page_icon="assets/moviestar.png",
    )
st.balloons()

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
    actor_param = query_params.get("actor") 
    director_param = query_params.get("director")

    # Vérifie si un film est sélectionné dans l'URL
    if movie_param:
        show_movie_details(movie_param)
        return
    elif actor_param: 
        show_actor_page(actor_param)
        return
    elif director_param:
        show_director_page(director_param)
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
            st.session_state.current_page = 'my_list' # <--- CHANGE THIS TO 'my_list'
            st.query_params.clear()
        if st.button("FILMS", key="nav_films_sidebar"):
            st.session_state.current_page = 'movie'
            st.query_params.clear()

        

    # --- Main content ---
    if st.session_state.current_page == 'search':
        search_page()
    elif st.session_state.current_page == 'movie':
        movie_detail_page()  # la page qui liste les films (posters cliquables)
    elif st.session_state.current_page == 'my_list':
        my_list_page() 
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
