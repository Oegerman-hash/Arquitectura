(servicio_pedidos.py)
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
app = Flask(__name__)

# Simulación de base de datos
pedidos = [
    {"id": 1, "usuario_id": 1, "producto": "Laptop"},
    {"id": 2, "usuario_id": 2, "producto": "Teléfono"},
]

@app.route('/api/pedidos', methods=['GET'])
def obtener_pedidos():
    return jsonify({"data": pedidos})

@app.route('/api/pedidos/<int:id>', methods=['GET'])
def obtener_pedido(id):
    pedido = next((p for p in pedidos if p["id"] == id), None)
    if pedido:
        return jsonify({"data": pedido})
    return jsonify({"error": "Pedido no encontrado"}), 404

if __name__ == '__main__':
    port = int(os.getenv('ORDERS_SERVICE_PORT', 5001))
    app.run(port=port, debug=True)