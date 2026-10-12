stack = []
size = 0
pos = 0

def isEmpty(stack):
    return not stack

def peek(stack):
    if isEmpty(stack):
        return("La pila esta vacía")
    return stack[-1]

def push(item, stack, size, pos):
    if pos < size:
        stack.append(item)
        return "Elemento apilado..."
    else:
        return "Pila llena..."

def pop(stack):
    if isEmpty(stack):
        return "La pila esta vacía..."
    return stack.pop()

def len_stack(stack):
    if isEmpty(stack):
        return "La pila esta vacía..."
    return len(stack)

def show(stack):
    if isEmpty(stack):
        return "Pila vacía..."
    my_stack = f""
    my_stack += "┌" + "—"*8 + "┐ \n"
    my_stack += "▌  Pila  ▌ \n"
    for item in reversed(stack):
        my_stack += f"▌"+ "-"*8 + "▌\n"
        my_stack += f"▌ {item:<6} ▌\n"
    my_stack += "└" + "—"*8 + "┘"
    return my_stack

def menu():
    print("1. Apilar")
    print("2. Mostrar Pila")
    print("3. Mostrar Tope")
    print("0. Salir")

def option():
    while True:
      menu()
      op = input("Dime una opción: ")
      if op == "1":
        item = input("Dime un valor: ")
        print(push(item, stack, size))
        pos += 1
      elif op == "2":
        print(show(stack))
      elif op == "3":
        print(peek(stack))
      elif op == "0":
          break

option()