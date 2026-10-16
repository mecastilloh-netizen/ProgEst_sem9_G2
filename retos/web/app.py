"""Interfaz Flask del gestor de solicitudes."""

from flask import Flask, flash, redirect, render_template, request, url_for

import logica

app = Flask(__name__)
app.secret_key = "gestor-solicitudes-local"


def mostrar_inicio(**datos):
    return render_template(
        "index.html",
        pendientes=logica.cola_pendientes,
        historial=reversed(logica.pila_historial),
        siguiente=logica.consultar_siguiente(),
        estadisticas=logica.estadisticas(),
        **datos,
    )


@app.get("/")
def inicio():
    return mostrar_inicio()


@app.post("/registrar")
def registrar():
    solicitud, error = logica.registrar_solicitud(
        request.form.get("cliente", ""), request.form.get("asunto", "")
    )
    if error:
        flash(error, "warning")
    else:
        flash(f"Solicitud #{solicitud['id']} registrada.", "success")
    return redirect(url_for("inicio"))


@app.post("/atender")
def atender():
    solicitud = logica.atender_siguiente()
    if solicitud:
        flash(f"Solicitud #{solicitud['id']} atendida.", "success")
    else:
        flash("No hay solicitudes pendientes para atender.", "info")
    return redirect(url_for("inicio"))


@app.post("/deshacer")
def deshacer():
    solicitud = logica.deshacer_ultima_atencion()
    if solicitud:
        flash(f"Solicitud #{solicitud['id']} restaurada al inicio de la cola.", "success")
    else:
        flash("No hay atenciones para deshacer.", "info")
    return redirect(url_for("inicio"))


@app.post("/deshacer-varias")
def deshacer_varias():
    try:
        cantidad = int(request.form.get("cantidad", ""))
        restauradas = logica.deshacer_varias(cantidad)
    except ValueError:
        flash("Ingresa un número entero mayor que cero.", "warning")
    else:
        flash(f"Se restauraron {restauradas} solicitudes.", "success" if restauradas else "info")
    return redirect(url_for("inicio"))


@app.get("/buscar")
def buscar():
    texto_id = request.args.get("id", "").strip()
    if not texto_id.isdecimal() or int(texto_id) < 1:
        return mostrar_inicio(busqueda_error="Ingresa un ID entero mayor que cero.", busqueda_id=texto_id)

    solicitud, estado = logica.buscar_por_id(int(texto_id))
    return mostrar_inicio(
        busqueda=solicitud,
        busqueda_estado=estado,
        busqueda_id=texto_id,
        busqueda_realizada=True,
    )


@app.post("/cancelar/<int:identificador>")
def cancelar(identificador):
    solicitud = logica.cancelar_solicitud(identificador)
    if solicitud:
        flash(f"Solicitud #{identificador} cancelada.", "success")
    else:
        flash(f"La solicitud #{identificador} no está pendiente.", "warning")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
