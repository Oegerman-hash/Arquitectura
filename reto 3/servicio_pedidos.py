from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import requests
import win32evtlogutil
import win32evtlog

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Datos simulados de pedidos
pedidos = [
    {"id": 1, "usuario_id": 1, "producto": "Laptop", "cantidad": 1, "total": 999.99},
    {"id": 2, "usuario_id": 1, "producto": "Mouse", "cantidad": 2, "total": 49.98},
    {"id": 3, "usuario_id": 2, "producto": "Monitor", "cantidad": 1, "total": 299.99},
    {"id": 4, "usuario_id": 3, "producto": "Teclado", "cantidad": 1, "total": 89.99}
]

# Función para registrar eventos en el Visor de Eventos de Windows
def log_event(message, event_type=win32evtlog.EVENTLOG_INFORMATION_TYPE):
    try:
        win32evtlogutil.ReportEvent(
            "Aplicación",  # Log en el que se escribirán los eventos
            1,  # Event ID
            eventCategory=0,  # Event Category
            eventType=event_type,
            strings=[message]
        )
    except Exception as e:
        print(f"Error logging event: {e}")

def verificar_usuario(usuario_id):
    try:
        response = requests.get(f'http://localhost:{os.getenv("USERS_SERVICE_PORT")}/api/usuarios/{usuario_id}')
        return response.status_code == 200
    except requests.RequestException:
        log_event(f"Error al verificar usuario con ID {usuario_id}.", event_type=win32evtlog.EVENTLOG_ERROR_TYPE)
        return False

@app.route('/api/pedidos', methods=['GET'])
def obtener_pedidos():
    log_event("Solicitud para obtener pedidos recibida.")
    return jsonify({
        "servicio": "pedidos",
        "data": pedidos,
        "status": "success"
    })

@app.route('/api/pedidos/<int:usuario_id>', methods=['GET'])
def obtener_pedidos_usuario(usuario_id):
    log_event(f"Solicitud para obtener pedidos del usuario con ID {usuario_id} recibida.")
    if not verificar_usuario(usuario_id):
        log_event(f"Usuario con ID {usuario_id} no válido.", event_type=win32evtlog.EVENTLOG_WARNING_TYPE)
        return jsonify({"error": "Usuario no válido", "status": "error"}), 404

    pedidos_usuario = [p for p in pedidos if p['usuario_id'] == usuario_id]
    return jsonify({
        "servicio": "pedidos",
        "data": pedidos_usuario,
        "status": "success"
    })

@app.route('/api/pedidos/healthcheck', methods=['GET'])
def healthcheck():
    log_event("Solicitud de healthcheck recibida.")
    return jsonify({"status": "healthy", "service": "pedidos"})

if __name__ == '__main__':
    port = int(os.getenv('ORDERS_SERVICE_PORT', 5001))
    app.run(port=port, debug=True)