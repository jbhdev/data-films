# pages/3_Details_Film.py
import streamlit as st
from utils.css_loader import load_css

load_css("style.css")
load_css("sidebar_style.css")

st.title("Détails du Film")
st.write("Affichez ici les informations détaillées d'un film.")
# In a real app, you'd fetch movie details based on some ID
st.subheader("Titre du Film : Le Film Épique")
st.write("Genre: Aventure, Fantastique")
st.write("Durée: 2h 30min")
st.image("https://placehold.co/400x300/87CEEB/ffffff?text=Affiche+du+Film", use_column_width=False)