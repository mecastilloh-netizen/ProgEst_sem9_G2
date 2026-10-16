pendientes = []
historial = []

def registrar_solicitud(cliente, asunto):
    cliente = cliente.strip().lower()
    asunto = asunto.strip().lower()

    if cliente == "" or asunto == "":
        return "Datos vacíos"

    for solicitud in pendientes:
        nombre = solicitud[0]
        tema = solicitud[1]

        if nombre == cliente:
            if tema == asunto:
                return "Solicitud duplicada"

    pendientes.append([cliente, asunto])
    return "Solicitud registrada"

def obtener_estadisticas():
    unicas = []

    for solicitud in pendientes:
        if solicitud not in unicas:
            unicas.append(solicitud)

    for solicitud in historial:
        if solicitud not in unicas:
            unicas.append(solicitud)

    print("Pendientes:", len(pendientes))
    print("Atendidas:", len(historial))
    print("Total únicas:", len(unicas))

print(registrar_solicitud("Ana", "Wi-Fi"))
print(registrar_solicitud(" ana ", " wi-fi "))

print("Lista:", pendientes)
obtener_estadisticas()