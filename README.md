# API-PDP
Pasos para levantar API en kubernetes.
  1. Crear nuestra API
  2. Establecer un Dockerfile para construir la imagen: docker build -t <nombre_imagen>:v1 .
  3. Ejecutar docker: docker run -d -p 5000:5000 <nombre_imagen>
  ---- KUBERNETES
  4. Subir la imagen a Dockerhub: docker push <tu_usuario_docker>/<nombre_imagen_flask>:v1
  5. Crear archivo deployment de kubernetes con su correspondiente pod y servicio
           -Si es en local establecer un nodeport junto con el targeport.
  6. Aplicar el deploy


Ejemplos:
  - GET basica, devuelve todas las temperaturas: http://127.0.0.1:5000/resource/temperature

  - GET con todos los queryParameters: http://127.0.0.1:5000/resource/temperature?min_value=20&max_value=23&sensor=sensor2&unit=Celsius&min_time=2024-09-09T12:00:00Z&max_time=2024-09-09T12:01:00Z

  - POST con queryParamaters: http://localhost:5000/resource?sensor=sensor7&unit=Celsius&measure=temperature&values=18.75,2024-10-02T14:00:00Z&values=19
  
  - POST con JSONbody: http://127.0.0.1:5000/resource + body:
{
    "sensor": "sensor8",
    "measure": "temperature",
    "unit": "Celsius",
    "values": [
        {"value": 21, "timestamp": "2024-09-09T12:34:56Z"},
        {"value": 23, "timestamp": "2024-09-09T12:35:56Z"},
        {"value": 25}
    ]
}
