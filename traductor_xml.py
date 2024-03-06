from xml.etree import ElementTree as ET
from deep_translator import GoogleTranslator
import html
import os
from concurrent.futures import ThreadPoolExecutor

def traducir_archivo_xml(xml_path):
    # Inicializa el traductor
    traductor = GoogleTranslator(source='ja', target='es')

    # Cargar el archivo XML
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Función para manejar la traducción de un elemento
    def traducir_elemento(texto_japones):
        if texto_japones:
            texto_traducido = traductor.translate(texto_japones)
            if texto_traducido:
                return html.unescape(texto_traducido)
        return "Texto no disponible"
    
    # Recoger todos los textos japoneses
    textos_japoneses = [elemento.text.strip() for elemento in root.findall('.//text') if elemento.text.strip()]

    # Traducir los textos de manera concurrente
    with ThreadPoolExecutor(max_workers=10) as executor:
        textos_traducidos = list(executor.map(traducir_elemento, textos_japoneses))

    # Actualizar el XML con los textos traducidos
    for elemento, texto_traducido in zip(root.findall('.//text'), textos_traducidos):
        elemento.set('translated_text', texto_traducido)
    
    # Generar el nombre del archivo de salida con el sufijo "-es"
    file_name = os.path.splitext(os.path.basename(xml_path))[0]
    output_file_name = f"{file_name}-es.xml"

    # Guardar el archivo XML modificado
    tree.write(output_file_name, encoding="utf-8", xml_declaration=True)
    print(f"Archivo traducido guardado como: {output_file_name}")