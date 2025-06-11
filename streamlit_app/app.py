import streamlit as st
import os
from streamlit_lottie import st_lottie
import json
import time
from home import home_page
from mylist import my_list_page
from movie_detail import movie_detail_page, show_movie_details, show_actor_page, show_director_page
from utils.css_loader import load_css

if "my_list" not in st.session_state:
    st.session_state.my_list = []

st.set_page_config(
        page_title="Moviestar App",
        layout="wide",
        page_icon="assets/moviestar.png",
    )

# --- Fonction pour charger l'animation Lottie depuis un fichier local ---
def load_lottie_local(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Erreur : Le fichier Lottie '{filepath}' est introuvable. Assurez-vous qu'il est au même niveau que votre script Streamlit ou indiquez le chemin complet.")
        return None
    except json.JSONDecodeError:
        st.error(f"Erreur : Le fichier '{filepath}' n'est pas un JSON valide. Veuillez vérifier votre fichier Lottie.")
        return None

# --- Chemin de votre animation Lottie locale ---
LOTTIE_FILEPATH = "assets/panda.json"



# --- Session State pour contrôler l'affichage de l'animation ---
if 'animation_played' not in st.session_state:
    st.session_state.animation_played = False
# Si l'animation n'a pas encore été jouée
if not st.session_state.animation_played:
    # Utilisez un conteneur pour l'animation
    animation_placeholder = st.empty()
    
    

    with animation_placeholder: 
        
        lottie_json_data = load_lottie_local(LOTTIE_FILEPATH)
        if lottie_json_data:
            st_lottie(
                lottie_json_data,
                speed=3,
                width=600,
                height=600,
                key="logo_animation",
                loop=True
            )
            
            # Optionnel : Ajoutez un petit délai pour que l'utilisateur puisse voir l'animation
            time.sleep(3) # Ajustez la durée de l'animation + le temps de pause si besoin
        else:
            # Le message d'erreur est déjà géré dans load_lottie_local
            pass

    # Efface le contenu du placeholder une fois l'animation "terminée"
    animation_placeholder.empty()

    # Marquez l'animation comme jouée pour cette session
    st.session_state.animation_played = True
    


def init_session_state():
    defaults = {
        'current_page': 'home'
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

    # --- Sidebar ---
    with st.sidebar:
        st.image("assets/moviestar.png")
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