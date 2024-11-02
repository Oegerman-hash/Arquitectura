from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import redis
import json

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar Redis
cache = redis.Redis(host='localhost', port=6379, db=0)

# Simulación de base de datos
usuarios = [
    {"id": 1, "nombre": "Ana García", "email": "ana@email.com"},
    {"id": 2, "nombre": "Carlos López", "email": "carlos@email.com"},
    {"id": 3, "nombre": "María Rodríguez", "email": "maria@email.com"}
]

def obtener_usuarios_desde_db():
    """Simula una consulta a la base de datos."""
    return usuarios

@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    # Intentar obtener los datos de usuarios desde el caché Redis
    usuarios_cache = cache.get("usuarios")

    if usuarios_cache:
        # Si encontramos los datos en caché, los devolvemos directamente
        return jsonify({
            "servicio": "usuarios",
            "data": json.loads(usuarios_cache),
            "status": "success (from cache)"
        })

    # Si no están en caché, los obtenemos de la "base de datos"
    data = obtener_usuarios_desde_db()
    
    # Guardar los datos en el caché por 10 minutos (600 segundos)
    cache.setex("usuarios", 600, json.dumps(data))

    return jsonify({
        "servicio": "usuarios",
        "data": data,
        "status": "success"
    })

@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    # Intentar obtener el usuario específico desde el caché
    usuario_cache = cache.get(f"usuario:{usuario_id}")

    if usuario_cache:
        # Si está en caché, lo devolvemos directamente
        return jsonify({
            "servicio": "usuarios",
            "data": json.loads(usuario_cache),
            "status": "success (from cache)"
        })

    # Si no está en caché, busca en la "base de datos"
    usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
    
    if usuario:
        # Guardar el usuario específico en el caché por 10 minutos
        cache.setex(f"usuario:{usuario_id}", 600, json.dumps(usuario))
        return jsonify({
            "servicio": "usuarios",
            "data": usuario,
            "status": "success"
        })

    return jsonify({"error": "Usuario no encontrado", "status": "error"}), 404

@app.route('/api/usuarios/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy", "service": "usuarios"})

if __name__ == '__main__':
    port = int(os.getenv('USERS_SERVICE_PORT', 5000))
    app.run(port=port, debug=True)
