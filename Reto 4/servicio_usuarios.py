from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import requests

# Cargar variables de entorno
load_dotenv()
app = Flask(__name__)

# Función para obtener configuración
def obtener_configuracion():
    response = requests.get('http://localhost:5002/api/configuracion')
    if response.status_code == 200:
        return response.json()['data']
    return {}

# Obtener configuración
configuracion = obtener_configuracion()

# Simulación de base de datos
usuarios = [
    {"id": 1, "nombre": "Juan"},
    {"id": 2, "nombre": "Ana"}
]

@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify(usuarios)

@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
    if usuario:
        return jsonify(usuario)
    return jsonify({"error": "Usuario no encontrado"}), 404

if __name__ == '__main__':
    port = int(os.getenv('USERS_SERVICE_PORT', 5000))
    app.run(port=port, debug=True)