import streamlit as st
from utils.css_loader import load_css

def home_page():
    """
    Displays the home page content.
    """
    load_css("style.css") # Load specific CSS for this page
    

    # --- Moviestar Banner Section (single image) ---
    st.markdown("<h1 style='color: #fff;'>Déjà sur Moviestar</h2>", unsafe_allow_html=True)

    st.image("https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/415b599e-9d55-4809-9dbc-38bd89fe14ac/compose?format=webp&label=hero_carousel_none_300&width=2880", use_container_width=True,
             caption="American Dad, Saison 20 disponible dès maintenant, 2005, Comédie, Animation",
             output_format="auto", # Ensures best format for display
             )
    
    st.markdown("<br>", unsafe_allow_html=True)
    # --- End Moviestar Banner Section ---


    # "Notre sélection pour vous" section
    st.markdown("<h2 style='color: #fff;'>Notre sélection pour vous</h2>", unsafe_allow_html=True)

    # Movie data
    movies = [
        {"title": "MULAN", "year": "1998", "genre": "Action and adventure, Story...", "age": "6+", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/7dad0c2d-b314-4929-a9c2-294e9e25fc63/compose?format=webp&label=poster_vertical_080&width=800"},
        {"title": "THE RETURN OF JAFAR", "year": "1994", "genre": "Action and adventure, Anim....", "age": "0+", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/50ce8306-b1e9-41e5-9954-2776218049fe/compose?format=webp&label=poster_vertical_080&width=800"},
        {"title": "MULAN 2", "year": "2005", "genre": "Action and adventure, Anim...", "age": "6+", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/d93e9c56-9349-407e-9b62-a7f9c628a6ad/compose?format=webp&label=poster_vertical_080&width=800"},
        {"title": "POCAHONTAS", "year": "1995", "genre": "Action and adventure, History....", "age": "6+", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/c1bb91cf-6c10-4987-b9b6-8d0dad58f8bb/compose?format=webp&label=poster_vertical_080&width=800"},
        {"title": "BEAUTY AND THE BEAST", "year": "1991", "genre": "Animation, Romance", "age": "6+", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/5d2b32a2-45b6-4465-99cf-e63240e5a364/compose?format=webp&label=poster_vertical_080&width=800"},
    ]

    # Display movies in columns
    cols = st.columns(len(movies)) # Create as many columns as there are movies

    for i, movie in enumerate(movies):
        with cols[i]:
            st.image(movie["image"], use_container_width=True)
            st.markdown(
                f"""
                <p style='color: #fff; font-weight: bold; margin-bottom: 2px;'>{movie["title"]}</p>
                <p style='color: #999; font-size: 12px;'>{movie["age"]} | {movie["year"]} | {movie["genre"]}</p>
                """,
                unsafe_allow_html=True
            )

 