import streamlit as st
from PIL import Image
# Fix para Pillow nuevo
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

import numpy as np
import tempfile
from moviepy.editor import ImageClip, AudioFileClip, concatenate_audioclips
from moviepy.audio.fx.all import audio_fadein, audio_fadeout

st.set_page_config(page_title="Brasil Relax Final", layout="centered")

st.title("🇧🇷 Brasil Relax - FINAL CONTINUO")
st.caption("Sube 5-6 Bossa Novas de 3 min y las pega en 18 min continuos sin loop corto")

# Controles
duracion = st.slider("Duración del video final (segundos)", 8, 3600, 1200, help="1200 = 20 minutos. 3600 = 1 hora")
crossfade = 3

col1, col2 = st.columns(2)
with col1:
    mp3s = st.file_uploader("1. SUBE LAS 5-6 MP3 AQUÍ", type=["mp3","wav","m4a"], accept_multiple_files=True)
with col2:
    imagen = st.file_uploader("2. SUBE IMAGEN CABAÑA", type=["jpg","jpeg","png"])

if imagen:
    st.image(Image.open(imagen), caption="Imagen usada", use_container_width=True)

    if st.button("🚀 GENERAR VIDEO FINAL", type="primary", use_container_width=True):
        if not mp3s:
            st.error("¡Falta subir las músicas!")
        else:
            with st.spinner(f"Armando {len(mp3s)} canciones con pegado suave... puede tardar 2-4 min"):
                try:
                    audios_procesados = []
                    temp_paths = []
                    for f in mp3s:
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                        tmp.write(f.read())
                        tmp.close()
                        temp_paths.append(tmp.name)
                        clip = AudioFileClip(tmp.name)
                        # Fade suave para que no haya golpe
                        clip = clip.fx(audio_fadein, 1).fx(audio_fadeout, 1)
                        audios_procesados.append(clip)

                    # Pega con overlap de 3 segundos para que no se note el corte
                    audio_unido = concatenate_audioclips(audios_procesados, padding=-crossfade)
                    
                    # Si pide más tiempo que lo que tenemos, loopea el bloque grande (18 min) no 1 canción
                    if audio_unido.duration < duracion:
                        audio_final = audio_unido.loop(duration=duracion)
                    else:
                        audio_final = audio_unido.subclip(0, duracion)

                    img = Image.open(imagen).convert("RGB")
                    video = ImageClip(np.array(img)).set_duration(duracion).resize(height=720).set_audio(audio_final)

                    out
