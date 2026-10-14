stack = []
actual = ""

def isEmpty(stack):
    return not stack

def push(item, stack):
    stack.append(item)
    return "Pagina guardada..."

def pop(stack):
    if isEmpty(stack):
        return "Sin pagina anterior"
    return stack.pop()

def visitar(pagina):
    global actual
    if pagina == "":
        return "La pagina no puede estar vacía"
    if actual != "":
        push(actual, stack)
    actual = pagina
    return f"Visitando: {actual}"

def regresar():
    global actual
    if isEmpty(stack):
        return "Sin pagina anterior"
    actual = pop(stack)
    return f"Regresando a: {actual}"

def mostrar_actual():
    if actual == "":
        return "No hay página actual"
    return f"Pagina actual: {actual}"

def show(stack):
    if isEmpty(stack):
        return "Historial vacío..."

    historial = ""
    for pagina in reversed(stack):
        historial += pagina + "\n"
    return historial

def menu():
    print("1. Visitar página")
    print("2. Regresar")
    print("3. Mostrar actual")
    print("4. Mostrar historial")
    print("0. Salir")

def option():
    while True:
        menu()
        op = input("Dime una opción: ")
        if op == "1":
            pagina = input("Dime la página: ").strip()
            print(visitar(pagina))
        elif op == "2":
            print(regresar())
        elif op == "3":
            print(mostrar_actual())
        elif op == "4":
            print(show(stack))
        elif op == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")

option()
