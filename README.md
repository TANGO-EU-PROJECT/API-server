# API-PDP
Pasos para levantar API en kubernetes.
  1. Crear nuestra API
  2. Establecer un Dockerfile para construir la imagen: docker build -t <tu_usuario_docker>/<nombre_imagen_flask>:v1 .
  3. Subir la imagen a Dockerhub
  4. Crear archivo deployment de kubernetes con su correspondiente pod y servicio
  5. Aplicar el deploy
  6. Si es en local establecer un nodeport
