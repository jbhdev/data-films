import pandas as pd
import streamlit as st
st.write("Hello World")

# Titre principal de l'application (affiché en haut de la page)
st.title("The title of my page")

# Titre de section important (taille 1)
st.header("An Important Header")

# Sous-titre (taille 2), utile pour organiser le contenu par sous-sections
st.subheader("A Secondary Header")

# Affiche une ligne de texte simple (sans mise en forme particulière)
st.text("My classic text")

# Affiche du texte avec mise en forme Markdown
st.markdown(''':rainbow: :rainbow[My markdown]''')  # Ici, un effet arc-en-ciel est appliqué

# Affiche un dataframe (st.write accepte plusieurs arguments et plusieurs types de données)
st.write(
    pd.DataFrame({
            "Cards": ['Name 1', 'Name 2', 'Name 3', 'Name 4'],
            "Quantity": [0, 1, 0, 3]}
    )
)