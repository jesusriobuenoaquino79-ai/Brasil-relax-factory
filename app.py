import streamlit as st
from PIL import Image
import numpy as np
import tempfile

# Fix para Pillow
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import ImageClip, AudioFileClip, concatenate_audioclips

st.set_page_config(page_title="Brasil Relax Final", layout="centered")
st.title("🇧🇷 Brasil Relax - FINAL")
st.caption("Sube 5-6 Bossa Novas de 3 min = 18 min continuos sin loop corto")

duracion = st.slider("Duración video (segundos)", 8, 3600, 1200)
# 1200 = 20 min prueba, 3600 = 1 hora final

mp3s = st.file_uploader("1. SUBE 5-6 MP3 JUNTOS", type=["mp3","wav","m4a"], accept_multiple_files=True)
imagen = st.file_uploader("2. SUBE IMAGEN CABAÑA", type=["jpg","jpeg","png"])

if imagen:
    st.image(Image.open(imagen), use_container_width=True)
    
    if st.button("🚀 GENERAR VIDEO CONTINUO", type="primary", use_container_width=True):
        if not mp3s:
            st.error("Sube las músicas primero")
        else:
            with st.spinner(f"Pegando {len(mp3s)} canciones... tarda 2 min"):
                lista_audios = []
                for f in mp3s:
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    tmp.write(f.read())
                    tmp.close()
                    clip = AudioFileClip(tmp.name)
                    lista_audios.append(clip)
                
                # Pega una detrás de otra con 2 seg de cruce para que no se note el corte
                audio_unido = concatenate_audioclips(lista_audios, padding=-2)
                
                # Si pide
