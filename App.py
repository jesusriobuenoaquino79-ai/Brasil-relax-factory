import streamlit as st
st.title("Brasil Relax Factory - Video con Movimiento")
st.write("Fabrica de videos para Brasil y Vikingo - 1 app para todo")

modo = st.selectbox("Elige modo", ["Brasil - Lluvia", "Vikingo - Nieve y Fuego", "Base - Solo Zoom"])

uploaded_image = st.file_uploader("Sube tu imagen de cabaña", type=["jpg","png"])

if uploaded_image:
    st.image(uploaded_image, caption=f"Modo: {modo}")
    st.success("Imagen lista. El motor de zoom lento se activará al generar.")
