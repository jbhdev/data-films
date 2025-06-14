import streamlit as st
import os
from PIL import Image

def show_stats_page():
    st.title("📊 Statistiques des films")
    
    # Chemin vers le dossier des images de statistiques
    stats_dir = os.path.join(os.path.dirname(__file__), "assets/stats")
    
    
    
    # Vérifier si le dossier existe, sinon le créer
    if not os.path.exists(stats_dir):
        os.makedirs(stats_dir)
        st.warning(f"Le dossier {stats_dir} a été créé, mais il est vide. Ajoutez des images pour afficher des statistiques.")
        return
        
        # Lister tous les fichiers du dossier
    try:
        stat_files = [f for f in os.listdir(stats_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        if not stat_files:
            st.warning("Aucune image trouvée dans le dossier des statistiques.")
            return
        
        # Afficher chaque image
        for stat_file in sorted(stat_files):
            try:
                image_path = os.path.join(stats_dir, stat_file)
                image = Image.open(image_path)
                
                # Afficher le nom du fichier comme sous-titre avec uniquement la première lettre en majuscule
                subtitle = stat_file.replace('.png', '').replace('_', ' ').casefold()
                if subtitle:
                    subtitle = subtitle[0].upper() + subtitle[1:]
                st.subheader(subtitle)
                st.image(image, use_container_width=True)
                st.markdown("---")  # Ligne de séparation
                
            except Exception as e:
                st.error(f"Erreur lors du chargement de l'image {stat_file}: {e}")
    
    except Exception as e:
        st.error(f"Erreur lors de la lecture du dossier des statistiques: {e}")

if __name__ == "__main__":
    show_stats_page()
