from flask import Flask, jsonify
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Simulación de configuración
configuracion = {
    "USERS_SERVICE_PORT": os.getenv("USERS_SERVICE_PORT", 5000),
    "ORDERS_SERVICE_PORT": os.getenv("ORDERS_SERVICE_PORT", 5001),
    "DATABASE_URL": os.getenv("DATABASE_URL", "sqlite:///default.db"),
    "API_KEY": os.getenv("API_KEY", "default_api_key")
}

@app.route('/api/configuracion', methods=['GET'])
def obtener_configuracion():
    return jsonify({
        "servicio": "configuracion",
        "data": configuracion,
        "status": "success"
    })

if __name__ == '__main__':
    port = int(os.getenv('CONFIG_SERVICE_PORT', 5002))
    app.run(port=port, debug=True)