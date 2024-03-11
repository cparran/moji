import roboflow_segmentation
import image_processing
import OCR_processing
import traductor_xml
import os
from params import *
import sys
from PIL import Image
import tempfile
import matplotlib.pyplot as plt

if __name__ == '__main__':

    ## Importar imagen
    

    if __name__ == '__main__':
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

            PATH = tmp_file_path  # Tomar la ruta de la imagen cargada temporalmente
            image = image_processing.cargar_imagen(PATH)
            ## Extraer bubbles
            image_info = roboflow_segmentation.infer_on_image(image)['predictions']
            bubbles = image_processing.extraer_burbujas(image, image_info)
            # fig, axs = plt.subplots(1, 6)
            # for i, bubble in enumerate(bubbles[:6]):
            #     axs[i].imshow(bubble)
            # plt.show()
            ### OCR Analysis
            text = [OCR_processing.ocr_bubble_text(bubble) for bubble in bubbles]
            for i, bubble in enumerate(bubbles):
                #Save Text
                image_info[i]['text'] = text[i]
                ### Translator
                image_info[i]['translated_text'] = traductor_xml.traducir_elemento(image_info[i]['text'])
            ### Image Reinsertion
            new_image = image_processing.image_reinsertion(image, image_info)
            