pendientes = ["T001", "T002", "T003", "T004"]
historial = ["T005", "T006"]

def cancelar_pendiente(id_solicitud):
    if id_solicitud in pendientes:
        pendientes.remove(id_solicitud)
        return id_solicitud

    return None

print(cancelar_pendiente("T002"))
print(pendientes)

print(cancelar_pendiente("T005"))
print(pendientes)
