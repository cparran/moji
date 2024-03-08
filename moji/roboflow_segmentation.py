from inference_sdk import InferenceHTTPClient

def infer_on_image(image_path):
    # Configuración fija
    model_id = "manga-text-detection/2"
    api_url = "http://detect.roboflow.com"
    api_key = "JVuvSUZ2T8BQEtoGVvtv"

    # Inicializar el cliente
    CLIENT = InferenceHTTPClient(
        api_url=api_url,
        api_key=api_key
    )

    # Inferir en la imagen especificada con el model_id dado
    result = CLIENT.infer(image_path, model_id)

    return result

# Ejemplo de uso de la función
# ! pip install inference-sdk
# from roboflow_segmentation import infer_on_image
image_path = "/home/carol/code/cparran/MOJI/raw_data/Nana v01/003.jpg"
result = infer_on_image(image_path)
print(result)