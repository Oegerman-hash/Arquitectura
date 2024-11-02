from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import win32evtlogutil
import win32evtlog

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Datos simulados de usuarios
usuarios = [
    {"id": 1, "nombre": "Ana García", "email": "ana@email.com"},
    {"id": 2, "nombre": "Carlos López", "email": "carlos@email.com"},
    {"id": 3, "nombre": "María Rodríguez", "email": "maria@email.com"}
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

@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    log_event("Solicitud para obtener usuarios recibida.")
    return jsonify({
        "servicio": "usuarios",
        "data": usuarios,
        "status": "success"
    })

@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    log_event(f"Solicitud para obtener usuario con ID {usuario_id} recibida.")
    usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
    if usuario:
        return jsonify({
            "servicio": "usuarios",
            "data": usuario,
            "status": "success"
        })
    log_event(f"Usuario con ID {usuario_id} no encontrado.", event_type=win32evtlog.EVENTLOG_WARNING_TYPE)
    return jsonify({"error": "Usuario no encontrado", "status": "error"}), 404

@app.route('/api/usuarios/healthcheck', methods=['GET'])
def healthcheck():
    log_event("Solicitud de healthcheck recibida.")
    return jsonify({"status": "healthy", "service": "usuarios"})

if __name__ == '__main__':
    port = int(os.getenv('USERS_SERVICE_PORT', 5000))
    app.run(port=port, debug=True)