from PIL import Image
# import pytesseract
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
