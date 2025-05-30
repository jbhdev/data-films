# pages/1_Accueil.py
import streamlit as st
from utils.css_loader import load_css

load_css("style.css")
load_css("sidebar_style.css")

st.title("Page d'Accueil Détaillée")
st.write("Ceci est le contenu de votre page d'accueil principale.")
# Add any specific content that belongs on the home page, e.g., trending movies, welcome message etc.
st.image("https://placehold.co/800x400/FFA07A/ffffff?text=Accueil", use_column_width=True)