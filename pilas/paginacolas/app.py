from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-key-paginacolas-cambiar-en-produccion"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
MAX_NOMBRE = 80


def obtener_cola():
    cola = session.get("cola", [])
    return cola if isinstance(cola, list) else []


@app.get("/")
def inicio():
    return render_template("index.html")


@app.get("/api/cola")
def consultar_cola():
    return jsonify({"nombres": obtener_cola()})


@app.post("/api/cola")
def encolar_nombre():
    datos = request.get_json(silent=True)
    nombre = datos.get("nombre") if isinstance(datos, dict) else None
    if not isinstance(nombre, str) or not nombre.strip():
        return jsonify({"error": "Escribe o dicta un nombre para agregarlo a la cola."}), 400
    nombre = nombre.strip()
    if len(nombre) > MAX_NOMBRE:
        return jsonify({"error": f"El nombre no puede superar los {MAX_NOMBRE} caracteres."}), 400
    cola = obtener_cola()
    cola.append(nombre)
    session["cola"] = cola
    return jsonify({"mensaje": f"{nombre} se agregó al final de la cola.", "nombres": cola}), 201


@app.post("/api/cola/atender")
def atender_siguiente():
    cola = obtener_cola()
    if not cola:
        return jsonify({"error": "La cola está vacía."}), 409
    atendido = cola.pop(0)
    session["cola"] = cola
    return jsonify({"mensaje": f"Turno atendido: {atendido}.", "atendido": atendido, "nombres": cola})


@app.post("/api/cola/limpiar")
def limpiar_cola():
    session["cola"] = []
    return jsonify({"mensaje": "La cola quedó vacía.", "nombres": []})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
