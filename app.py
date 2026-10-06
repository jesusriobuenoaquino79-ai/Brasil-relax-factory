import streamlit as st
from PIL import Image
import numpy as np
import tempfile

if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import ImageClip, AudioFileClip, concatenate_audioclips

st.set_page_config(page_title="Brasil Relax Factory", layout="centered")
st.title("Brasil Relax - FABRICA CELULAR")

if 'lista' not in st.session_state:
    st.session_state.lista = []
if 'nombres' not in st.session_state:
    st.session_state.nombres = []
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

duracion = st.slider("Duracion del video (segundos)", 60, 3600, 1200)

# Este truco borra el archivo despues de agregarlo
mp3 = st.file_uploader("1. Sube 1 MP3", type=["mp3","wav","m4a","wma"], key=f"mp3_{st.session_state.uploader_key}")

c1, c2 = st.columns(2)
with c1:
    if st.button("AGREGAR CANCION", use_container_width=True):
        if mp3:
            t = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            t.write(mp3.read())
            t.close()
            st.session_state.lista.append(t.name)
            st.session_state.nombres.append(mp3.name)
            # Esto limpia el cargador para la siguiente cancion
            st.session_state.uploader_key += 1
            st.rerun()
        else:
            st.warning("Selecciona un MP3 primero")
with c2:
    if st.button("BORRAR TODO", use_container_width=True):
        st.session_state.lista = []
        st.session_state.nombres = []
        st.session_state.uploader_key += 1
        st.rerun()

st.write("Total guardadas:")
st.write(len(st.session_state.lista))

# Aqui ves que canciones ya agregaste
if len(st.session_state.nombres) > 0:
    st.write("Canciones agregadas:")
    for i, nom in enumerate(st.session_state.nombres, 1):
        st.write(f"{i}. {nom}")

imagen = st.file_uploader("2. Sube la imagen", type=["jpg","jpeg","png"])

if imagen:
    st.image(Image.open(imagen), use_container_width=True)
    if st.button("GENERAR VIDEO FINAL", type="primary", use_container_width=True):
        if len(st.session_state.lista) == 0:
            st.error("Agrega al menos 1 cancion")
        else:
            with st.spinner("Creando video, espera 2 minutos..."):
                audios = [AudioFileClip(p) for p in st.session_state.lista]
                audio_unido = concatenate_audioclips(audios, padding=-2)
                if audio_unido.duration < duracion:
                    audio_final = audio_unido.loop(duration=duracion)
                else:
                    audio_final = audio_unido.subclip(0, duracion)
                img = Image.open(imagen).convert("RGB")
                video = ImageClip(np.array(img)).set_duration(duracion).resize(height=720).set_audio(audio_final)
                salida = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
                video.write_videofile(salida, fps=24, codec='libx264', audio_codec='aac', logger=None)
                st.success("VIDEO LISTO")
                st.video(salida)
                with open(salida, "rb") as f:
                    st.download_button("DESCARGAR VIDEO", f.read(), file_name="Brasil_Relax_1_Hora.mp4", use_container_width=True)
