import ml_logic.roboflow_segmentation as roboflow_segmentation
import ml_logic.image_processing as image_processing
import ml_logic.OCR_processing as OCR_processing
import ml_logic.traductor_xml as traductor_xml
import os
import sys  # Importa sys para manejar argumentos de la línea de comando
import matplotlib.pyplot as plt
# from params import *  # Asegúrate de que cualquier parámetro necesario se maneje adecuadamente

if __name__ == '__main__':
    # Comprueba si se ha pasado una ruta de imagen como argumento
    if len(sys.argv) != 2:
        raise ValueError("Debe proporcionar una ruta de imagen como argumento")
    image_path = sys.argv[1]  # Usa el argumento proporcionado como la ruta de la imagen

    # Importar imagen usando el argumento proporcionado
    image = image_processing.cargar_imagen(image_path)

    # Procesamiento de la imagen
    image_info = roboflow_segmentation.infer_on_image(image)['predictions']
    bubbles = image_processing.extraer_burbujas(image, image_info)

    ### OCR Analysis
    text = [OCR_processing.ocr_bubble_text(bubble) for bubble in bubbles]

    for i, bubble in enumerate(bubbles):
        # Guarda el texto extraído en image_info
        image_info[i]['text'] = text[i]

        ### Traducción
        image_info[i]['translated_text'] = traductor_xml.traducir_elemento(image_info[i]['text'])

    ### Reinsersión de la imagen
    new_image = image_processing.image_reinsertion(image, image_info)

    # Guarda la imagen procesada de nuevo en una ruta que app.py espera
    processed_image_path = image_path.replace(".jpg", "_translated.jpg")
    new_image.save(processed_image_path)  # Asume que new_image es un objeto PIL Image
