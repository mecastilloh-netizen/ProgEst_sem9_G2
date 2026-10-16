"""Operaciones en memoria del gestor de solicitudes."""

cola_pendientes = []
pila_historial = []
siguiente_id = 1


def registrar_solicitud(cliente, asunto):
    """Agrega una solicitud, salvo que ya exista una pendiente igual."""
    global siguiente_id

    cliente = cliente.strip()
    asunto = asunto.strip()
    if not cliente or not asunto:
        return None, "El cliente y el asunto son obligatorios."

    if any(
        item["cliente"].casefold() == cliente.casefold()
        and item["asunto"].casefold() == asunto.casefold()
        for item in cola_pendientes
    ):
        return None, "Esta solicitud ya se encuentra pendiente."

    solicitud = {"id": siguiente_id, "cliente": cliente, "asunto": asunto}
    cola_pendientes.append(solicitud)
    siguiente_id += 1
    return solicitud, None


def consultar_siguiente():
    """Consulta la primera solicitud sin retirarla de la cola."""
    return cola_pendientes[0] if cola_pendientes else None


def atender_siguiente():
    if not cola_pendientes:
        return None
    solicitud = cola_pendientes.pop(0)
    pila_historial.append(solicitud)
    return solicitud


def deshacer_ultima_atencion():
    if not pila_historial:
        return None
    solicitud = pila_historial.pop()
    cola_pendientes.insert(0, solicitud)
    return solicitud


def deshacer_varias(cantidad):
    """Restaura hasta `cantidad` atenciones en su orden original."""
    if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 1:
        raise ValueError("La cantidad debe ser un entero positivo.")

    restauradas = 0
    while restauradas < cantidad and pila_historial:
        deshacer_ultima_atencion()
        restauradas += 1
    return restauradas


def buscar_por_id(identificador):
    for estado, solicitudes in (
        ("Pendiente", cola_pendientes),
        ("Atendida", pila_historial),
    ):
        for solicitud in solicitudes:
            if solicitud["id"] == identificador:
                return solicitud, estado
    return None, None


def cancelar_solicitud(identificador):
    """Elimina solo una solicitud pendiente."""
    for indice, solicitud in enumerate(cola_pendientes):
        if solicitud["id"] == identificador:
            return cola_pendientes.pop(indice)
    return None


def estadisticas():
    pendientes = len(cola_pendientes)
    atendidas = len(pila_historial)
    return {
        "pendientes": pendientes,
        "atendidas": atendidas,
        "total": pendientes + atendidas,
    }
