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


@app.route('/resource', methods=['POST'])
@app.route('/resource', methods=['POST'])
def add_resource():
    try:
        data = request.get_json()  # Intenta obtener el JSON
        if not data:
            return jsonify({'error': 'Bad request: No JSON body provided'}), 400
    except Exception as e:
        return jsonify({'error': 'Bad request: Invalid JSON format', 'message': str(e)}), 400


    # Iterar sobre los elementos en el JSON para agregarlos a resources
    for resource_type, resource_data in data.items():
        # Validación básica de nombres de recursos
        if not re.match("^[a-zA-Z0-9_]+$", resource_type):
            return jsonify({'error': f'Bad request: Invalid resource type {resource_type}'}), 400
        
        # Validación del formato de los valores del recurso
        if 'value' not in resource_data or 'unit' not in resource_data:
            return jsonify({'error': 'Missing value or unit in resource data'}), 400

        # Añadir el nuevo recurso o actualizar uno existente
        resources[resource_type] = {'value': resource_data['value'], 'unit': resource_data['unit']}
    
    return jsonify({'response': resources}), 201

# Ejecutar la app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
