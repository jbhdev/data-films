import streamlit as st
import os

def load_css(file_name):
        """
        Loads CSS from a given file and injects it into the Streamlit app.
        Assumes CSS files are in the 'css' directory relative to the project root.
        """
        css_path = os.path.join("css", file_name)
        try:
            with open(css_path) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.error(f"Error: The CSS file '{css_path}' was not found. Make sure it's in the 'css' directory.")
        except Exception as e:
            st.error(f"An error occurred while loading CSS from '{css_path}': {e}")
    