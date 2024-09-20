from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Simulando una base de datos simple en memoria
tasks = [
    {
        'id': 1,
        'title': 'Comprar comida',
        'description': 'Leche, Queso, Pan, Frutas',
        'done': False
    },
    {
        'id': 2,
        'title': 'Estudiar Flask',
        'description': 'Terminar el tutorial de Flask y hacer pruebas',
        'done': False
    }
]

# Ruta de bienvenida (raíz)
@app.route('/')
def index():
    return "Bienvenido a la API de tareas!"

# Obtener todas las tareas
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# Obtener una tarea específica por ID
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        abort(404)
    return jsonify({'task': task})

# Crear una nueva tarea
@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    
    new_task = {
        'id': tasks[-1]['id'] + 1 if tasks else 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(new_task)
    return jsonify({'task': new_task}), 201

# Actualizar una tarea existente
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        abort(404)
    
    if not request.json:
        abort(400)
    
    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task['done'] = request.json.get('done', task['done'])
    
    return jsonify({'task': task})

# Eliminar una tarea por ID
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        abort(404)
    
    tasks.remove(task)
    return jsonify({'result': True})

# Manejar errores personalizados
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

# Ejecutar la app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
