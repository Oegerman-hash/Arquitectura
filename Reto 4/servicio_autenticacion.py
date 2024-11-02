from flask import Flask, jsonify
from flask_windows_auth import WindowsAuth

app = Flask(__name__)
auth = WindowsAuth(app)

@app.route('/api/auth', methods=['GET'])
@auth.login_required
def auth_user():
    user = auth.get_user()
    return jsonify({"message": f"Bienvenido, {user}!"})

if __name__ == '__main__':
    app.run(port=5002, debug=True)