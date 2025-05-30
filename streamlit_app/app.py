import streamlit as st
import os

# Import page functions
from home import home_page
from search import search_page
from movie_detail import movie_detail_page
from utils.css_loader import load_css # Import the CSS loader utility

# Main application logic
def main():
    st.set_page_config(
        page_title="Moviestar App",
        layout="wide",
        page_icon="assets/moviestar.png",  # Path to your logo
        
    )

    #Load global CSS
    load_css("style.css")
    # Load sidebar specific CSS
    load_css("sidebar_style.css")


    # Initialize session state for page if not already set
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    # Removed: 'show_login_modal' and 'is_signup_mode' session state initializations


    # --- Sidebar content ---
    with st.sidebar:
        # Logo
        st.image("assets/moviestar.png") # [Image of Moviestar Logo]

        st.markdown("<br>", unsafe_allow_html=True) # Add some space

        # Navigation buttons
        if st.button("ACCUEIL", key="nav_accueil_sidebar"):
            st.session_state.current_page = 'home'
        if st.button("RECHERCHE", key="nav_recherche_sidebar"):
            st.session_state.current_page = 'search'
        if st.button("MA LISTE", key="nav_ma_liste_sidebar"):
            # For now, if no specific page, redirect to home or show a message
            st.session_state.current_page = 'home'
            st.info("La page 'MA LISTE' n'est pas encore implémentée.")
        if st.button("FILMS", key="nav_films_sidebar"):
            st.session_state.current_page = 'movie'

        # Removed: Login Button and its container

        # User profile
        st.markdown('<div class="sidebar-profile-container">', unsafe_allow_html=True)
        st.image("https://placehold.co/60x60/663399/ffffff?text=User", width=60, clamp=True) # Placeholder for user profile pic
        st.markdown("<p class='sidebar-profile-name'>Johnbie</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Removed: Render the login modal if active (login_modal() call)

    # --- Main content area ---
    # Render the current page based on session state
    if st.session_state.current_page == 'search':
        search_page()
    elif st.session_state.current_page == 'movie':
        movie_detail_page()
    else: # Default to home page
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
