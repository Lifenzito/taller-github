import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# permite llamadas desde Vite (http://localhost)
CORS(app, resources={r"/*": {"origins": "*"}})

# "base de datos" en memoria (solo para la demo)
users = []

# regex simple para validar email
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"msg": "Datos incompletos"}), 400

    email = data["email"].strip()
    password = data["password"]

    if not EMAIL_REGEX.match(email):
        return jsonify({"msg": "Email inválido"}), 400

    if len(password) < 4:
        return jsonify({"msg": "La contraseña debe tener al menos 4 caracteres"}), 400

    if any(u["email"].lower() == email.lower() for u in users):
        return jsonify({"msg": "El email ya está registrado"}), 409

    users.append({"email": email, "password": password})
    return jsonify({"msg": "Usuario registrado exitosamente"}), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"msg": "Datos incompletos"}), 400

    email = data["email"].strip()
    password = data["password"]

    # usuario fijo de prueba
    if email == "user@test.com" and password == "Test123":
        return jsonify({"msg": "Login exitoso (usuario de prueba)"}), 200

    # validar contra usuarios registrados
    for u in users:
        if u["email"].lower() == email.lower() and u["password"] == password:
            return jsonify({"msg": "Login exitoso"}), 200

    return jsonify({"msg": "Credenciales inválidas"}), 401

# Debug: listar usuarios registrados
@app.route("/users", methods=["GET"])
def get_users():
    # NO es seguro en producción (muestra contraseñas); solo para la demo
    return jsonify(users), 200

if __name__ == "__main__":
    # Debe coincidir con lo que usa tu App.vue (127.0.0.1:5000)
    app.run(host="127.0.0.1", port=5000, debug=True)