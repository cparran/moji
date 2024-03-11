import streamlit as st
from PIL import Image
import subprocess
import tempfile

# Configuración de la página para un diseño minimalista
st.set_page_config(page_title="MOJI: Traductor de Manga", layout="centered")
st.title("Traductor de Manga")

# Instrucciones simples y claras
st.write("Carga un manga en japonés y obtén su versión en español.")

# Carga de imagen
uploaded_file = st.file_uploader("Cargar imagen", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Mostrar la imagen cargada
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_column_width=True)
    
    # Guardar la imagen cargada temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        image.save(tmp_file)
        tmp_file_path = tmp_file.name

    # Opcional: botón para iniciar la traducción manualmente si se requiere un procesamiento intensivo.
    if st.button('Traducir'):
        st.write("Procesando traducción...")
        # Llamar a main.py con el path de la imagen temporal como argumento
        process = subprocess.run(["python", "moji/main.py", tmp_file_path], capture_output=True, text=True)
        
        if process.returncode == 0:
            translated_image_path = tmp_file_path.replace(".jpg", "_translated.jpg")
            st.image(translated_image_path, caption="Imagen Traducida", use_column_width=True)
        else:
            st.error("Hubo un error en la traducción del manga.")
