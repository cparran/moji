import ml_logic.roboflow_segmentation as roboflow_segmentation
import ml_logic.image_processing as image_processing
import ml_logic.OCR_processing as OCR_processing
import ml_logic.traductor_xml as traductor_xml
import os
import matplotlib.pyplot as plt
from params import *

if __name__ == '__main__':

    ## Importar imagen
    PATH = "/Users/sarancibia/Downloads/Made in Abyss/Made in Abyss v01/CCF_0058.jpg"
    #PATH = "/Users/sarancibia/code/sarabarancibiag/Images-MOJI/images/GinNoChimera/015.jpg"
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
