import streamlit as st
import pandas as pd
from recommendation import (
    films)


def encode_title(title):
    """Encode un titre de film pour l'URL"""
    return title.replace(' ', '+').replace('&', '%26')

def decode_title(encoded_title):
    """Décode un titre de film depuis l'URL"""
    return encoded_title.replace('+', ' ').replace('%26', '&')

def my_list_page():
    st.markdown("<h1 style='color: #fff;'>Ma Liste</h1>", unsafe_allow_html=True)
    st.write("Bienvenue sur votre liste personnalisée de films !")

    if "my_list" not in st.session_state:
        st.session_state.my_list = []

    # Récupérer les films
    my_movies = films[films['original_title'].isin(st.session_state.my_list)]

    if my_movies.empty:
        st.info("Votre liste est vide. Ajoutez des films en cliquant sur le bouton '➕ Ajouter à ma liste' sur les pages de détails.")
        return

    # Afficher les films en colonnes
    cols = st.columns(5)
    for i, (_, row) in enumerate(my_movies.iterrows()):
        with cols[i % 5]:
            # Afficher le film
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <a href="?movie={row['original_title']}" target="_self" style="text-decoration: none;">
                        <img src="{row.get('poster_url', 'https://placehold.co/300x450?text=No+Image')}" 
                             style="width:100%; height: 270px; object-fit: cover; border-radius: 10px;">
                        <p style='color: white; font-weight: bold; font-size: 16px; text-align: center;'>
                            {row['original_title']}
                        </p>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Bouton de suppression Streamlit
            if st.button("Supprimer", key=f"delete_{row['original_title']}"):
                st.session_state.my_list.remove(row['original_title'])
                st.success(f"{row['original_title']} a été supprimé de votre liste.")
                st.rerun()

    st.markdown("---")

    # Bouton retour
    if st.button("Retour aux films", key="back_to_films_button"):
        st.session_state.current_page = 'movie'
        st.rerun()