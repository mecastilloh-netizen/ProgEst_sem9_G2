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