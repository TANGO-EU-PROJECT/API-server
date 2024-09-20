# Imagen base con Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requisitos (si tienes uno)
COPY requirements.txt /app/requirements.txt

# Instalar las dependencias
RUN pip install -r requirements.txt

# Copiar el archivo main.py de la API
COPY main.py /app/

# Exponer el puerto que utilizará la aplicación Flask
EXPOSE 5000

# Comando para ejecutar la API Flask
CMD ["python", "main.py"]

