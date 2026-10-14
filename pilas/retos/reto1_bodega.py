
stack = []
size = 5

def isEmpty(stack):
    return not stack

def peek(stack):
    if isEmpty(stack):
        return "La pila esta vacía"
    return stack[-1]

def push(item, stack, size):
    if item == "":
        return "El codigo no puede estar vacío"
    if item in stack:
        return "La caja ya existe"
    if len(stack) < size:
        stack.append(item)
        return "Caja apilada..."
    return "Pila llena..."

def pop(stack):
    if isEmpty(stack):
        return "La pila esta vacía..."
    return stack.pop()

def len_stack(stack):
    return len(stack)

def show(stack):
    if isEmpty(stack):
        return "Pila vacía..."

    my_stack = ""
    my_stack += "┌" + "—"*12 + "┐\n"
    my_stack += "│   BODEGA   │\n"

    for item in reversed(stack):
        my_stack += "├" + "—"*12 + "┤\n"
        my_stack += f"│ {item:<10} │\n"

    my_stack += "└" + "—"*12 + "┘"
    return my_stack

def menu():
    print("1. Apilar caja")
    print("2. Desapilar caja")
    print("3. Consultar tope")
    print("4. Mostrar pila")
    print("0. Salir")

def option():
    while True:
        menu()
        op = input("Dime una opción: ")
        if op == "1":
            item = input("Dime el código de la caja: ").strip()
            print(push(item, stack, size))
        elif op == "2":
            print("Caja retirada:", pop(stack))
        elif op == "3":
            print("Tope:", peek(stack))
        elif op == "4":
            print(show(stack))
            print("Cantidad de cajas:", len_stack(stack))
        elif op == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")

option()