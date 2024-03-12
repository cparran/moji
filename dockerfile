# Utilizar una imagen base de Python
FROM python:3.10.6

# Establecer el directorio de trabajo en el contenedor
WORKDIR /moji

# Copiar los archivos requeridos al contenedor
COPY requirements.txt ./requirements.txt
# Instalar las dependencias
RUN pip install -r requirements.txt

# Copiar repositorio
COPY moji moji

# Copiar setup.py
COPY setup.py ./setup.py

# Instalar proyecto localmente
RUN pip install .

# Comando para ejecutar la aplicación al iniciar el contenedor
CMD uvicorn main_api:app --host 0.0.0.0 --port $PORT
