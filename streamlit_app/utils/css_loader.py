import streamlit as st
import os

def load_css(file_name):
    """
    Loads CSS from a given file, testing multiple possible paths.
    """
    # Obtenir le répertoire de ce fichier
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Tester plusieurs chemins possibles
    possible_paths = [
        # Depuis utils/ vers ../css/
        os.path.join(os.path.dirname(current_dir), "css", file_name),
        # Depuis la racine du projet
        os.path.join("css", file_name),
        # Chemin absolu depuis streamlit_app
        os.path.join(os.path.dirname(current_dir), "css", file_name),
        # Au cas où on serait dans un autre répertoire
        os.path.join("streamlit_app", "css", file_name)
    ]
    
    css_loaded = False
    
    for css_path in possible_paths:
        try:
            if os.path.exists(css_path):
                with open(css_path, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                    st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
                print(f"✅ CSS chargé depuis: {css_path}")
                css_loaded = True
                break
        except Exception as e:
            continue
    
    if not css_loaded:
        st.error(f"❌ Impossible de charger le fichier CSS '{file_name}'")
        st.error("Chemins testés:")
        for path in possible_paths:
            st.error(f"  - {path}")
        
        # Afficher la structure actuelle pour debug
        st.error("Structure du répertoire courant:")
        try:
            for root, dirs, files in os.walk(os.getcwd()):
                level = root.replace(os.getcwd(), '').count(os.sep)
                indent = ' ' * 2 * level
                st.error(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    st.error(f"{subindent}{file}")
                if level > 3:  # Limiter la profondeur
                    break
        except:
            pass
