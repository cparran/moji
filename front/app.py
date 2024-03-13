import streamlit as st
from PIL import Image, ImageOps, ImageChops
import subprocess
import tempfile
import random
import os
import io

# Generar una clave única para el file_uploader
def generate_upload_key():
    return os.urandom(24).hex()

# Configuración de la página para un diseño minimalista
st.set_page_config(page_title="MOJI", layout="centered")

# Lista de URLs de las imágenes de fondo
background_images = [
    "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/02af675a-dd3b-47f2-84bf-8b87d6a5496e/dedisp4-fba6e176-04e3-4aed-a1c3-50c64b76be83.jpg/v1/fill/w_1192,h_670,q_70,strp/gojou_satoru_minimalism_wallpaper__ver__1_3__by_rkimx_dedisp4-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTA4MCIsInBhdGgiOiJcL2ZcLzAyYWY2NzVhLWRkM2ItNDdmMi04NGJmLThiODdkNmE1NDk2ZVwvZGVkaXNwNC1mYmE2ZTE3Ni0wNGUzLTRhZWQtYTFjMy01MGM2NGI3NmJlODMuanBnIiwid2lkdGgiOiI8PTE5MjAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.RkFwbKHMvCogd6R4NHlc3FHquma1qd28SkR-U9YZF2M",
    "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/b8cce1c9-38fb-49f0-ba0d-f48ec0394def/de84h55-ba6af665-58b9-44f7-9ba5-67795cfd39df.png/v1/fill/w_1192,h_670,q_70,strp/sukuna__jujutsu_kaisen__by_jiance_de84h55-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9Mzc1MCIsInBhdGgiOiJcL2ZcL2I4Y2NlMWM5LTM4ZmItNDlmMC1iYTBkLWY0OGVjMDM5NGRlZlwvZGU4NGg1NS1iYTZhZjY2NS01OGI5LTQ0ZjctOWJhNS02Nzc5NWNmZDM5ZGYucG5nIiwid2lkdGgiOiI8PTY2NjcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.Gyu7gidVFg1t68MenFlmlG02kNKXVGQDHG61I5_svmE",
    "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/02af675a-dd3b-47f2-84bf-8b87d6a5496e/delq7ir-9828ae46-251f-4afc-ade5-a193113e6cf9.jpg/v1/fill/w_1192,h_670,q_70,strp/kamado_nezuko_chan_minimalism_wallpaper_by_rkimx_delq7ir-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MjE2MCIsInBhdGgiOiJcL2ZcLzAyYWY2NzVhLWRkM2ItNDdmMi04NGJmLThiODdkNmE1NDk2ZVwvZGVscTdpci05ODI4YWU0Ni0yNTFmLTRhZmMtYWRlNS1hMTkzMTEzZTZjZjkuanBnIiwid2lkdGgiOiI8PTM4NDAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.G86NfySDt6ivEl4wZK7JKUTMxcun6cHgQ7KmKRdJ4F8",
    "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/02af675a-dd3b-47f2-84bf-8b87d6a5496e/de1110v-c45e4a82-9c04-422c-bada-e95698926011.jpg/v1/fill/w_1253,h_638,q_70,strp/mikasa_ackerman_minimalism_wallpaper_by_rkimx_de1110v-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9Njk2IiwicGF0aCI6IlwvZlwvMDJhZjY3NWEtZGQzYi00N2YyLTg0YmYtOGI4N2Q2YTU0OTZlXC9kZTExMTB2LWM0NWU0YTgyLTljMDQtNDIyYy1iYWRhLWU5NTY5ODkyNjAxMS5qcGciLCJ3aWR0aCI6Ijw9MTM2NiJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.IhlCl6EikR-6EzrsVy7L6wULO4kreU9KZnr0oMR6FDI",
    "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/02af675a-dd3b-47f2-84bf-8b87d6a5496e/depow31-44cecd43-0603-453d-980a-a4174770d1cf.jpg/v1/fill/w_1192,h_670,q_70,strp/luffy_d__monkey_minimalism_wallpaper_by_rkimx_depow31-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NzIwIiwicGF0aCI6IlwvZlwvMDJhZjY3NWEtZGQzYi00N2YyLTg0YmYtOGI4N2Q2YTU0OTZlXC9kZXBvdzMxLTQ0Y2VjZDQzLTA2MDMtNDUzZC05ODBhLWE0MTc0NzcwZDFjZi5qcGciLCJ3aWR0aCI6Ijw9MTI4MCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.s_ViDGQRazgeiga1LoWy-NYZoP1PqBtF3ueQQgX5wRg",
    # Añade tantas URLs como quieras
]

