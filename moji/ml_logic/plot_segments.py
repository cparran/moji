import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
from inference_sdk import InferenceHTTPClient

def plot_segments(image_path, num_cols=3, target_size=(100, 100)):
    # Configurar los valores fijos
    model_id = "manga-text-detection/2"  # Reemplaza con tu modelo_id
    api_url = "http://detect.roboflow.com"  # Reemplaza con tu api_url
    api_key = "JVuvSUZ2T8BQEtoGVvtv"  # Reemplaza con tu api_key

    # Cargar la imagen
    img = Image.open(image_path)

    # Inicializar el cliente
    CLIENT = InferenceHTTPClient(api_url=api_url, api_key=api_key)

    # Inferir en la imagen local
    result = CLIENT.infer(image_path, model_id=model_id)

    # Obtener los segmentos del resultado
    segments = result['predictions']

    # Calcular el número de filas necesario en función del número de segmentos y el número de columnas
    num_rows = int(np.ceil(len(segments) / num_cols))

    # Crear el grid de subgráficos
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 15))

    # Iterar sobre los segmentos y asignar cada uno a un subgráfico
    for idx, segment in enumerate(segments):
        row = idx // num_cols
        col = idx % num_cols
        ax = axes[row, col]

        # Dibujar rectángulo alrededor del segmento
        x, y, w, h = segment['x'], segment['y'], segment['width'], segment['height']
        rect = patches.Rectangle((x - w / 2, y - h / 2), w, h, linewidth=2, edgecolor='none', facecolor='none')
        ax.add_patch(rect)

        # Recorta la imagen al cuadro delimitador ajustado
        crop_img = img.crop((max(x - w / 2, 0), max(y - h / 2, 0), x + w / 2, y + h / 2))

        # Convierte la imagen recortada a escala de grises
        crop_img_gray = crop_img.convert('L')

        # Redimensiona la imagen recortada sin deformar (manteniendo el aspecto original)
        crop_img_gray.thumbnail(target_size, Image.LANCZOS)

        # Crea una matriz de relleno verde
        green_fill = np.full((target_size[1], target_size[0], 3), 0, dtype=np.uint8)

        # Obtén las coordenadas para insertar la imagen recortada en el centro del área de relleno verde
        top_left_x = (target_size[0] - crop_img_gray.width) // 2
        top_left_y = (target_size[1] - crop_img_gray.height) // 2

        # Inserta la imagen recortada en el área de relleno verde
        green_fill[top_left_y:top_left_y + crop_img_gray.height, top_left_x:top_left_x + crop_img_gray.width, 1] = np.array(crop_img_gray)

        # Muestra la imagen recortada y redimensionada en escala de grises con relleno verde en el subgráfico
        ax.imshow(green_fill, cmap='gray')

        # Ajusta el aspecto del subgráfico
        ax.set_title(f"Segmento {idx + 1}")
        ax.axis('off')

    # Ajusta el diseño de la figura y muestra la cuadrícula de subgráficos
    plt.tight_layout()
    plt.show()