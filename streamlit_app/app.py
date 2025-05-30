import streamlit as st
import os

# Import page functions
from pages.home import home_page
from pages.search import search_page
from pages.movie_detail import movie_detail_page
from utils.css_loader import load_css

def main():
    st.set_page_config(
        page_title="Moviestar App",
        layout="wide",
        page_icon="assets/moviestar.png",  # Path to your logo
        initial_sidebar_state="auto" # 'auto' will show the sidebar by default
    )

    # Initialize session state for page if not already set
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'

   
    load_css("sidebar_style.css")  # Load global CSS for styling
    # --- Sidebar content ---
    with st.sidebar:
        # Logo
        st.image("assets/moviestar.png") # Disney+ logo

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
            
            # Login Button
        st.markdown('<div class="login-button-container">', unsafe_allow_html=True)
        if st.button("Connexion", key="login_button_sidebar"):
            st.info("Fonctionnalité de connexion à implémenter.")
        st.markdown('</div>', unsafe_allow_html=True)
        

    # --- Main content area (remains the same) ---
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
        
            <div class="footer">
                <p>&copy; 2025 Moviestar App. Tous droits réservés.</p>
                
            </div>
        
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
