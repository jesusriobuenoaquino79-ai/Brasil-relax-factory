import streamlit as st
from PIL import Image

def apply_motion_mode(image, mode):
    if mode == "Brasil - Lluvia":
        st.info("🌧️ Aplicando: Zoom lento + Lluvia + Luz cálida")
    elif mode == "Vikingo - Nieve y Fuego":
        st.info("❄️🔥 Aplicando: Zoom lento + Nieve + Humo + Fuego de chimenea")
    else:
        st.info("🎥 Aplicando: Solo Zoom lento")
    return image
