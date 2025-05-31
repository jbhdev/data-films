# recommendation.py

import pandas as pd
import joblib
from sklearn.neighbors import NearestNeighbors

# Chargement des fichiers nécessaires
films = pd.read_csv("C:/Users/sirnb/OneDrive/Bureau/WildCode/Projets/Projet_2_App/Scripts/datasets/raw/films.csv")  # Mets à jour le bon chemin
df_processed = joblib.load("C:/Users/sirnb/OneDrive/Bureau/WildCode/Projets/Projet_2_App/Scripts/datasets/raw/processed_films.pkl")
nn_model = joblib.load("C:/Users/sirnb/OneDrive/Bureau/WildCode/Projets/Projet_2_App/Scripts/datasets/raw/nn_model.pkl")
distances_all, indices_all = joblib.load("C:/Users/sirnb/OneDrive/Bureau/WildCode/Projets/Projet_2_App/Scripts/datasets/raw/nn_distances.pkl")

films['poster_path'] = films['poster_path'].fillna('')
films['poster_url'] = "https://image.tmdb.org/t/p/w500" + films['poster_path']


def get_film_index_by_title(title: str):
    """Trouve l'index du film dans la base originale à partir du titre."""
    try:
        return films[films["original_title"] == title].index[0]
    except IndexError:
        return None


def get_recommendations_by_title(title: str, n=5, **filters) -> pd.DataFrame:
    """Renvoie les recommandations d’un film donné selon le modèle KNN."""
    idx = get_film_index_by_title(title)
    if idx is None:
        return pd.DataFrame()

    distances = distances_all[idx][:n+1]
    indices = indices_all[idx][:n+1]

    recs = films.iloc[indices].copy()
    recs["distance"] = distances
    recs = recs[recs["original_title"] != title]  # Retirer le film lui-même

    # Filtres optionnels
    if "min_popularity" in filters:
        recs = recs[recs["popularity"] >= filters["min_popularity"]]
    if "runtime_range" in filters:
        min_r, max_r = filters["runtime_range"]
        recs = recs[recs["runtimeMinutes"].between(min_r, max_r)]
    if "sort_by" in filters and filters["sort_by"] in recs.columns:
        recs = recs.sort_values(by=filters["sort_by"], ascending=False)

    return recs[["original_title", "popularity", "runtimeMinutes", "distance", "poster_url"]]

def recommend_by_actors(index: int,
                        original_data: pd.DataFrame = films,
                        min_popularity: float = None,
                        decade: str = None,
                        sort_by: str = 'popularity',
                        top_n: int = 10) -> pd.DataFrame:
    """Recommande des films avec au moins un acteur ou actrice en commun."""

    # Nettoyage
    for col in ['acteurs_1', 'acteurs_2', 'actrices']:
        original_data[col] = original_data[col].fillna('').astype(str).str.strip().str.title()

    film_ref = original_data.iloc[index]
    acteurs_ref = set([
        film_ref['acteurs_1'],
        film_ref['acteurs_2'],
        film_ref['actrices']
    ])

    def has_common_actor(row):
        acteurs_row = set([
            row['acteurs_1'],
            row['acteurs_2'],
            row['actrices']
        ])
        return not acteurs_ref.isdisjoint(acteurs_row)

    filtered = original_data[original_data.index != index]
    filtered = filtered[filtered.apply(has_common_actor, axis=1)]

    if min_popularity is not None:
        filtered = filtered[filtered['popularity'] >= min_popularity]

    if decade is not None:
        filtered = filtered[filtered['decennie'] == decade]

    if sort_by and sort_by in filtered.columns:
        filtered = filtered.sort_values(by=sort_by, ascending=False)

    # Retourne les colonnes utiles
    return filtered[["original_title", "popularity", "runtimeMinutes", "poster_url"]].head(top_n)

def recommend_similar_items(index: int, n_neighbors: int = 5) -> pd.DataFrame:
    """Recommande des films similaires."""
    distances, indices = nn_model.kneighbors(df_processed[index].reshape(1, -1), n_neighbors=n_neighbors)
    recs = films.iloc[indices[0]]
    recs["distance"] = distances[0]
    return recs

