import streamlit as st
from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

import numpy as np
import tempfile

st.set_page_config(page_title="Brasil Relax Factory", layout="centered")
st.title("🇧🇷 Brasil Relax Factory V3 - Con Musica")
st.write("Ahora si con musica fuerte")

modo = st.selectbox("Modo", ["Brasil - Lluvia", "Brasil - Bosque", "Brasil - Neblina"])
musica = st.selectbox("Elige Musica", ["Lluvia Suave - FUERTE", "Bossa Nova - FUERTE", "Bosque Pajaros - FUERTE", "Sin musica"])

uploaded = st.file_uploader("Sube imagen de cabana", type=["jpg","jpeg","png"])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, use_container_width=True)
    st.success("Imagen lista")
    
    if st.button("Generar Video con Musica", use_container_width=True):
        try:
            from moviepy.editor import ImageClip, AudioClip
            duration = 8
            clip = ImageClip(np.array(img)).set_duration(duration).resize(height=720)
            
            sr = 44100
            if musica != "Sin musica":
                def make_audio(t):
                    # t puede ser array
                    if "Lluvia" in musica:
                        # Ruido blanco fuerte
                        return np.random.uniform(-0.5, 0.5, size=1) if np.isscalar(t) else np.random.uniform(-0.5, 0.5, size=(len(t),1))[:,0]
                    elif "Bossa" in musica:
                        # Acorde Bossa Nova fuerte 220Hz
                        vol = 0.6
                        if np.isscalar(t):
                            return vol * np.sin(2*np.pi*220*t) + vol*0.5*np.sin(2*np.pi*330*t)
                        else:
                            return vol * np.sin(2*np.pi*220*t) + vol*0.5*np.sin(2*np.pi*330*t)
                    else:
                        # Pajaros - tonos agudos
                        vol = 0.5
                        if np.isscalar(t):
                            return vol * np.sin(2*np.pi*800*t) * (1 if np.random.rand()>0.9 else 0.1)
                        else:
                            base = np.sin(2*np.pi*800*t)*0.1
                            base[::2000] = 0.8
                            return base
                
                audio = AudioClip(make_audio, duration=duration, fps=sr)
                clip = clip.set_audio(audio)
            
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            tmp.close()
            clip.write_videofile(tmp.name, fps=24, codec='libx264', audio_codec='aac', logger=None)
            
            st.success("¡Video Listo con Musica!")
            st.video(tmp.name)
            st.balloons()
            with open(tmp.name, "rb") as f:
                st.download_button("Descargar Video", f.read(), file_name="brasil_con_musica.mp4", mime="video/mp4", use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Sube una imagen para empezar")
