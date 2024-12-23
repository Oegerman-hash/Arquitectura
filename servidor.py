from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# Diccionario de usuarios con contraseñas 
users = {
    "admin": generate_password_hash("password123")
}

# Función para verificar las credenciales
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return users
    return False

# Base de datos simulada
base_datos = {
    "usuarios": [
        {"id": 1, "nombre": "Fabian"},
        {"id": 2, "nombre": "Pedro"}
    ]
}

# Ruta para obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
@auth.login_required
def obtener_usuarios():
    return jsonify(base_datos["usuarios"])

# Ruta para crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
@auth.login_required
def crear_usuario():
    nuevo_usuario = request.json
    if 'id' not in nuevo_usuario or 'nombre' not in nuevo_usuario:
        return jsonify({"error": "Datos inválidos"}), 400  # Código de error 400
    base_datos["usuarios"].append(nuevo_usuario)
    return jsonify(nuevo_usuario), 201  # Devuelve el nuevo usuario y un código de estado 201

# Ruta para obtener un usuario por ID
@app.route('/usuarios/<int:id>', methods=['GET'])
@auth.login_required
def obtener_usuario_por_id(id):
    usuario = next((u for u in base_datos["usuarios"] if u["id"] == id), None)
    if usuario:
        return jsonify(usuario)
    return jsonify({"error": "Usuario no encontrado"}), 404  # Código de error 404

# Ruta para eliminar un usuario por ID
@app.route('/usuarios/<int:id>', methods=['DELETE'])
@auth.login_required
def eliminar_usuario(id):
    global base_datos
    base_datos["usuarios"] = [u for u in base_datos["usuarios"] if u["id"] != id]
    return jsonify({"mensaje": "Usuario eliminado"}), 204  # Código de éxito 204

if __name__ == '__main__':
    app.run(port=5000)  # Ejecuta el servidor en el puerto 5000
