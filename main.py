class NodoArbol:

    def __init__(self, pregunta, respuesta_si=None, respuesta_no=None):
        self.pregunta = pregunta
        self.respuesta_si = respuesta_si
        self.respuesta_no = respuesta_no


def recorrer_arbol_inorden(nodo):
    if nodo is not None:
        recorrer_arbol_inorden(nodo.izquierda)
        print(nodo.valor, end='')
        recorrer_arbol_inorden(nodo.derecha)


def recorrer_arbol_preorden(nodo):
    if nodo is not None:
        print(nodo.valor, end='')
        recorrer_arbol_preorden(nodo.izquierda)
        recorrer_arbol_preorden(nodo.derecha)


def recorrer_arbol_postorden(nodo):
    if nodo is not None:
        recorrer_arbol_postorden(nodo.izquierda)
        recorrer_arbol_postorden(nodo.derecha)
        print(nodo.valor, end='')


def construir_arbol():
    pregunta_raiz = input("Ingrese la pregunta raíz: ")
    nodo_raiz = NodoArbol(pregunta_raiz)

    nodo_raiz.respuesta_si = construir_nodo()
    if nodo_raiz.respuesta_si is not None:
        nodo_raiz.respuesta_no = construir_nodo()
    return nodo_raiz


def construir_nodo():
    respuesta = input("Ingrese un objeto o una pregunta: ")
    if not respuesta:  # Si el usuario no ingresa nada
        return None
    if respuesta == "objeto":
        objeto = input("Ingrese el objeto: ")
        return objeto
    else:
        nodo = NodoArbol(respuesta)
        hijo_izquierdo = construir_nodo()
        if hijo_izquierdo is not None:  # Si el hijo izquierdo no es None
            nodo.respuesta_si = hijo_izquierdo
            hijo_derecho = construir_nodo()
            if hijo_derecho is not None:  # Si el hijo derecho no es None
                nodo.respuesta_no = hijo_derecho
        return nodo


def jugar(nodo_raiz):
    if nodo_raiz is None:
        print("El árbol está vacío o tiene un formato incorrecto.")
        return

    if isinstance(nodo_raiz, str):
        print("¿Es un/una", nodo_raiz, "?")
        respuesta = input("Ingrese 'si' o 'no': ").lower()
        if respuesta == "si":
            print("¡Adiviné correctamente!")
            return
        else:
            objeto = input("Ingrese el objeto que tenías en mente: ")
            pregunta = input(f"Ingrese una pregunta que distinga a '{objeto}' de '{nodo_raiz}': ")
            respuesta_objeto = input(f"¿La respuesta para '{objeto}' es 'si' o 'no'? ").lower()
            if respuesta_objeto == "si":
                nodo_raiz = NodoArbol(pregunta, objeto, nodo_raiz)
            else:
                nodo_raiz = NodoArbol(pregunta, nodo_raiz, objeto)
            print("¡Gracias por ayudarme a aprender!")
    else:
        print(nodo_raiz.pregunta)
        respuesta = input("Ingrese 'si' o 'no': ").lower()
        if respuesta == "si":
            jugar(nodo_raiz.respuesta_si)
        else:
            jugar(nodo_raiz.respuesta_no)


def preorden(nodo):
    if isinstance(nodo, str):
        print(nodo)
    else:
        print(nodo.pregunta)
        preorden(nodo.respuesta_si)
        preorden(nodo.respuesta_no)


def inorden(nodo):
    if isinstance(nodo, str):
        print(nodo)
    else:
        inorden(nodo.respuesta_si)
        print(nodo.pregunta)
        inorden(nodo.respuesta_no)


def postorden(nodo):
    if isinstance(nodo, str):
        print(nodo)
    else:
        postorden(nodo.respuesta_si)
        postorden(nodo.respuesta_no)
        print(nodo.pregunta)


def exportar_arbol(nodo_raiz, archivo):
    with open(archivo, "w") as f:
        f.write("Preorder:\n")
        preorden(nodo_raiz)
        f.write("\nInorder:\n")
        inorden(nodo_raiz)
        f.write("\nPostorder:\n")
        postorden(nodo_raiz)


def importar_arbol(archivo):
    with open(archivo, "r") as f:
        contenido = f.read().split("\n")
    preorden_lista = contenido[1:contenido.index("Inorden:")]
    inorden_lista = contenido[contenido.index("Inorden:") + 1:contenido.index("Postorden:")]
    postorden_lista = contenido[contenido.index("Postorden:") + 1:]

    def construir_desde_preorder(preorder_lista):
        if not preorder_lista:
           return None
        pregunta = preorder_lista.pop(0)
        nodo = NodoArbol(pregunta)
        nodo.respuesta_si = construir_desde_preorder(preorder_lista)
        nodo.respuesta_no = construir_desde_preorder(preorder_lista)
        return nodo

    nodo_raiz = construir_desde_preorder(preorden_lista)
    return nodo_raiz


print("Bienvenido al Juego de Adivinanzas")
print("1 Construir arbol")
print("2 Importar arbol")
opcion = input("Eliga una opcion: ")
if opcion == '1':
    raiz = construir_arbol()

elif opcion == '2':
    archivo = input("Ingrese el nombre del archivo: ")
    raiz = importar_arbol(archivo)
else:
    print("Opción inválida")

jugar_de_nuevo = "si"
while jugar_de_nuevo.lower() == "si":
    jugar(raiz)
    jugar_de_nuevo = input("¿Desea jugar de nuevo? (si/no): ")

exportar = input("¿Desea exportar el árbol a un archivo? (si/no): ")
if exportar.lower() == "si":
    archivo = input("Ingrese el nombre del archivo(incluya la extencion TXT): ")
    exportar_arbol(raiz, archivo)
