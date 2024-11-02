from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
app = Flask(__name__)

# Simulación de base de datos
usuarios = [
    {"id": 1, "nombre": "Juan"},
    {"id": 2, "nombre": "Ana"},
]

@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify({"data": usuarios})

@app.route('/api/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = next((u for u in usuarios if u["id"] == id), None)
    if usuario:
        return jsonify({"data": usuario})
    return jsonify({"error": "Usuario no encontrado"}), 404

if __name__ == '__main__':
    port = int(os.getenv('USERS_SERVICE_PORT', 5000))
    app.run(port=port, debug=True)