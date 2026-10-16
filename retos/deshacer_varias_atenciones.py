pendientes = ["A", "B", "C", "D"]
historial = []

def atender():
    if not pendientes:
        return None

    solicitud = pendientes.pop(0)
    historial.append(solicitud)
    return solicitud

def deshacer_ultima_atencion():
    if not historial:
        return None

    solicitud = historial.pop()
    pendientes.insert(0, solicitud)
    return solicitud

def deshacer_varias(cantidad):
    if type(cantidad) != int:
        return "Cantidad no válida"

    if cantidad <= 0:
        return "Cantidad no válida"

    recuperadas = 0

    for i in range(cantidad):
        resultado = deshacer_ultima_atencion()

        if resultado == None:
            break

        recuperadas += 1

    return recuperadas

atender()
atender()
atender()

print("Pendientes:", pendientes)
print("Historial:", historial)

print("Recuperadas:", deshacer_varias(2))

print("Pendientes:", pendientes)
print("Historial:", historial)