# Inicializa o recupera la imagen de fondo de la sesión
if 'selected_background' not in st.session_state:
    st.session_state.selected_background = random.choice(background_images)

# Añadiendo CSS para la imagen de fondo seleccionada y estilos adicionales
st.markdown(f"""
<style>
.stApp {{
    background-image: url({st.session_state.selected_background});
    background-size: cover;
}}
.text-background {{
    background-color: rgba(255, 255, 255, 0.8);  # Blanco con opacidad
    border-radius: 5px;
    padding: 10px;
    margin: 10px 0;
}}
.title-text {{
    font-size: 32px;
    font-weight: bold;
}}
.subtitle-text {{
    font-size: 20px;
}}
</style>
""", unsafe_allow_html=True)

# Textos y título
st.markdown('<div class="text-background title-text">Moji - Traductor de Manga</div>', unsafe_allow_html=True)
st.markdown('<div class="text-background subtitle-text">Carga una imagen de manga en japonés y obtén su versión en español.</div>', unsafe_allow_html=True)

# Inicializar o actualizar la clave de carga si es necesario
if 'upload_key' not in st.session_state or ('reset_uploader' in st.session_state and st.session_state.reset_uploader):
    st.session_state.upload_key = generate_upload_key()
    st.session_state.reset_uploader = False

uploaded_file = st.file_uploader("Cargar imagen", type=["png", "jpg", "jpeg"], key=st.session_state.upload_key)

# Crear un placeholder para la imagen
image_placeholder = st.empty()

if uploaded_file is not None:
    if 'translated_image' in st.session_state:
        # Limpiar la imagen traducida del estado si se carga una nueva imagen
        del st.session_state['translated_image']
        image_placeholder.empty()

    st.session_state.original_image = Image.open(uploaded_file)
    image_placeholder.image(st.session_state.original_image, caption="Imagen cargada", use_column_width=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        st.session_state.original_image.save(tmp_file)
        tmp_file_path = tmp_file.name
        st.session_state.tmp_file_path = tmp_file_path

if 'tmp_file_path' in st.session_state and st.button('Traducir'):
    with st.spinner('Procesando traducción...'):
        process = subprocess.run(["python", "moji/main.py", st.session_state.tmp_file_path], capture_output=True, text=True)

        if process.returncode == 0:
            translated_image_path = st.session_state.tmp_file_path.replace(".jpg", "_translated.jpg")
            if os.path.exists(translated_image_path):
                st.session_state.translated_image = Image.open(translated_image_path)
                st.session_state.reset_uploader = True  # Preparar para resetear la carga en la próxima interacción
            else:
                st.error("La imagen traducida no se encontró o no pudo ser creada.")
        else:
            st.error(f"Hubo un error en la traducción del manga: {process.stderr}")

# Muestra el slider y las imágenes solo si la traducción ha sido realizada
if 'translated_image' in st.session_state:
    reveal_factor = st.slider('Desliza para revelar la imagen original', 0, 100, 50)
    width, height = st.session_state.original_image.size
    reveal_width = int((width * reveal_factor) / 100)

    mask = Image.new("L", st.session_state.original_image.size, 0)
    mask.paste(255, (reveal_width, 0, width, height))
    composite_image = Image.composite(st.session_state.original_image, st.session_state.translated_image, mask)
    image_placeholder.image(composite_image, caption="Desliza para revelar la imagen original", use_column_width=True)

    img_buffer = io.BytesIO()
    st.session_state.translated_image.save(img_buffer, format='JPEG')
    img_buffer.seek(0)
    st.download_button("Descargar traducción", img_buffer, "translated_image.jpg", "image/jpeg")
