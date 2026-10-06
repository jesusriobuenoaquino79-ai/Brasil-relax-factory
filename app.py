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
    st.session_state.lista=[]
if 'nombres' not in st.session_state:
    st.session_state.nombres=[]
if 'key' not in st.session_state:
    st.session_state.key=0

duracion=st.slider("Duracion del video",60,3600,1200)
mp3=st.file_uploader("1. Sube 1 MP3",type=["mp3","wav","m4a","wma"],key=f"mp3_{st.session_state.key}")

if st.button("AGREGAR CANCION"):
    if mp3:
        t=tempfile.NamedTemporaryFile(delete=False,suffix=".mp3")
        t.write(mp3.read())
        t.close()
        st.session_state.lista.append(t.name)
        st.session_state.nombres.append(mp3.name)
        st.session_state.key+=1
        st.rerun()

if st.button("BORRAR TODO"):
    st.session_state.lista=[]
    st.session_state.nombres=[]
    st.session_state.key+=1
    st.rerun()

st.write(f"Total: {len(st.session_state.lista)}")
for i,n in enumerate(st.session_state.nombres,1):
    st.write(f"{i}. {n}")

imagen=st.file_uploader("2. Sube imagen",type=["jpg","jpeg","png"])

if imagen:
    st.image(Image.open(imagen),use_container_width=True)
    if st.button("GENERAR VIDEO FINAL",type="primary"):
        if len(st.session_state.lista)==0:
            st.error("Agrega canciones")
        else:
            with st.spinner("Creando video..."):
                audios=[AudioFileClip(p) for p in st.session_state.lista]
                if len(audios)==1:
                    audio_unido=audios[0]
                else:
                    audio_unido=concatenate_audioclips(audios)
                if audio_unido.duration < duracion:
                    veces=int(duracion//audio_unido.duration)+1
                    audio_largo=concatenate_audioclips([audio_unido]*veces)
                    if hasattr(audio_largo,'subclipped'):
                        audio_final=audio_largo.subclipped(0,duracion)
                    else:
                        audio_final=audio_largo.subclip(0,duracion)
                else:
                    if hasattr(audio_unido,'subclipped'):
                        audio_final=audio_unido.subclipped(0,duracion)
                    else:
                        audio_final=audio_unido.subclip(0,duracion)
                img=Image.open(imagen).convert("RGB")
                video=ImageClip(np.array(img)).set_duration(duracion).resize(height=720).set_audio(audio_final)
                salida=tempfile.NamedTemporaryFile(delete=False,suffix=".mp4").name
                video.write_videofile(salida,fps=24,codec='libx264',audio_codec='aac',logger=None)
                st.success("VIDEO LISTO!")
                st.video(salida)
                with open(salida,"rb") as f:
                    st.download_button("DESCARGAR VIDEO",f.read(),file_name="Brasil_Relax.mp4")
