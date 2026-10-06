import streamlit as st
from PIL import Image
import numpy as np
import tempfile
import os

# Config
st.set_page_config(page_title="Brasil Relax Factory V2", layout="centered")

st.title("🇧🇷 Brasil Relax Factory")
st.write("Video + Música - V2")

# --- OPCIONES ---
modo = st.selectbox("Elige modo", ["Brasil - Lluvia", "Brasil - Bosque", "Brasil - Neblina"])

musica = st.selectbox("Elige música", [
    "Lluvia Suave (Generada)",
    "Bossa Nova Relax (Generada)", 
    "Bosque - Pájaros (Generada)",
    "Sin música",
    "Subir mi música MP3"
])

uploaded_img = st.file_uploader("Sube tu imagen de cabaña", type=["jpg","jpeg","png"])
uploaded_audio = None
if musica == "Subir mi música MP3":
    uploaded_audio = st.file_uploader("Sube tu MP3", type=["mp3","wav","ogg"])

# Mostrar imagen
if uploaded_img:
    img = Image.open(uploaded_img).convert("RGB")
    st.image(img, caption=f"Modo: {modo}", use_container_width=True)
    st.success("Imagen lista. Ahora genera el video con música abajo.")

    if st.button("🎬 Generar Video con Música", use_container_width=True):
        try:
            from moviepy.editor import ImageClip, AudioClip, AudioFileClip, CompositeAudioClip
            import moviepy.audio.fx.all as afx

            with st.spinner("Creando tu video con música... 20 seg..."):
                # 1. VIDEO - efecto zoom lento
                duration = 8  # segundos
                clip = ImageClip(np.array(img)).set_duration(duration)
               
