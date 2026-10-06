import streamlit as st
from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS
import numpy as np, tempfile
from moviepy.editor import ImageClip, AudioFileClip

st.set_page_config(page_title="Brasil Relax 1 HORA", layout="centered")
st.title("🇧🇷 Brasil Relax - 1 HORA REAL")

duracion = st.slider("Duración del video (segundos)", 8, 3600, 60, help="8=prueba, 3600=1 hora")
st.write(f"Vas a generar: {duracion//60} minutos y {duracion%60} segundos")

mp3 = st.file_uploader("SUBE AQUÍ TU MP3 REAL (Bossa Nova o Lluvia de 1 hora)", type=["mp3","wav","m4a"])
imagen = st.file_uploader("Sube imagen cabaña", type=["jpg","jpeg","png"])

if imagen:
    img = Image.open(imagen).convert("RGB")
    st.image(img, caption="Imagen para video 1 hora", use_container_width=True)
    if st.button("GENERAR VIDEO 1 HORA", use_container_width=True):
        if not mp3:
            st.error("¡Primero sube el MP3! Sin MP3 no hay música real.")
        else:
            try:
                with st.spinner(f"Generando {duracion//60} min... espera"):
                    tmp_a = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    tmp_a.write(mp3.read()); tmp_a.close()
                    audio = AudioFileClip(tmp_a.name).set_duration(duracion)
                    if audio.duration < duracion:
                        audio = audio.loop(duration=duracion)
                    
                    clip = ImageClip(np.array(img)).set_duration(duracion).resize(height=720).set_audio(audio)
                    tmp_v = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                    tmp_v.close()
                    clip.write_videofile(tmp_v.name, fps=24, codec='libx264', audio_codec='aac', logger=None)
                    st.success("¡VIDEO DE 1 HORA LISTO!")
                    st.video(tmp_v.name)
                    with open(tmp_v.name, "rb") as f:
                        st.download_button("DESCARGAR VIDEO 1 HORA", f.read(), file_name=f"brasil_{duracion}s.mp4", mime="video/mp4", use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
