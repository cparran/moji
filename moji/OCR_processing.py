from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from inference_sdk import InferenceHTTPClient
import requests
from io import BytesIO
from manga_ocr import MangaOcr


def ocr_bubble_text(image): ## Imagen en formato PIL.Image

    mocr = MangaOcr()

    # Realizar la operación de OCR en la imagen
    text = mocr(image)

    return text


# # URL de la imagen
# url = 'https://raw.githubusercontent.com/kha-white/manga-ocr/master/assets/examples/01.jpg'

# # Descargar la imagen desde la URL
# response = requests.get(url)
# img = Image.open(BytesIO(response.content))

# Realizar la operación de OCR en la imagen
# text = mocr(image)
# print(text)

###############################################################################

# Actualiza la ruta de la imagen
img_path = '/home/carol/code/cparran/MOJI/raw_data/0007.jpg'

# Carga la nueva imagen
img = Image.open(img_path)


# Inicializar el cliente
CLIENT = InferenceHTTPClient(
    api_url="http://detect.roboflow.com",
    api_key="JVuvSUZ2T8BQEtoGVvtv"
)

# Inferir en la imagen local
result = CLIENT.infer(img_path, model_id="manga-text-detection/2")

# Carga la imagen
img = Image.open(img_path)

# Segments
segments = result['predictions']

# Función para aplicar OCR a un segmento de imagen
def ocr_segment(image, segment):
    left = segment['x'] - segment['width'] / 2
    top = segment['y'] - segment['height'] / 2
    right = left + segment['width']
    bottom = top + segment['height']

    left = max(left, 0)
    top = max(top, 0)

    # Recorta y escala la imagen
    crop_img = image.crop((left, top, right, bottom)).convert('L')  # Convierte a escala de grises
    crop_img = crop_img.resize((int(crop_img.width * 2), int(crop_img.height * 2)), Image.LANCZOS)  # Usa Image.LANCZOS en lugar de Image.ANTIALIAS

    # Aplica binarización
    threshold = 128
    crop_img = crop_img.point(lambda p: p > threshold and 255)

    # Aplica OCR usando opciones optimizadas
    config = '--oem 3 --psm 6'
    text = pytesseract.image_to_string(crop_img, lang='jpn', config=config)

    return text.strip()

# Itera sobre los segmentos, aplica OCR y almacena el texto en cada segmento
fig, ax = plt.subplots(1)
ax.imshow(img)

for segment in segments:
    text = ocr_segment(img, segment)
    segment['text'] = text  # Almacenar el texto detectado en el segmento

    # Dibujar rectángulo alrededor del segmento
    x, y, w, h = segment['x'], segment['y'], segment['width'], segment['height']
    rect = patches.Rectangle((x - w / 2, y - h / 2), w, h, linewidth=2, edgecolor='r', facecolor='none')
    ax.add_patch(rect)

# Mostrar la imagen con los segmentos
# Mostrar la imagen en escala de grises
plt.imshow(img, cmap='gray')
plt.show()

# Imprimir el texto detectado y las coordenadas de cada segmento
for segment in segments:
    print(f"Texto: {segment['text']}, Coordenadas: ({segment['x']}, {segment['y']}, {segment['width']}, {segment['height']})")
