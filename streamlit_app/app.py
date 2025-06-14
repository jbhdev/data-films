import streamlit as st
import os
from home import home_page
from mylist import my_list_page
from movie_detail import movie_detail_page, show_movie_details, show_actor_page, show_director_page
from stats import show_stats_page
from utils.css_loader import load_css, load_image_path

if "my_list" not in st.session_state:
    st.session_state.my_list = []

st.set_page_config(
    page_title="Moviestar App",
    layout="wide",
    page_icon="🎬",  # ✅ Utilisez un emoji
)

def init_session_state():
    defaults = {
        'current_page': 'home'
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
 
def main():
    init_session_state()
    
    # Chargement des CSS
    load_css("style.css")
    load_css("sidebar_style.css")

    # --- Lire les paramètres d'URL ---
    query_params = st.query_params
    movie_param = query_params.get("movie")
    actor_param = query_params.get("actor") 
    director_param = query_params.get("director")

    # --- Sidebar ---
    with st.sidebar:
        # ✅ Chargement sécurisé de l'image
        image_path = load_image_path("moviestar.png")
        if image_path:
            st.image(image_path)
        else:
            st.markdown("🎬 **Moviestar App**")  # Fallback si image non trouvée
        
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("ACCUEIL", key="nav_accueil_sidebar"):
            st.session_state.current_page = 'home'
            st.query_params.clear()

        if st.button("RECHERCHE", key="nav_films_sidebar"):
            st.session_state.current_page = 'movie'
            st.query_params.clear()

        if st.button("MA LISTE", key="nav_ma_liste_sidebar"):
            st.session_state.current_page = 'my_list' 
            st.query_params.clear()
            
        if st.button("STATISTIQUES", key="nav_stats_sidebar"):
            st.session_state.current_page = 'stats'
            st.query_params.clear()
        
    # --- Main content ---
    if movie_param:
        show_movie_details(movie_param)
    elif actor_param: 
        show_actor_page(actor_param)
    elif director_param:
        show_director_page(director_param)
    else:    
        if st.session_state.current_page == 'movie':
            movie_detail_page()  # la page qui liste les films (posters cliquables)
        elif st.session_state.current_page == 'my_list':
            my_list_page()
        elif st.session_state.current_page == 'stats':
            show_stats_page()
        else:
            home_page()

    # --- Footer ---
    st.markdown(
        """
        <footer class="footer">
            <p>&copy; 2025 Moviestar App. Tous droits réservés.</p>
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
