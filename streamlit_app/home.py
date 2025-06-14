import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta

# Local utilities (assuming these files are in your project)

from movie_detail import show_movie_details
from recommendation import films # Assuming 'films' is a pandas DataFrame


# --- Constants ---
# Base URL for TMDB movie posters
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
# Columns required in the 'films' DataFrame for displaying movie cards
REQUIRED_FILM_COLUMNS = ['vote_average', 'poster_path', 'original_title', 'release_date', 'genres']


# --- Helper Functions ---

def get_movie_card_html(movie_data: dict) -> str:
    """
    Generates the HTML for a single movie card.
    The card includes an image, title, rating, year, and genres,
    and acts as a clickable link to the movie's detail page.

    Args:
        movie_data (dict): A dictionary containing movie information
                           (must include 'original_title', 'poster_path',
                           'vote_average', 'release_date', 'genres').

    Returns:
        str: An HTML string representing the movie card.
    """
    # Ensure release_date is a datetime object or can be converted to year
    release_year = movie_data["release_date"].year if pd.notna(movie_data["release_date"]) else 'N/A'
    
    return f"""
    <a href="?movie={movie_data['original_title']}" style="text-decoration: none;" target="_self">
        <div style="text-align: center;">
            <img src="{movie_data['poster_path']}" style="width: 100%; height: auto;">
            <p style='color: #fff; font-weight: bold; margin-bottom: 2px;'>{movie_data["original_title"]}</p>
            <p style='color: #999; font-size: 12px;'>⭐ {round(movie_data["vote_average"], 1)} | {release_year} | {movie_data["genres"]}</p>
        </div>
    </a>
    """

