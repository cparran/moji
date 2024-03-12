from inference_sdk import InferenceHTTPClient

def infer_on_image(image):
    # Configuración fija
    model_id = "manga-text-detection/2"
    api_url = "https://detect.roboflow.com"
    api_key = "JVuvSUZ2T8BQEtoGVvtv"

    # Inicializar el cliente
    CLIENT = InferenceHTTPClient(
        api_url=api_url,
        api_key=api_key
    )

    # Inferir en la imagen especificada con el model_id dado
    result = CLIENT.infer(image, model_id)

    return result

# # Ejemplo de uso de la función
# # ! pip install inference-sdk
# # from roboflow_segmentation import infer_on_image
#image_path = "/Users/sarancibia/Downloads/Made in Abyss/Made in Abyss v01/CCF_0017.jpg"
#result = infer_on_image(image_path)
#print(result)
