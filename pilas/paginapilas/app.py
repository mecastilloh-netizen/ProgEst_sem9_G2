"""Aplicación educativa para visualizar pilas de palabras e imágenes."""

import os
import secrets
import warnings
from io import BytesIO
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory, session, url_for
from PIL import Image, ImageOps, UnidentifiedImageError
from werkzeug.exceptions import HTTPException

CAPACIDAD_PREDETERMINADA = 8
CAPACIDAD_MAXIMA = 20
MAX_IMAGEN_BYTES = 5 * 1024 * 1024
FORMATOS_PERMITIDOS = {"JPEG", "PNG", "WEBP", "GIF"}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-key-cambiar-en-produccion")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 10_000_000

DIRECTORIO_IMAGENES = Path(app.instance_path) / "uploads"
DIRECTORIO_IMAGENES.mkdir(parents=True, exist_ok=True)


def obtener_pilas():
    """Devuelve las dos pilas de la sesión, separadas por tipo."""
    pilas = session.get("pilas")
    if not isinstance(pilas, dict):
        anterior = session.get("pila", [])
        pilas = {"palabras": anterior if isinstance(anterior, list) else [], "imagenes": []}
    return {
        "palabras": pilas.get("palabras", []) if isinstance(pilas.get("palabras"), list) else [],
        "imagenes": pilas.get("imagenes", []) if isinstance(pilas.get("imagenes"), list) else [],
    }


def modo_actual():
    modo = session.get("modo")
    return modo if modo in ("palabras", "imagenes") else None


def guardar_pila(modo, pila):
    pilas = obtener_pilas()
    pilas[modo] = pila
    session["pilas"] = pilas


def obtener_capacidad(modo):
    capacidades = session.get("capacidades", {})
    valor = capacidades.get(modo) if isinstance(capacidades, dict) else None
    if type(valor) is int and 1 <= valor <= CAPACIDAD_MAXIMA:
        return valor
    return CAPACIDAD_PREDETERMINADA


def estado_pila(mensaje=None):
    modo = modo_actual()
    elementos = obtener_pilas()[modo] if modo else []
    if modo == "imagenes":
        elementos = [
            {"id": item["id"], "nombre": item["nombre"],
             "url": url_for("ver_imagen", image_id=item["id"])}
            for item in elementos
        ]
    estado = {"modo": modo, "elementos": elementos,
              "cantidad": len(elementos), "capacidad": obtener_capacidad(modo),
              "capacidad_maxima": CAPACIDAD_MAXIMA}
    if mensaje:
        estado["mensaje"] = mensaje
    return estado


def borrar_imagen(item):
    """Elimina únicamente archivos creados por esta aplicación."""
    nombre = item.get("archivo", "") if isinstance(item, dict) else ""
    if nombre and Path(nombre).name == nombre:
        (DIRECTORIO_IMAGENES / nombre).unlink(missing_ok=True)


@app.get("/")
def inicio():
    return render_template("index.html")


@app.get("/api/pila")
def consultar_pila():
    return jsonify(estado_pila())


@app.post("/api/modo")
def seleccionar_modo():
    datos = request.get_json(silent=True)
    modo = datos.get("modo") if isinstance(datos, dict) else None
    if modo not in ("palabras", "imagenes"):
        return jsonify({"error": "Elige palabras o imágenes."}), 400
    session["modo"] = modo
    return jsonify(estado_pila())


@app.post("/api/pila/capacidad")
def cambiar_capacidad():
    modo = modo_actual()
    if not modo:
        return jsonify({"error": "Selecciona primero el tipo de pila."}), 409
    datos = request.get_json(silent=True)
    nueva = datos.get("capacidad") if isinstance(datos, dict) else None
    if type(nueva) is not int or not 1 <= nueva <= CAPACIDAD_MAXIMA:
        return jsonify({"error": f"Elige una capacidad entre 1 y {CAPACIDAD_MAXIMA}."}), 400
    if nueva < len(obtener_pilas()[modo]):
        return jsonify({"error": "La capacidad no puede ser menor que la cantidad de elementos actuales."}), 409
    capacidades = session.get("capacidades", {})
    if not isinstance(capacidades, dict):
        capacidades = {}
    capacidades[modo] = nueva
    session["capacidades"] = capacidades
    return jsonify(estado_pila(f"Capacidad actualizada a {nueva} elementos."))


@app.post("/api/pila")
def apilar_palabra():
    if modo_actual() != "palabras":
        return jsonify({"error": "Selecciona primero la pila de palabras."}), 409
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify({"error": "Envía un JSON con el campo 'elemento'."}), 400
    elemento = datos.get("elemento")
    if not isinstance(elemento, str) or not elemento.strip():
        return jsonify({"error": "Escribe una palabra antes de apilar."}), 400
    elemento = elemento.strip()
    if len(elemento) > 40:
        return jsonify({"error": "El texto no puede superar los 40 caracteres."}), 400
    pila = obtener_pilas()["palabras"]
    if len(pila) >= obtener_capacidad("palabras"):
        return jsonify({"error": "La pila está llena. Retira un elemento para continuar."}), 409
    pila.append(elemento)
    guardar_pila("palabras", pila)
    return jsonify(estado_pila(f"'{elemento}' se apiló correctamente.")), 201


