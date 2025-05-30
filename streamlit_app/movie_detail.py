import streamlit as st
from utils.css_loader import load_css

def movie_detail_page():
        """
        Displays the movie detail page content.
        """
        load_css("movie_style.css") # Load specific CSS for this page

        st.markdown("<h1 style='text-align: center; color: #fff;'>Movie Details</h1>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="movie-header">
                <img src="https://i.pinimg.com/1200x/c0/37/40/c03740709286733cfce2f0e805147138.jpg" width="300" height="450"; height:auto; border-radius:12px;">
                <div class="movie-details">
                    <h1>MULAN</h1>
                    <p>12+ HD CC AD | 2020 - 1h 59 min | Drama, Action and adventure</p>
                    <p>
                        In China, a young woman takes all risks and becomes a legendary warrior.
                    </p>
                    <div class="movie-actions">
                        <button>PLAY</button>
                        <button>TRAILER</button>
                        <button>+</button>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<h2 style='color: #fff;'>Suggestions</h2>", unsafe_allow_html=True)
        

        suggestions = [
            {"title": "DEADPOOL AND WOLVERINE", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/6ce1f5bd-92aa-4d3b-83d7-1d72c0fd3859/compose?format=webp&label=poster_vertical_080&width=800"},
            {"title": "INDIANA JONES", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/bc756a67-89b8-471f-8056-c52ad3804b97/compose?format=webp&label=poster_vertical_080&width=800"},
            {"title": "BREF 2", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/f9fd76f4-72be-4d04-9007-5c7da732913b/compose?format=webp&label=poster_vertical_star-original_080&width=800"},
            {"title": "SHOGUN", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/cae42e93-635b-438b-a67a-776348546a7e/compose?format=webp&label=poster_vertical_star-original_080&width=800"},
            {"title": "PARADISE", "image": "https://disney.images.edge.bamgrid.com/ripcut-delivery/v2/variant/disney/790c8f5b-d6c1-4238-b75f-47838546a897/compose?format=webp&label=poster_vertical_star-original_080&width=800"},
        ]

        # Create a single row of 5 columns for suggestions
        cols_suggestions = st.columns(5) # Assuming always 5 suggestions for a single row

        for i, suggestion in enumerate(suggestions):
            with cols_suggestions[i]:
                st.image(suggestion["image"], use_container_width=True)
                st.markdown(
                    f"""
                    <p style='color: #fff; font-weight: bold; margin-bottom: 2px; font-size: 14px;'>{suggestion["title"]}</p>
                    """,
                    unsafe_allow_html=True
                )
