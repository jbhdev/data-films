# 🎬 Moviestar App

![Moviestar Logo](streamlit_app/assets/moviestar2.png)



Bienvenue dans **Moviestar App**, une application web de recommandation de films basée sur des algorithmes de machine learning. Ce projet a pour objectif d'offrir une expérience personnalisée aux utilisateurs en leur suggérant des films en fonction de leurs préférences et de leur historique.

## 🚀 Fonctionnalités

- Recommandation de films personnalisée
- Système de filtrage collaboratif et/ou basé sur le contenu
- Interface utilisateur intuitive
- Possibilité de noter des films
- Historique des films consultés
- Backend alimenté par des modèles de machine learning

## 🧠 Algorithmes ML utilisés


- **Filtrage collaboratif** (Collaborative Filtering)
- **Filtrage basé sur le contenu** (Content-Based Filtering)
- **Hybrid Approach** (optionnel)
- Réduction de dimension (ex : PCA, SVD)
- Clustering (ex : KMeans, DBSCAN pour le profilage utilisateur)

## 🛠️ Technologies

- **Frontend** : Streamlit / HTML/CSS
- **Backend** : Python (Pandas/ Numpy)
- **Machine Learning** : Scikit-learn, Pandas, NumPy, Surprise
- **Base de données** : PostgreSQL / SQLite / MongoDB
- **Déploiement** : Docker, Heroku, Vercel, etc.

## ⚙️ Installation

1. **Cloner le dépôt** :

   ```bash
   git clone https://github.com/jbhdev/data-films.git
   
## Données compressées
Ces fichiers .pkl.gz sont utilisés pour le système de recommandation :
- `processed_films_compressed.pkl.gz` : Données transformées pour KNN.
- `nn_model_compressed.pkl.gz` : Modèle KNN entraîné.
- `nn_distances_compressed.pkl.gz` : Distances et indices pré-calculés.

⚠️ Ces fichiers ont été compressés pour rester en dessous de 100 Mo.