@app.post("/api/pila/imagen")
def apilar_imagen():
    if modo_actual() != "imagenes":
        return jsonify({"error": "Selecciona primero la pila de imágenes."}), 409
    pila = obtener_pilas()["imagenes"]
    if len(pila) >= obtener_capacidad("imagenes"):
        return jsonify({"error": "La pila está llena. Retira una imagen para continuar."}), 409
    archivo = request.files.get("imagen")
    if not archivo or not archivo.filename:
        return jsonify({"error": "Selecciona una imagen antes de apilar."}), 400
    contenido = archivo.read(MAX_IMAGEN_BYTES + 1)
    if len(contenido) > MAX_IMAGEN_BYTES:
        return jsonify({"error": "La imagen no puede superar los 5 MB."}), 413

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(contenido)) as imagen:
                if imagen.format not in FORMATOS_PERMITIDOS:
                    return jsonify({"error": "Usa una imagen JPG, PNG, WEBP o GIF."}), 400
                imagen.verify()
            with Image.open(BytesIO(contenido)) as imagen:
                imagen = ImageOps.exif_transpose(imagen)
                imagen.thumbnail((1200, 1200))
                transparente = "A" in imagen.getbands() or "transparency" in imagen.info
                extension = "png" if transparente else "jpg"
                identificador = secrets.token_hex(12)
                nombre_archivo = f"{identificador}.{extension}"
                destino = DIRECTORIO_IMAGENES / nombre_archivo
                if transparente:
                    imagen.convert("RGBA").save(destino, format="PNG", optimize=True)
                else:
                    imagen.convert("RGB").save(destino, format="JPEG", quality=85, optimize=True)
    except (OSError, ValueError, UnidentifiedImageError,
            Image.DecompressionBombError, Image.DecompressionBombWarning):
        return jsonify({"error": "El archivo no es una imagen válida o es demasiado grande."}), 400

    nombre_original = Path(archivo.filename.replace("\\", "/")).name[:80]
    pila.append({"id": identificador, "archivo": nombre_archivo, "nombre": nombre_original})
    guardar_pila("imagenes", pila)
    return jsonify(estado_pila(f"'{nombre_original}' se apiló correctamente.")), 201


@app.get("/api/imagen/<image_id>")
def ver_imagen(image_id):
    for item in obtener_pilas()["imagenes"]:
        if item.get("id") == image_id:
            respuesta = send_from_directory(DIRECTORIO_IMAGENES, item["archivo"])
            respuesta.headers["Cache-Control"] = "private, no-store"
            return respuesta
    return jsonify({"error": "Imagen no encontrada en esta sesión."}), 404


@app.post("/api/pila/reordenar")
def reordenar_pila():
    modo = modo_actual()
    if not modo:
        return jsonify({"error": "Selecciona primero el tipo de pila."}), 409
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify({"error": "Indica las posiciones de origen y destino."}), 400
    origen = datos.get("origen")
    destino = datos.get("destino")
    pila = obtener_pilas()[modo]
    if (type(origen) is not int or type(destino) is not int
            or not 1 <= origen <= len(pila) or not 1 <= destino <= len(pila)):
        return jsonify({"error": "Las posiciones deben estar dentro de la pila."}), 400
    if origen != destino:
        elemento = pila.pop(origen - 1)
        pila.insert(destino - 1, elemento)
        guardar_pila(modo, pila)
    return jsonify(estado_pila(f"Elemento movido a la posición {destino}."))


@app.post("/api/pila/desapilar")
def desapilar():
    modo = modo_actual()
    if not modo:
        return jsonify({"error": "Selecciona primero el tipo de pila."}), 409
    pila = obtener_pilas()[modo]
    if not pila:
        return jsonify({"error": "La pila está vacía. No hay elementos para retirar."}), 409
    elemento = pila.pop()
    guardar_pila(modo, pila)
    if modo == "imagenes":
        borrar_imagen(elemento)
        nombre = elemento["nombre"]
    else:
        nombre = elemento
    return jsonify(estado_pila(f"'{nombre}' salió de la pila."))


@app.delete("/api/pila")
def vaciar_pila():
    modo = modo_actual()
    if not modo:
        return jsonify({"error": "Selecciona primero el tipo de pila."}), 409
    pila = obtener_pilas()[modo]
    guardar_pila(modo, [])
    if modo == "imagenes":
        for item in pila:
            borrar_imagen(item)
    return jsonify(estado_pila("La pila quedó vacía."))


@app.errorhandler(HTTPException)
def error_http(error):
    if request.path.startswith("/api/"):
        return jsonify({"error": error.description}), error.code
    return error


if __name__ == "__main__":
    app.run(debug=True)
