import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'datasets', 'raw')
file_path = os.path.join(DATA_PATH, 'films.csv')

print("Chemin attendu :", file_path)
print("Existe :", os.path.exists(file_path))

# Si le fichier existe, essaye de le lire
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    print("Chargement OK, nombre de lignes :", len(df))
else:
    print("❌ Le fichier est introuvable.")
