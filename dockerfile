# Utilizar una imagen base de Python
FROM python:3.10.6

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos requeridos al contenedor
COPY requirements.txt ./requirements.txt
COPY app.py ./app.py
# Si tienes más archivos o directorios necesarios para tu aplicación, inclúyelos aquí
# COPY directory_or_file ./directory_or_file

# Instalar las dependencias
RUN pip install -r requirements.txt

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8501

# Comando para ejecutar la aplicación al iniciar el contenedor
CMD ["streamlit", "run", "app.py"]
