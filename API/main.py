from flask import Flask, jsonify, request, abort
import re

app = Flask(__name__)

# Simulación de recursos (puedes reemplazar esto con lógica para obtener datos reales)
resources = {
    'temperature': {'value': 22.5, 'unit': 'Celsius'},
    'humidity': {'value': 60, 'unit': '%'},
    'pressure': {'value': 1013, 'unit': 'hPa'}
}


# Ruta de bienvenida
@app.route('/')
def index():
    return "Bienvenido a la API de recursos!"

@app.route('/resource/<resource_type>', methods=['GET'])
def get_resource(resource_type):
    query_parameters = request.args  # Obtiene los parámetros de consulta
    # Aquí puedes procesar query_parameters según sea necesario
    
    # Validación del tipo de recurso
    if not re.match("^[a-zA-Z0-9_]+$", resource_type):
        return jsonify({'error': 'Bad request: Invalid resource type'}), 400

    resource_data = resources.get(resource_type)
    if resource_data:
        return jsonify({'response': resource_data}), 200
    else:
        return jsonify({'error': 'Resource not found'}), 404



# Ejecutar la app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
