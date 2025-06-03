import streamlit as st
from utils.css_loader import load_css # Assurez-vous que ce module est correctement configuré

def search_page():
    """
    Displays the search page content with a grid of results.
    """
    load_css("style.css") # Load global CSS for styling

    # --- Search Input Section ---
    st.markdown("<h1 style='color: #fff;'>Recherche</h1>", unsafe_allow_html=True)

    # Custom CSS for the search input to match the dark theme and look
    st.markdown("""
        <style>
            .stTextInput>div>div>input {
                color: #black; /* White text */
                border: 1px solid #555555; /* Subtle border */
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 16px;
                
            }
            .stTextInput>div>div>input::placeholder {
                color: #aaa; /* Placeholder text color */
            }
            /* Adjust padding of the stForm for the search input if needed */
            .css-1r6dn7c { /* This class might target the form element around st.text_input */
                padding: 0;
            }
        </style>
    """, unsafe_allow_html=True)

    # The search input field
    # label_visibility="collapsed" hides the default Streamlit label
    search_query = st.text_input("Rechercher un titre", placeholder="Titre , personnage ou genre", label_visibility="collapsed")
    


    # --- Dummy data for search results ---
    # In a real application, this data would come from an API call
    # based on the search_query.
    all_movies = [

{"title": "MULAN", "year": "1998", "genre": "Action et aventure", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/7dad0c2d-b314-4929-a9c2-294e9e25fc63/compose?format=webp&label=poster_vertical_080&width=800"},

{"title": "MULAN 2", "year": "2005", "genre": "Action et aventure", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/d93e9c56-9349-407e-9b62-a7f9c628a6ad/compose?format=webp&label=poster_vertical_080&width=800"},

{"title": "CENDRILLON", "year": "2015", "genre": "Romance, Fantastique", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/dc14f26f-c930-481d-aac3-b35e110dadc1/compose?format=webp&label=poster_vertical_080&width=800"},

{"title": "LA PETITE SIRENE", "year": "2018", "genre": "Action, Horreur", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/62791a68-88f9-4cf1-ba31-492ff6f5909f/compose?format=webp&label=poster_vertical_080&width=800"},

{"title": "ANASTASIA", "year": "2022", "genre": "Aventure, Animation", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/baf6ae08-907a-4355-9da4-f620a3dbf4ac/compose?format=webp&label=poster_vertical_080&width=800"},

{"title": "CRUELLA", "year": "2021", "genre": "Drame, Policier", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/60e4c384-bc25-4b09-b00f-09b723422fe1/compose?format=webp&label=poster_vertical_080&width=800"},

{"title": "BLACK SWAN", "year": "2010", "genre": "Drame, Mystère", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/a6d609ba-1fe3-46f3-9f4f-d16dc9e7f1c9/compose?format=webp&label=poster_vertical_080&width=800"},

{"title": "MALEFIQUE", "year": "2014", "genre": "Action, Aventure, Fantastique", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/5896e7cf-30c2-484f-87af-a62c6926a3ca/compose?format=webp&label=poster_vertical_080&width=800"},

{"title": "LA PRINCESSE ET LA GRENOUILLE", "year": "2009", "genre": "Animation, Comédie", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/a2a5ea6d-6671-4c7e-8248-3a1514580488/compose?format=webp&label=poster_vertical_080&width=800"},

{"title": "RAIPONCE", "year": "2010", "genre": "Action, Aventure", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/d50ccce8-da72-45d9-aef0-e7eb0a3f6d75/compose?format=webp&label=poster_vertical_080&width=800"},


]


    # Filter results based on search query (case-insensitive)
    if search_query:
        filtered_results = [
            item for item in all_movies
            if search_query.lower() in item["title"].lower()
        ]
    else:
        filtered_results = all_movies # Show all movies if no search query

    if not filtered_results:
        st.markdown("<p style='color: #999; text-align: center;'>Aucun résultat trouvé pour votre recherche.</p>", unsafe_allow_html=True)
        return

    # --- Display results in a grid of 5 columns ---
    num_columns = 5
    cols = st.columns(num_columns) # Initialize columns outside the loop

    for i, movie in enumerate(filtered_results):
        # Place item in the current column (looping through cols)
        with cols[i % num_columns]:
            st.image(movie["image"], use_container_width=True)
            st.markdown(
                f"""
                <p style='color: #fff; font-weight: bold; margin-bottom: 2px; font-size: 14px;'>{movie["title"]}</p>
                <p style='color: #999; font-size: 11px;'>{movie["year"]} | {movie["genre"]}</p>
                """,
                unsafe_allow_html=True
            )