def apply_home_page_styles():
    """
    Applies the custom CSS styles for the Hollywood-themed title,
    subtitle, and background stars.
    """
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue:wght@400&family=Anton:wght@400&display=swap');
            
            body {
                background-color: #0d1117; /* Dark background for stars */
                overflow-x: hidden; /* Prevent horizontal scrollbar from stars */
            }

            /* --- Starry Background Effect --- */
            .stars {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none; /* Allows clicks on content below */
                z-index: -1; /* Places stars behind main content */
                background: transparent;
            }

            .star {
                position: absolute;
                background-color: white;
                border-radius: 50%;
                opacity: 0;
                animation: twinkle 5s infinite ease-in-out;
            }

            /* Define individual star positions, sizes, and animation delays */
            .star:nth-child(1) { width: 2px; height: 2px; top: 10%; left: 20%; animation-delay: 0s; }
            .star:nth-child(2) { width: 3px; height: 3px; top: 5%; left: 70%; animation-delay: 1s; }
            .star:nth-child(3) { width: 2px; height: 2px; top: 20%; left: 85%; animation-delay: 2s; }
            .star:nth-child(4) { width: 4px; height: 4px; top: 30%; left: 40%; animation-delay: 0.5s; }
            .star:nth-child(5) { width: 2px; height: 2px; top: 15%; left: 50%; animation-delay: 2.5s; }
            .star:nth-child(6) { width: 3px; height: 3px; top: 25%; left: 10%; animation-delay: 1.5s; }
            .star:nth-child(7) { width: 2px; height: 2px; top: 35%; left: 95%; animation-delay: 3s; }
            .star:nth-child(8) { width: 3px; height: 3px; top: 40%; left: 60%; animation-delay: 0.8s; }
            .star:nth-child(9) { width: 2px; height: 2px; top: 18%; left: 30%; animation-delay: 3.5s; }
            .star:nth-child(10) { width: 4px; height: 4px; top: 22%; left: 5%; animation-delay: 1.2s; }
            /* Add more .star:nth-child(n) rules for more stars if needed */

            @keyframes twinkle {
                0%, 100% { opacity: 0; transform: scale(0.5); }
                50% { opacity: 0.8; transform: scale(1); }
            }

            /* --- Hollywood Title Container --- */
            .hollywood-container {
                position: relative;
                text-align: center;
                margin-top: -80px; /* Pulls it up to overlap the header a bit */
                margin-bottom: 60px;
                padding: 60px 20px;
                background: linear-gradient(135deg, 
                    rgba(51, 51, 51, 0.9) 0%, 
                    rgba(34, 34, 34, 0.95) 50%, 
                    rgba(17, 17, 17, 0.9) 100%);
                border-radius: 15px;
                box-shadow: 
                    0 20px 40px rgba(0, 0, 0, 0.6), /* Stronger shadow for depth */
                    inset 0 1px 0 rgba(255, 255, 255, 0.1); /* Inner light effect */
                overflow: hidden;
                z-index: 10; /* Ensures it's above the stars */
            }
            
            /* Hills in the background of the container */
            .hollywood-container::before {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 40%;
                background: linear-gradient(to top,
                    rgba(101, 67, 33, 0.8) 0%,
                    rgba(139, 90, 43, 0.6) 30%,
                    rgba(160, 120, 80, 0.4) 60%,
                    transparent 100%);
                z-index: 1; /* Below the text, above the container background */
            }
            
            /* --- Main Title Styling --- */
            .moviestar-title {
                font-family: 'Anton', 'Bebas Neue', sans-serif;
                font-size: 9.5em; /* Very large title */
                font-weight: 400;
                letter-spacing: 15px; /* Increased spacing for prominence */
                text-transform: uppercase;
                margin: 0;
                padding: 0;
                position: relative;
                z-index: 2; /* Ensures text is above hills */
                color: #FFFFFF; /* Classic Hollywood sign white */
                
                /* Multiple text shadows for 3D and glow effect */
                text-shadow: 
                    6px 6px 0px #000000, 
                    12px 12px 0px #000000,
                    18px 18px 0px #000000, /* Deeper black shadows */
                    24px 24px 30px rgba(0, 0, 0, 0.8), /* Soft, wide shadow for depth */
                    0 0 25px rgba(255, 255, 255, 0.8), /* Strong white glow */
                    0 -4px 0px rgba(255, 255, 255, 0.6); /* Top highlight/reflection */
                
                /* Perspective transform for angled 3D look */
                transform: perspective(300px) rotateX(15deg);
                transform-origin: center bottom;
            }
            
            /* Animation for subtle lighting effect on title */
            .moviestar-title {
                animation: hollywood-shine 4s ease-in-out infinite;
            }
            
            @keyframes hollywood-shine {
                0%, 100% {
                    text-shadow: 
                        6px 6px 0px #000000, 12px 12px 0px #000000, 18px 18px 0px #000000,
                        24px 24px 30px rgba(0, 0, 0, 0.8),
                        0 0 25px rgba(255, 255, 255, 0.8), 
                        0 -4px 0px rgba(255, 255, 255, 0.6);
                }
                50% {
                    text-shadow: 
                        6px 6px 0px #000000, 12px 12px 0px #000000, 18px 18px 0px #000000,
                        24px 24px 30px rgba(0, 0, 0, 0.8),
                        0 0 45px rgba(255, 255, 255, 1), /* Brighter glow at peak */
                        0 -4px 0px rgba(255, 255, 255, 0.9),
                        0 0 60px rgba(255, 255, 255, 0.7); /* Wider, softer halo */
                }
            }
            
            /* --- Subtitle Styling --- */
            .moviestar-subtitle {
                font-family: 'Bebas Neue', sans-serif;
                font-size: 2.8em; /* Large subtitle */
                font-weight: 400;
                letter-spacing: 8px; /* Increased spacing */
                text-transform: uppercase;
                color: #CCCCCC; /* Default gray for non-highlighted parts */
                margin-top: 25px; /* Spacing from title */
                position: relative;
                z-index: 2;
                text-shadow: 
                    3px 3px 6px rgba(0, 0, 0, 0.8), /* Dark shadow for depth */
                    0 0 12px rgba(255, 255, 255, 0.3); /* Subtle white glow */
            }
            
            /* Highlighted yellow text within the subtitle */
            .moviestar-subtitle .yellow-text {
                color: #fdc74c; /* Specific yellow-orange color */
                font-weight: bold;
                text-shadow: 
                    3px 3px 6px rgba(0, 0, 0, 0.8), /* Consistent dark shadow */
                    0 0 15px #fdc74c; /* Yellow glow for highlight */
            }

            /* --- Spotlight Effect --- */
            .light-spot {
                position: absolute;
                top: -50px;
                left: 50%;
                transform: translateX(-50%);
                width: 250px; /* Larger spot */
                height: 180px; /* Taller spot */
                background: radial-gradient(ellipse at center,
                    rgba(255, 255, 255, 0.2) 0%, /* More intense light */
                    rgba(255, 255, 255, 0.1) 50%,
                    transparent 100%);
                border-radius: 50%;
                z-index: 1; /* Below text, above container background */
                animation: light-sway 6s ease-in-out infinite alternate;
            }
            
            @keyframes light-sway {
                0% { transform: translateX(-60%) skewX(-5deg); }
                100% { transform: translateX(-40%) skewX(5deg); }
            }
            
            /* --- Responsive Design Adjustments --- */
            @media (max-width: 768px) {
                .moviestar-title {
                    font-size: 7em;
                    letter-spacing: 8px;
                    text-shadow: 
                        4px 4px 0px #000000, 8px 8px 0px #000000, 12px 12px 0px #000000,
                        16px 16px 20px rgba(0, 0, 0, 0.7),
                        0 0 18px rgba(255, 255, 255, 0.8);
                }
                .moviestar-subtitle {
                    font-size: 2.2em;
                    letter-spacing: 5px;
                }
                .hollywood-container {
                    padding: 40px 15px;
                }
            }
            
            @media (max-width: 480px) {
                .moviestar-title {
                    font-size: 5.5em;
                    letter-spacing: 5px;
                    text-shadow: 
                        2px 2px 0px #000000, 4px 4px 0px #000000, 6px 6px 0px #000000,
                        8px 8px 15px rgba(0, 0, 0, 0.7);
                }
                .moviestar-subtitle {
                    font-size: 1.8em;
                    letter-spacing: 3px;
                }
            }
        </style>
    """, unsafe_allow_html=True)


# --- Main Page Function ---

def home_page():
    """
    Renders the main home page of the MovieStar application.
    Displays upcoming movies, genre selections, and top-rated films,
    with a Hollywood-themed title and background effects.
    """
    # Auto-refresh the page every 15 seconds
    st_autorefresh(interval=15 * 1000, limit=None, key="autorefresh_home")

    # Load external CSS for global styling
    load_css("style.css")  

    # Check for a movie parameter in the URL to display details page
    query_params = st.query_params
    movie_param = query_params.get("movie")

    if movie_param:
        show_movie_details(movie_param)
        return # Stop further rendering of the home page

    # Use a placeholder to ensure the page content refreshes cleanly
    placeholder = st.empty()

    with placeholder.container():
        # Apply the custom Hollywood-themed CSS styles
        apply_home_page_styles()
        
        # HTML structure for the starry background and the main title/subtitle container
        st.markdown(f'''
            <div class="stars">
                {''.join(['<div class="star"></div>' for _ in range(10)])}
            </div>
            <div class="hollywood-container">
                <div class="light-spot"></div>
                <h1 class="moviestar-title">🎬 MOVIESTAR 🎬</h1>
                <p class="moviestar-subtitle">★ <span class="yellow-text">AU CŒUR DE L'ACTU CINÉ CREUSOISE</span> ★</p>
            </div>
        ''', unsafe_allow_html=True)
        
        # --- Movie Data Loading and Validation ---
        # Validate that essential columns exist in the DataFrame
        missing_columns = [col for col in REQUIRED_FILM_COLUMNS if col not in films.columns]
        if missing_columns:
            st.error(f"Erreur: Les colonnes suivantes sont absentes du dataset 'films': {', '.join(missing_columns)}. Veuillez vérifier votre fichier 'recommendation.py'.")
            return

        # Convert release_date to datetime objects for date comparisons
        films['release_date'] = pd.to_datetime(films['release_date'], errors='coerce')


        # --- Movie Display Sections ---

        def display_movie_section(title_html: str, filtered_movies: pd.DataFrame):
            """
            Displays a section of movies in a horizontally arranged format.

            Args:
                title_html (str): The HTML string for the section title.
                filtered_movies (pd.DataFrame): DataFrame of movies to display in this section.
            """
            st.markdown(title_html, unsafe_allow_html=True)
            
            # Ensure there are enough movies to display, sample up to 5
            num_movies_to_display = min(len(filtered_movies), 5)
            
            if num_movies_to_display == 0:
                st.info("Aucun film trouvé pour cette catégorie.")
                return

            selected_movies = filtered_movies.sample(n=num_movies_to_display).copy()
            # Prepend the TMDB base URL to poster paths
            selected_movies['poster_path'] = TMDB_IMAGE_BASE_URL + selected_movies['poster_path'].astype(str)
            
            cols = st.columns(num_movies_to_display)
            for i, movie in enumerate(selected_movies.to_dict(orient='records')):
                with cols[i]:
                    st.markdown(
                        get_movie_card_html(movie),
                        unsafe_allow_html=True
                    )


        # Upcoming Movies Section
        st.markdown("<h2 style='color: #fff;'>À venir <span style='color:#fdc74c';>Prochainement</span></h2>", unsafe_allow_html=True)
        today = datetime.today()
        upcoming_movies = films[
            (films['release_date'].notna()) & # Ensure release date exists
            (films['release_date'] > today) & # After today
            (films['release_date'] <= today + timedelta(days=30)) & # Within next 30 days
            (films['poster_path'].notna()) # Has a poster
        ]
        if upcoming_movies.empty:
            st.warning("Aucun film prévu dans les 30 prochains jours.")
        else:
            display_movie_section("", upcoming_movies) # Title handled by markdown above


        # Drama Selection Section
        display_movie_section(
            "<h2 style='color: #fff;'>Notre sélection <span style='color:#fdc74c';>Drame</span></h2>",
            films[(films['vote_average'] > 8) & 
                  (films['poster_path'].notna()) &
                  (films['genres'].str.contains("Drame", case=False, na=False))]
        )

        # Comedy Selection Section
        display_movie_section(
            "<h2 style='color: #fff;'>Notre sélection <span style='color:#fdc74c';>Comédie</span></h2>",
            films[(films['vote_average'] > 8) & 
                  (films['poster_path'].notna()) &
                  (films['genres'].str.contains("Comédie", case=False, na=False))]
        )

        # Romance Selection Section
        display_movie_section(
            "<h2 style='color: #fff;'>Notre sélection <span style='color:#fdc74c';>Romance</span></h2>",
            films[(films['vote_average'] > 8) & 
                  (films['poster_path'].notna()) &
                  (films['genres'].str.contains("Romance", case=False, na=False))]
        )

        # Top Movies (> 9 rating) Section
        display_movie_section(
            "<h2 style='color: #fff;'>Notre sélection <span style='color:#fdc74c';>Divers</span></h2>",
            films[(films['vote_average'] > 9) & (films['poster_path'].notna())]
        )
