# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /webscraping-markets-col

# Copia los archivos del proyecto al contenedor
COPY . /webscraping-markets-col

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Define el comando por defecto para ejecutar el script
CMD ["python", "src/batch/run_all_batches.py"]
