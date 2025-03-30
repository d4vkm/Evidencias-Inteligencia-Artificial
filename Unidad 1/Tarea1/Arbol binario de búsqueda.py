class Nodo:
    def __init__(self, dato):
        self.izquierda = None
        self.derecha = None
        self.dato = dato

class Arbol:
    def __init__(self, dato):
        self.raiz = Nodo(dato)

    #Para crear un arbol vacío:
    """def __init__(self):
        self.raiz = None"""

    def insertarRecursivo(self, nodo, dato):
        if dato < nodo.dato:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(dato)
            else:
                self.insertarRecursivo(nodo.izquierda, dato)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(dato)
            else:
                self.insertarRecursivo(nodo.derecha, dato)

    def insertar(self, dato):
        self.insertarRecursivo(self.raiz, dato)
            
    def vacio(self):
        print (self.raiz is None)
    
    def buscarRecursivo(self, nodo, busqueda):
        if nodo is None:
            return None
        if nodo.dato == busqueda:
            return nodo
        if busqueda < nodo.dato:
            return self.buscarRecursivo(nodo.izquierda, busqueda)
        else:
            return self.buscarRecursivo(nodo.derecha, busqueda)
        
    def buscarNodo(self, nombre):
        return self.buscarRecursivo(self.raiz, nombre)
    
    def imprimirArbol(self, nodo):
        if nodo is not None:
            self.imprimirArbol(nodo.izquierda)
            print(nodo.dato)
            self.imprimirArbol(nodo.derecha)
                    
arbol = Arbol(10)
arbol.insertar(5)
arbol.insertar(15)
arbol.insertar(1)
arbol.insertar(7)
arbol.insertar(13)
arbol.insertar(20)

"""arbolVacio = Arbol()"""

#Da False porque no está vacío:
arbol.vacio()
"""print(arbolVacio.vacio())"""
#Da la dirección en memoria del nodo 5:
print(arbol.buscarNodo(5))
#Da "None" porque no existe
print(arbol.buscarNodo(40))

#Imprime de forma ordenada:
arbol.imprimirArbol(arbol.raiz)
