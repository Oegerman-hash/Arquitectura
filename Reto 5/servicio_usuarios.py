from flask import Flask, jsonify, request
from prometheus_client import start_http_server, Counter, Gauge, Summary
import time
import os

app = Flask(__name__)

# Definir métricas
REQUEST_COUNT = Counter('usuarios_requests_total', 'Total de solicitudes recibidas')
REQUEST_LATENCY = Summary('usuarios_request_latency_seconds', 'Latencia de solicitudes')
ACTIVE_USERS = Gauge('usuarios_active', 'Número de usuarios activos en la aplicación')

# Datos simulados de usuarios
usuarios = [
    {"id": 1, "nombre": "Ana García", "email": "ana@email.com"},
    {"id": 2, "nombre": "Carlos López", "email": "carlos@email.com"},
    {"id": 3, "nombre": "María Rodríguez", "email": "maria@email.com"}
]

@app.before_request
def before_request():
    REQUEST_COUNT.inc()  # Incrementar contador en cada solicitud

@app.route('/api/usuarios', methods=['GET'])
@REQUEST_LATENCY.time()  # Medir latencia
def obtener_usuarios_api():
    """Endpoint para obtener todos los usuarios con métricas"""
    ACTIVE_USERS.set(len(usuarios))  # Ajustar usuarios activos
    return jsonify({
        "servicio": "usuarios",
        "data": usuarios,
        "status": "success"
    })

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    """Endpoint para obtener todos los usuarios sin métricas"""
    return jsonify({"usuarios": usuarios, "total": len(usuarios)})

@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    """Endpoint para obtener un usuario específico por ID"""
    usuario = next((u for u in usuarios if u["id"] == usuario_id), None)
    if usuario:
        return jsonify({"usuario": usuario})
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/health', methods=['GET'])
def healthcheck():
    """Endpoint para verificar el estado del servicio"""
    return jsonify({"status": "healthy", "service": "usuarios"})

if __name__ == '__main__':
    # Iniciar el servidor de métricas de Prometheus
    start_http_server(8000)  # En este puerto Prometheus recogerá métricas
    puerto = int(os.getenv('USERS_SERVICE_PORT', 5000))
    app.run(port=puerto, debug=True)
