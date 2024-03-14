from fastapi import FastAPI, File, UploadFile
from typing import Optional
from PIL import Image
import io
import time
from fastapi.responses import StreamingResponse

import moji.ml_logic.roboflow_segmentation as roboflow_segmentation
import moji.ml_logic.image_processing as image_processing
import moji.ml_logic.OCR_processing as OCR_processing
import moji.ml_logic.traductor_xml as traductor_xml

app = FastAPI()

@app.on_event("startup")
def load_models():
    # Aquí, en lugar de cargar modelos reales, simplemente asignaremos los módulos importados
    # al estado de la aplicación para usarlos más adelante.
    app.state.model = {
        'roboflow_segmentation': roboflow_segmentation,
        'image_processing': image_processing,
        'OCR_processing': OCR_processing,
        'traductor_xml': traductor_xml
    }

@app.get("/")
async def root():
    # Mensaje de bienvenida
    return {"message": "Welcome to the MOJI API"}

def process_image(image: Image.Image) -> Image.Image:
    # Utiliza los módulos/modelos desde el estado de la app para procesar la imagen
    image_info = app.state.model['roboflow_segmentation'].infer_on_image(image)['predictions']
    bubbles = app.state.model['image_processing'].extraer_burbujas(image, image_info)

    for i, bubble in enumerate(bubbles):
        text = app.state.model['OCR_processing'].ocr_bubble_text(bubble)
        image_info[i]['text'] = text

        translated_text = app.state.model['traductor_xml'].traducir_elemento(text)
        image_info[i]['translated_text'] = translated_text

    new_image = app.state.model['image_processing'].image_reinsertion(image, image_info)
    return new_image

@app.post("/process-image/", response_class=StreamingResponse)
async def create_upload_file(file: UploadFile = File(...)):
    start_time = time.time()  # Comenzar a medir el tiempo
    contents = await file.read()
    image_stream = io.BytesIO(contents)
    image = Image.open(image_stream)

    processed_image = process_image(image)
    image_stream.close()

    # Convertir la imagen procesada a bytes y prepararla para la respuesta
    img_io = io.BytesIO()
    processed_image.save(img_io, format='JPEG')
    img_io.seek(0)  # Retrocede al inicio del stream
    
    processing_time = time.time() - start_time

    # Devuelve la imagen procesada directamente
    return StreamingResponse(img_io, media_type="image/jpeg")
