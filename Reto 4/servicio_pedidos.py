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

pedidos = [
    {"id": 1, "usuario_id": 1, "producto": "Laptop", "cantidad": 1},
    {"id": 2, "usuario_id": 2, "producto": "Monitor", "cantidad": 2}
]

def verificar_usuario(usuario_id):
    try:
        response = requests.get(f'http://localhost:{configuracion["USERS_SERVICE_PORT"]}/api/usuarios/{usuario_id}')
        return response.status_code == 200
    except Exception as e:
        print(f"Error al verificar usuario: {e}")
        return False

@app.route('/api/pedidos', methods=['GET'])
def obtener_pedidos():
    return jsonify(pedidos)

@app.route('/api/pedidos', methods=['POST'])
def crear_pedido():
    nuevo_pedido = request.json
    if verificar_usuario(nuevo_pedido['usuario_id']):
        pedidos.append(nuevo_pedido)
        return jsonify(nuevo_pedido), 201
    return jsonify({"error": "Usuario no encontrado"}), 404

if __name__ == '__main__':
    port = int(os.getenv('ORDERS_SERVICE_PORT', 5001))
    app.run(port=port, debug=True)