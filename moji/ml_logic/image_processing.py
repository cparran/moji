from inference_sdk import InferenceHTTPClient
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import textwrap

def cargar_imagen(image_path):
    return Image.open(image_path)

def inicializar_cliente(api_url, api_key):
    return InferenceHTTPClient(api_url=api_url, api_key=api_key)

def inferir_en_imagen(cliente, image_path, model_id):
    return cliente.infer(image_path, model_id=model_id)

def obtener_segmentos(result):
    return result['predictions']

def extraer_burbujas(img, info):

    burbujas = []

    for segment in info:

        x, y, w, h = segment['x'], segment['y'], segment['width'], segment['height']
        crop_img = img.crop((max(x - w / 2, 0), max(y - h / 2, 0), x + w / 2, y + h / 2))

        burbujas.append(crop_img)

    return burbujas

def ajustar_imagen_subgráfico(ax, segment, img, target_size, idx):
    x, y, w, h = segment['x'], segment['y'], segment['width'], segment['height']
    rect = patches.Rectangle((x - w / 2, y - h / 2), w, h, linewidth=2, edgecolor='none', facecolor='none')
    ax.add_patch(rect)

    crop_img = img.crop((max(x - w / 2, 0), max(y - h / 2, 0), x + w / 2, y + h / 2))
    crop_img_gray = crop_img.convert('L')
    crop_img_gray.thumbnail(target_size, Image.LANCZOS)

    green_fill = np.full((target_size[1], target_size[0], 3), 0, dtype=np.uint8)
    top_left_x = (target_size[0] - crop_img_gray.width) // 2
    top_left_y = (target_size[1] - crop_img_gray.height) // 2

    green_fill[top_left_y:top_left_y + crop_img_gray.height, top_left_x:top_left_x + crop_img_gray.width, 1] = np.array(crop_img_gray)
    ax.imshow(green_fill, cmap='gray')

    ax.set_title(f"Segmento {idx + 1}")
    ax.axis('off')

def mostrar_grid(fig, axes):
    fig.tight_layout()
    plt.show()

def plot_segments(image_path, num_cols=3, target_size=(200, 200), model_id=None, api_url=None, api_key=None):
    # Valores predeterminados
    defaults = {
        'model_id': "manga-text-detection/2",
        'api_url': "http://detect.roboflow.com",
        'api_key': "JVuvSUZ2T8BQEtoGVvtv"
    }

    # Utilizar valores predeterminados si no se proporcionan valores personalizados
    config = {key: value or defaults[key] for key, value in zip(['model_id', 'api_url', 'api_key'], [model_id, api_url, api_key])}

    # Resto del código sigue igual
    img = cargar_imagen(image_path)
    cliente = inicializar_cliente(config['api_url'], config['api_key'])
    result = inferir_en_imagen(cliente, image_path, config['model_id'])
    segments = obtener_segmentos(result)
    num_rows = int(np.ceil(len(segments) / num_cols))
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(100, 100))

    for idx, segment in enumerate(segments):
        row, col = divmod(idx, num_cols)
        ajustar_imagen_subgráfico(axes[row, col], segment, img, target_size, idx)

    mostrar_grid(fig, axes)

# # Ejemplo de uso
# # pip install inference-sdk numpy Pillow matplotlib
# image_path = "/home/carol/code/cparran/MOJI/raw_data/Nana v01/003.jpg"
# plot_segments(image_path)

def image_reinsertion(img, page_data, margin=0):

    draw = ImageDraw.Draw(img)

    #Se hace loop sobre ese numero de pagina en data

    for bubble in page_data:

        x = float(bubble['x'])
        y = float(bubble['y'])
        width = float(bubble['width'])
        height = float(bubble['height'])

        x1 = round(x - width / 2) + margin
        y1 = round(y - height / 2) + margin
        x2 = round(x + width / 2) - margin
        y2 = round(y + height / 2) - margin

        draw.rounded_rectangle([x1, y1, x2, y2], fill='white', radius=20 )

        font = ImageFont.load_default()
        spacing = 1
        translated_text = bubble['translated_text']

        wrapped_text = textwrap.fill(translated_text, width=15)

        draw.multiline_text([x1, y1, x2, y2], wrapped_text, fill="black", spacing=spacing, align="left",font_size=35)

    img.save('imagen_guardada.png')

    return img
