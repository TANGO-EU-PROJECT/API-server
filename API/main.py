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


# Ruta de bienvenida
@app.route('/')
def index():
    return "Bienvenido a la API de recursos!"
    
    
# Endpoint para obtener la lista de todos los recursos
@app.route('/resource', methods=['GET'])
def get_resources():
    return jsonify({'response': resources}), 200

@app.route('/resource/<resource_type>', methods=['GET'])
def get_resource(resource_type):
    query_parameters = request.args  # Obtiene los parámetros de consulta

    # Extraer los parámetros de consulta
    sensor_name = query_parameters.get('sensor')
    unit = query_parameters.get('unit')
    min_value = query_parameters.get('min_value', type=float)  # Conversión a float
    max_value = query_parameters.get('max_value', type=float)  # Conversión a float
    min_time = query_parameters.get('min_time')  # Puede ser una cadena
    max_time = query_parameters.get('max_time')  # Puede ser una cadena

    # Validación del tipo de recurso
    sensors = {sensor_id: sensor for sensor_id, sensor in resources.items() if sensor['measure'] == resource_type}

    if not sensors:
        return jsonify({'response': 'No ' + resource_type + ' sensors found'}), 404

    # Aplicar filtros
    if sensor_name:
        sensors = {k: v for k, v in sensors.items() if k == sensor_name}

    if unit:
        sensors = {k: v for k, v in sensors.items() if v['unit'] == unit}

    if min_value is not None or max_value is not None or min_time or max_time:
        filtered_sensors = {}
        for k, v in sensors.items():
            # Filtrar valores dentro del rango especificado
            filtered_values = [
                value for value in v['values']
                if (min_value is None or value['value'] >= min_value) and
                   (max_value is None or value['value'] <= max_value) and
                   (min_time is None or datetime.fromisoformat(value['timestamp'][:-1]) >= datetime.fromisoformat(min_time[:-1])) and
                   (max_time is None or datetime.fromisoformat(value['timestamp'][:-1]) <= datetime.fromisoformat(max_time[:-1]))
            ]
            if filtered_values:
                filtered_sensors[k] = {
                    'measure': v['measure'],
                    'unit': v['unit'],
                    'values': filtered_values
                }
        sensors = filtered_sensors

    if not sensors:
        return jsonify({'response': 'No matching sensors found'}), 404

    return jsonify({'response': sensors}), 200



# Ruta para agregar un recurso, aceptando ambos métodos
@app.route('/resource', methods=['POST'])
def add_resource():
    # Si los datos vienen en formato JSON
    if request.is_json:
        data = request.get_json()
        sensor_name = data.get('sensor')
        unit = data.get('unit')
        measure = data.get('measure')
        values_param = data.get('values', [])  # Obtener los valores desde JSON como lista
    else:
        # Obtener parámetros de la URL (query parameters)
        sensor_name = request.args.get('sensor')
        unit = request.args.get('unit')
        measure = request.args.get('measure')
        values_param = request.args.getlist('values')  # Obtener múltiples valores como lista desde Query Params

    # Verificación de la existencia de todos los parámetros requeridos
    if not sensor_name or not unit or not measure or not values_param:
        return jsonify({'error': 'Missing required parameters'}), 400

    # Validación básica del nombre del sensor
    if not re.match("^[a-zA-Z0-9_]+$", sensor_name):
        return jsonify({'error': 'Bad request: Invalid sensor name'}), 400

    # Agregar el nuevo recurso a 'resources' si no existe
    if sensor_name not in resources:
        resources[sensor_name] = {'measure': measure, 'unit': unit, 'values': []}

    # Procesar valores desde JSON
    if isinstance(values_param, list) and isinstance(values_param[0], dict):
        # Si vienen en formato JSON
        for val in values_param:
            value = val.get('value')
            timestamp = val.get('timestamp', datetime.utcnow().isoformat() + 'Z')  # Añadir timestamp actual si no está
            resources[sensor_name]['values'].append({'value': value, 'timestamp': timestamp})
    else:
        # Procesar valores desde query parameters
        for val in values_param:
            try:
                if ',' in val:
                    value_str, timestamp = val.split(',')
                else:
                    value_str = val
                    timestamp = datetime.utcnow().isoformat() + 'Z'  # Si no hay timestamp, agregar la actual
                value = float(value_str)
            except ValueError:
                return jsonify({'error': 'Invalid value format'}), 400

            resources[sensor_name]['values'].append({'value': value, 'timestamp': timestamp})

    return jsonify({'response': f'Sensor {sensor_name} added successfully!', 'sensor': resources[sensor_name]}), 201
    

# Ejecutar la app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
