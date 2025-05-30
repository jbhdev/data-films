import streamlit as st
from utils.css_loader import load_css

load_css("style.css")
load_css("sidebar_style.css")

st.title("Page Ma liste")
st.write("Ceci est le contenu de votre page ma liste.")