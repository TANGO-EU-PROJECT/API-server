# API-PDP
Pasos para levantar API en kubernetes.
  1. Crear nuestra API
  2. Establecer un Dockerfile para construir la imagen: docker build -t <nombre_imagen>:v1 .
  3. Subir la imagen a Dockerhub: docker push <tu_usuario_docker>/<nombre_imagen_flask>:v1
  4. Crear archivo deployment de kubernetes con su correspondiente pod y servicio
           -Si es en local establecer un nodeport junto con el targeport.
  6. Aplicar el deploy

Ejemplo de solicitud GET: http://192.168.161.135:30080/resource/humidity

Ejemplo de body POST:
	- {"solar_radiation": {"value": 500, "unit": "W/m²"}}
	- {"wind_speed": {"value": 12.5, "unit": "m/s"}}
	- {"solar_radiation": {"value": 500, "unit": "W/m²"}}
	- {"co2_concentration": {"value": 415, "unit": "ppm"}}
	- {"water_ph": {"value": 7.2, "unit": "pH"}}
	- {"rain_intensity": {"value": 15, "unit": "mm/h"}}
