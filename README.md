# API-PDP
Pasos para levantar API en kubernetes.
  1. Crear nuestra API
  2. Establecer un Dockerfile para construir la imagen: docker build -t <nombre_imagen>:v1 .
  3. Subir la imagen a Dockerhub: docker push <tu_usuario_docker>/<nombre_imagen_flask>:v1
  4. Crear archivo deployment de kubernetes con su correspondiente pod y servicio
           -Si es en local establecer un nodeport junto con el targeport.
  6. Aplicar el deploy

Ejemplo de solicitud: http://192.168.161.135:30080
