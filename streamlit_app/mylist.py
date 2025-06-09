import streamlit as st
import pandas as pd
from recommendation import (
    films)


def my_list_page():
    st.markdown("<h1 style='color: #fff;'>Ma Liste</h1>", unsafe_allow_html=True)
    st.write("Bienvenue sur votre liste personnalisée de films !")

    if "my_list" not in st.session_state:
        st.session_state.my_list = []

    # Récupérer les films
    my_movies = films[films['original_title'].isin(st.session_state.my_list)]

    cols = st.columns(5)
    for i, (_, row) in enumerate(my_movies.iterrows()):
        with cols[i % 5]:
            st.markdown(
                f"""
                <a href="?movie={row['original_title']}" target="_self">
                    <img src="{row.get('poster_url', 'https://placehold.co/300x450?text=No+Image')}" style="width:100%;">
                    <p style="color:white;text-align:center;font-weight:bold;">{row['original_title']}</p>
                </a>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    if st.button("Retour aux films", key="back_to_films_button"):
        st.session_state.current_page = 'movie'
        st.query_params.clear()
       