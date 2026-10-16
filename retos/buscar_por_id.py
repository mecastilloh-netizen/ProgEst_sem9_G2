pendientes = ["T001", "T002", "T003"]
historial = ["T004", "T005"]

def buscar_solicitud(id_solicitud):
    if id_solicitud in pendientes:
        return id_solicitud, "Pendientes"

    if id_solicitud in historial:
        return id_solicitud, "Historial"

    return None

print(buscar_solicitud("T002"))
print(buscar_solicitud("T005"))
print(buscar_solicitud("T010"))
