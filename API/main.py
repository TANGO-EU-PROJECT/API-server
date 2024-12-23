from flask import Flask, jsonify, request, abort
import re
from datetime import datetime

app = Flask(__name__)

# Simulación de recursos (puedes reemplazar esto con lógica para obtener datos reales)
resources = {
    'sensor1': {
        'measure': 'temperature',
        'unit': 'Celsius',
        'values': [
            {'value': 5, 'timestamp': '2024-09-09T12:00:00Z'},
            {'value': 10.5, 'timestamp': '2024-09-09T12:01:00Z'},
            {'value': 10, 'timestamp': '2024-09-09T12:02:00Z'},
            {'value': 21, 'timestamp': '2024-09-09T12:03:00Z'},
            {'value': 23, 'timestamp': '2024-09-09T12:04:00Z'},
            {'value': 25, 'timestamp': '2024-09-09T12:05:00Z'},
            {'value': 28, 'timestamp': '2024-09-09T12:06:00Z'},
            {'value': 27, 'timestamp': '2024-09-09T12:07:00Z'},
            {'value': 40, 'timestamp': '2024-09-09T12:08:00Z'}
        ]
    },
    'sensor2': {
        'measure': 'temperature',
        'unit': 'Celsius',
        'values': [
            {'value': 10, 'timestamp': '2024-09-09T12:00:00Z'},
            {'value': 20, 'timestamp': '2024-09-09T12:01:00Z'},
            {'value': 25, 'timestamp': '2024-09-09T12:02:00Z'},
            {'value': 40, 'timestamp': '2024-09-09T12:03:00Z'}
        ]
    },
    'sensor3': {
        'measure': 'humidity',
        'unit': '%',
        'values': [
            {'value': 60, 'timestamp': '2024-09-09T12:00:00Z'}
        ]
    },
    'sensor4': {
        'measure': 'pressure',
        'unit': 'hPa',
        'values': [
            {'value': 10.5, 'timestamp': '2024-09-09T12:00:00Z'},
            {'value': 10, 'timestamp': '2024-09-09T12:01:00Z'}
        ]
    }
}

# Mapa de acceso (ID, ROLE, ACTION -> Resources)
access_map = {
    ("user123", "employee", "GET"): ["/temperature", "/humidity"],
    ("user456", "leader", "POST"): ["/temperature", "/humidity", "/pressure"]
}


# Ruta de bienvenida
@app.route('/')
def index():
    return "Bienvenido a la API de recursos!"

# Verificar acceso basado en el mapa
def check_access(user_id, role, action, resource):
    if not user_id or not role:
        # Si no hay usuario o rol, denegar acceso
        return False
    allowed_resources = access_map.get((user_id, role, action), [])
    return f"/{resource}" in allowed_resources



# Endpoint para agregar un nuevo permiso
@app.route('/add_permission', methods=['POST'])
def add_permission():
    try:
        data = request.json
        user_id = data['user_id']
        role = data['role']
        action = data['action']
        resources = data['resources']

        # Crear la nueva clave en el access_map
        key = (user_id, role, action)
        if key in access_map:
            # Si la clave ya existe, agregamos los recursos si no están presentes
            access_map[key].extend([r for r in resources if r not in access_map[key]])
        else:
            # Si la clave no existe, la creamos
            access_map[key] = resources
        
        return jsonify({"message": "Permission added successfully"}), 201
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/access_map', methods=['GET'])
def get_access_map():
    # Convertir las claves de las tuplas a cadenas para que sean serializables
    serializable_map = {}
    for key, resources in access_map.items():
        serializable_map[str(key)] = resources
    return jsonify(serializable_map)

# Endpoint para obtener recursos
@app.route('/resource/<resource_type>', methods=['GET'])
def get_resource(resource_type):
    user_id = request.args.get('id')
    role = request.args.get('role')

    auth = 0  # Suponemos que el acceso no es autorizado al principio

    # Si se proporcionan los parámetros id y role, validamos el acceso
    if user_id and role:
        if not check_access(user_id, role, "GET", resource_type):
            return jsonify({'error': f'Unauthorized access for role {role} on resource {resource_type}'}), 403
        auth = 1  # Si pasa la validación, establecemos auth a 1

    # Si no se proporciona id ni role, seguimos adelante (sin validación de permisos)
    if (auth == 1) or (not user_id and not role):

        # Obtener sensores del tipo solicitado
        sensors = {k: v for k, v in resources.items() if v['measure'] == resource_type}
        if not sensors:
            return jsonify({'response': f'No {resource_type} sensors found'}), 404

        return jsonify({'response': sensors}), 200
    
    return jsonify({'error': 'Bad request'}), 400





# Endpoint para agregar un recurso
@app.route('/resource/<resource_type>', methods=['POST'])
def add_resource(resource_type):
    user_id = request.args.get('id')
    role = request.args.get('role')

    auth = 0  # Suponemos que el acceso no es autorizado al principio
    # Si se proporcionan los parámetros id y role, validamos el acceso
    if user_id and role:
        if not check_access(user_id, role, "POST", resource_type):
            return jsonify({'error': f'Unauthorized access for role {role} on resource {resource_type}'}), 403
        auth = 1  # Si pasa la validación, establecemos auth a 1

    # Si no se proporciona id ni role, seguimos adelante (sin validación de permisos)
    if (auth == 1) or (not user_id and not role):

        # Verificar que el cuerpo de la solicitud contenga datos válidos
        if not request.is_json:
            return jsonify({'error': 'Request body must be JSON'}), 400

        data = request.get_json()
        sensor = data.get('sensor')
        measure = data.get('measure')
        unit = data.get('unit')
        values = data.get('values', [])

        # Validar campos obligatorios
        if not sensor or not measure or not unit:
            return jsonify({'error': 'Missing required fields: sensor, measure, or unit'}), 400

        # Verificar que el sensor no exista ya
        if sensor in resources:
            return jsonify({'error': f'Sensor {sensor} already exists'}), 409

        # Agregar el nuevo recurso
        resources[sensor] = {
            'measure': measure,
            'unit': unit,
            'values': values
        }

        return jsonify({'response': f'Sensor {sensor} added successfully'}), 201
    
    # Si no se cumplen las condiciones de autorización, se retorna un error de solicitud incorrecta
    return jsonify({'error': 'Bad request'}), 400

# Ejecutar la app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)