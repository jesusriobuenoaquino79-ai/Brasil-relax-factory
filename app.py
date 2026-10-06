import streamlit as st
from PIL import Image
import numpy as np
import tempfile

st.set_page_config(page_title="Brasil Relax Factory", layout="centered")
st.title("🇧🇷 Brasil Relax Factory V2")
st.write("Video con lluvia + música")

modo = st.selectbox("Modo", ["Brasil - Lluvia", "Brasil - Bosque", "Brasil - Neblina"])
musica = st.selectbox("Música", ["Lluvia Suave", "Bossa Nova", "Bosque Pajaros", "Sin música"])

uploaded = st.file_uploader("Sube imagen de cabaña", type=["jpg","jpeg","png"])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, use_container_width=True)
    st.success("Imagen lista")
    
    if st.button("Generar Video con Música", use_container_width=True):
        try:
            from moviepy.editor import ImageClip, AudioClip
            duration = 8
            # Video con zoom lento
            clip = ImageClip(np.array(img)).set_duration(duration)
            clip = clip.resize(height=720).resize(lambda t: 1 + 0.05*t)
            clip = clip.set_position("center")
            
            # Audio simple
            sr = 44100
            if musica == "Lluvia Suave":
                def make_audio(t):
                    return np.random.uniform(-0.1, 0.1)
                audio = AudioClip(lambda t: [make_audio(t)], duration=duration, fps=sr)
                clip = clip.set_audio(audio)
            elif musica == "Bossa Nova":
                def make_audio(t):
                    return 0.15 * np.sin(2 * 3.1416 * 220 * t)
                audio = AudioClip(lambda t: [make_audio(t)], duration=duration, fps=sr)
                clip = clip.set_audio(audio)
            elif musica == "Bosque Pajaros":
                def make_audio(t):
                    return np.random.uniform(-0.05, 0.05)
                audio = AudioClip(lambda t: [make_audio(t)], duration=duration, fps=sr)
                clip = clip.set_audio(audio)
            
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            tmp.close()
            clip.write_videofile(tmp.name, fps=24, codec='libx264', audio_codec='aac', logger=None)
            
            st.success("Listo!")
            st.video(tmp.name)
            with open(tmp.name, "rb") as f:
                st.download_button("Descargar Video", f.read(), file_name="brasil.mp4", mime="video/mp4", use_container_width=True)
                
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Sube una imagen para empezar")
