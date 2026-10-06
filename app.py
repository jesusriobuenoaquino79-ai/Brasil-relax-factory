import streamlit as st
from PIL import Image
import numpy as np
import tempfile

# Arreglo para que no falle en celular
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import ImageClip, AudioFileClip, concatenate_audioclips

st.set_page_config(page_title="Brasil Relax Factory", layout="centered")
st.title("🇧🇷 Brasil Relax - FABRICA CELULAR")
st.write("Sube las canciones de 1 en 1")

# Memoria para guardar las canciones
if 'lista' not in st.session_state:
    st.session_state.lista = []

duracion = st.slider("Duración del video (segundos)", 60, 3600, 1200)

# Subir canciones
mp3 = st.file_uploader("1. Sube 1 MP3 y dale a AGREGAR", type=["mp3","wav","m4a","wma"])

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ AGREGAR CANCIÓN", use_container_width=True):
        if mp3:
            t = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            t.write(mp3.read())
            t.close()
            st.session_state.lista.append(t.name)
            st.success(f"¡Agregada! L
