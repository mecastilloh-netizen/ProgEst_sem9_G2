cola = ["C001", "C002", "C003"]

def consultar_siguiente():
    if not cola:
        return None
    return cola[0]

print(consultar_siguiente())
print(consultar_siguiente())
print("Cantidad de turnos:", len(cola))
