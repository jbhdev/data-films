import streamlit as st
from utils.css_loader import load_css
from recommendation import get_recommendations_by_title, recommend_by_actors, films, get_film_index_by_title

def select_movie(title):
    """Met à jour le film sélectionné et recharge la page."""
    st.session_state.selected_movie = title
    st.experimental_rerun()

def movie_detail_page():
    load_css("movie_style.css")  # Charge le CSS spécifique à cette page

    st.markdown("<h1 style='text-align: center; color: #fff;'>Détails du Film</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Choisir un film depuis le dataset
    selected_movie = st.selectbox("Choisissez un film :", sorted(films["original_title"].dropna().unique()))

    # Initialiser l'état d'affichage de la bande-annonce
    if "show_trailer" not in st.session_state:
        st.session_state.show_trailer = False

    # Si un film est sélectionné
    if selected_movie:
        movie_data = films[films["original_title"] == selected_movie].iloc[0]
        trailer_url = movie_data.get('trailer_url')

        # Affichage des infos du film sélectionné
        st.markdown(
            f"""
            <div class="movie-header">
                <img src="{movie_data.get('poster_url', 'https://placehold.co/300x450?text=No+Image')}" width="300" height="450">
                <div class="movie-details">
                    <h1>{selected_movie}</h1>
                    <p>{movie_data.get('startYear', 'Année inconnue')} || {movie_data.get('genres', 'Genre inconnu')} || {movie_data.get('runtimeMinutes', 'Durée inconnue')} min</p>
                    <p>{movie_data.get('overview', 'Pas de description disponible.')}</p>
                    <p>Avec : {movie_data.get('acteurs_1', 'Acteurs inconnus')}, {movie_data.get('acteurs_2', 'Acteurs inconnus')}, {movie_data.get('actrices', 'Acteurs inconnus')}</p>
                    <p>Réalisateur : {movie_data.get('realisateurs', 'Realisateur inconnu')}</p>
                    <div class="movie-actions">
                        <button>🎬 Lancer</button>
                        <button>➕ Ajouter à ma liste</button>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Bouton toggle pour afficher la bande-annonce
        if st.button("🎞️ Voir la bande-annonce" if not st.session_state.show_trailer else "❌ Cacher la bande-annonce"):
            st.session_state.show_trailer = not st.session_state.show_trailer

        # Affichage de la bande-annonce si activée
        if st.session_state.show_trailer and trailer_url:
            if "watch?v=" in trailer_url:
                youtube_id = trailer_url.split("watch?v=")[-1]
            elif "youtu.be/" in trailer_url:
                youtube_id = trailer_url.split("youtu.be/")[-1]
            else:
                youtube_id = None

            if youtube_id:
                st.markdown(
                    f"""
                    <div style="position: relative; padding-bottom: 56.25%; height: 0; margin-top: 20px;">
                        <iframe src="https://www.youtube.com/embed/{youtube_id}" 
                                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
                                frameborder="0" allowfullscreen>
                        </iframe>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Recommandations basées sur le contenu
        st.markdown("<h2 style='color: #fff;'>Titres similaires</h2>", unsafe_allow_html=True)
        recommendations = get_recommendations_by_title(selected_movie, n=5)
        if not recommendations.empty:
            cols = st.columns(len(recommendations))
            for i, (_, row) in enumerate(recommendations.iterrows()):
                with cols[i]:
                    st.image(row.get("poster_url", "https://placehold.co/400x500?text=No+Image"), use_container_width=True)
                    st.markdown(
                        f"<p style='color: #fff; font-weight: bold; font-size: 14px;'>{row['original_title']}</p>",
                        unsafe_allow_html=True
                    )

        # Recommandations basées sur les acteurs
        st.markdown("<h2 style='color: #fff;'>Autres films avec vos acteurs préférés</h2>", unsafe_allow_html=True)
        index = get_film_index_by_title(selected_movie)
        actor_recs = recommend_by_actors(index=index, top_n=5)
        if not actor_recs.empty:
            cols = st.columns(len(actor_recs))
            for i, (_, row) in enumerate(actor_recs.iterrows()):
                with cols[i]:
                    st.image(row.get("poster_url", "https://placehold.co/400x500?text=No+Image"), use_container_width=True)
                    st.markdown(
                        f"<p style='color: #fff; font-weight: bold; font-size: 14px;'>{row['original_title']}</p>",
                        unsafe_allow_html=True
                    )
        else:
            st.info("Aucune recommandation disponible pour ce film.")
            