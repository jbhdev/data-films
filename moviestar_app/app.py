import streamlit as st
import os

# Importez les fonctions de vos pages
# Assurez-vous que le chemin est correct (par exemple, 'pages.home_page' si 'pages' est un paquet)
from pages.home_page import home_page
from pages.search_page import search_page
from pages.movie_detail_page import movie_detail_page
from pages.ma_liste_page import ma_liste_page # Importez la nouvelle page "Ma Liste"

# Importez votre utilitaire CSS
from utils.css_loader import load_css

# --- Fonctions utilitaires de navigation ---
def set_page(page_name):
    """Met à jour l'état de la session pour changer de page."""
    st.session_state.current_page = page_name

# --- Logique principale de l'application ---
def main():
    st.set_page_config(
        page_title="Moviestar App - Navigation Personnalisée",
        layout="wide",
        page_icon="assets/moviestar.png",
    )

    # Chargez les CSS globaux
    load_css("style.css")
    load_css("sidebar_style.css") # Pour styliser votre barre latérale personnalisée

    # Initialisez l'état de la session pour la page courante si ce n'est pas déjà fait
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home' # La page par défaut au démarrage

    # --- Contenu de la barre latérale personnalisée ---
    with st.sidebar:
        # Logo
        st.image("assets/moviestar.png", use_column_width=True)
        st.markdown("<br>", unsafe_allow_html=True) # Ajoute de l'espace

        # Boutons de navigation personnalisés
        # Utilisez st.button avec une fonction lambda pour appeler set_page
        if st.button("ACCUEIL", key="nav_accueil", help="Retour à la page d'accueil"):
            set_page('home')
        if st.button("RECHERCHE", key="nav_recherche", help="Rechercher des films"):
            set_page('search')
        if st.button("MA LISTE", key="nav_ma_liste", help="Voir votre liste de films"):
            set_page('ma_liste')
        # Si vous voulez une page "Films" générique qui mène aux détails,
        # ou si elle mène à une liste de films avant les détails
        if st.button("FILMS", key="nav_films", help="Explorer tous les films"):
            set_page('movie_detail') # Pour cet exemple, cela mène à la page de détail

        st.markdown("<br>", unsafe_allow_html=True)

        # Contenu du profil utilisateur (inchangé)
        st.markdown('<div class="sidebar-profile-container">', unsafe_allow_html=True)
        st.image("https://placehold.co/60x60/663399/ffffff?text=User", width=60, clamp=True)
        st.markdown("<p class='sidebar-profile-name'>Johnbie</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Zone de contenu principal ---
    # Rendu de la page courante basé sur l'état de la session
    if st.session_state.current_page == 'home':
        home_page()
    elif st.session_state.current_page == 'search':
        search_page()
    elif st.session_state.current_page == 'movie_detail':
        movie_detail_page()
    elif st.session_state.current_page == 'ma_liste':
        ma_liste_page()
    else:
        # Fallback au cas où current_page aurait une valeur inattendue
        home_page()
    # --- Pied de page ---
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