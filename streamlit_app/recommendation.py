# recommendation.py

import pandas as pd
import joblib
import os
from utils.css_loader import load_css
from sklearn.neighbors import NearestNeighbors
from IPython.display import display, HTML
import unicodedata
import re



# Fonction pour normaliser les titres sinon le film n'est pas affoché
def normalize_title(title):
    if not isinstance(title, str):
        return ""
    # Enlever les accents
    #title = unicodedata.normalize('NFD', title).encode('ascii', 'ignore').decode('utf-8')

    # Remplacer tirets et underscore par espaces
    title = title.replace("&", "et")
    # Nettoyer espaces multiples
    title = re.sub(r'\s+', ' ', title).strip()
    return title

# Chargement des fichiers nécessaires
films = pd.read_csv('../datasets/raw/films.csv')
films['original_title'] = films['original_title'].fillna('').apply(normalize_title)
films["release_date"] = pd.to_datetime(films["release_date"], errors="coerce")


df_processed = joblib.load('datasets/raw/processed_films.pkl')
nn_model = joblib.load('datasets/raw/nn_model.pkl')
distances_all, indices_all = joblib.load('datasets/raw/nn_distances.pkl')

# ----------------------------------------------------------------------

# Fonction pour compléter l'URL des posters

def get_full_poster_url(path):
    load_css("movie_style.css")
    if pd.notna(path) and path != '':
        return f"https://image.tmdb.org/t/p/w185{path}"
    return "https://via.placeholder.com/185x278?text=No+Image"

# Fonction d'affichage HTML (Notebook)
def display_posters_with_names(names, poster_paths, title=""): 
    html = f"<h3>{title}</h3><div style='display:flex; gap:20px;'>"
    for name, path in zip(names, poster_paths):
        poster_url = get_full_poster_url(path)
        html += f"""
            <div style='text-align:center;'>
                <img src='{poster_url}' style='width:120px; height:auto; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.3);'><br>
                <span style='font-size:14px;'>{name}</span>
            </div>
        """
    html += "</div>"
    display(HTML(html))

# ----------------------------------------------------------------------

## Fonctions

def get_film_index_by_title(title: str):
    try:
        return films[films["original_title"] == title].index[0]
    except IndexError:
        return None

def get_recommendations_by_title(title: str, n=5, **filters) -> pd.DataFrame:
    idx = get_film_index_by_title(title)
    if idx is None:
        return pd.DataFrame()

    distances = distances_all[idx][:n+1]
    indices = indices_all[idx][:n+1]

    recs = films.iloc[indices].copy()
    recs["distance"] = distances
    recs = recs[recs["original_title"] != title]

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

    for col in ['acteurs_1', 'acteurs_2', 'actrices']:
        original_data[col] = original_data[col].fillna('').astype(str).str.strip().str.title()

    film_ref = original_data.iloc[int(index)]
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

    # Affichage des acteurs du film de référence
    names = [film_ref['acteurs_1'], film_ref['acteurs_2'], film_ref['actrices']]
    posters = [film_ref.get('actors_1_posters', ''), film_ref.get('actors_2_posters', ''), film_ref.get('actresse_1_posters', '')]
    display_posters_with_names(names, posters, title="Acteurs du film")

    return filtered[["original_title", "popularity", "runtimeMinutes", "poster_url"]].head(top_n)

def recommend_similar_items(index: int, n_neighbors: int = 5) -> pd.DataFrame:
    distances, indices = nn_model.kneighbors(df_processed[index].reshape(1, -1), n_neighbors=n_neighbors)
    recs = films.iloc[indices[0]].copy()
    recs["distance"] = distances[0]
    return recs


def normalize_name(name):
    return name.strip().lower() \
        .replace("é", "e").replace("è", "e") \
        .replace("-", " ").replace("_", " ") \
        .replace("ê", "e").replace("ô", "o")

def get_films_by_actor(actor_name: str, original_data: pd.DataFrame = films) -> pd.DataFrame:
    # Normaliser les colonnes d'acteurs
    for col in ['acteurs_1', 'acteurs_2', 'actrices']:
        original_data[col] = original_data[col].fillna('').astype(str).apply(normalize_name)

    actor_name_normalized = normalize_name(actor_name)

    filtered = original_data[
        (original_data['acteurs_1'] == actor_name_normalized) |
        (original_data['acteurs_2'] == actor_name_normalized) |
        (original_data['actrices'] == actor_name_normalized)
    ]

    return filtered[['original_title', 'poster_url', 'vote_average']]
