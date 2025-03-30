import time
#nodo (estado del puzzle)
class Nodo(object):
    def __init__(self, dato, anterior, siguiente):
        self.dato=dato
        self.anterior=anterior
        self.siguiente=siguiente

#lista doblemente enlazada
class ListaDoble(object):
    cabeza=None
    cola=None
    mejor=None
    explorado=0

    def agregar(self, dato):
        nuevo_nodo = Nodo(dato, None, None)
        if self.cabeza is None:
            self.cabeza = self.cola = self.mejor = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.mejor
            nuevo_nodo.siguiente = None
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo

    def obtener(self):
        nodo_actual = self.mejor
        while nodo_actual is not None:
            yield nodo_actual.dato
            nodo_actual = nodo_actual.anterior

    def mejorNodo(self):
        costoTotal=0
        m=1000
        heuristica=0
        nm=m

        i=self.cabeza
        while i is not None:
            costoTotal = i.dato.heuristica + i.dato.costo           
            if(i.dato.explorado==0 and costoTotal<m):
                m=costoTotal
            i=i.siguiente

        i=self.cabeza
        while i is not None:
            costoTotal = i.dato.heuristica + i.dato.costo
            heuristica = i.dato.heuristica
            if(i.dato.explorado==0 and costoTotal==m and heuristica  <nm):
                self.mejor = i
                nm=heuristica
            i=i.siguiente

        self.explorado = self.explorado + 1
        self.mejor.dato.explorado = self.explorado

#Escenario de juego
class Puzzle(object):
    coordenadas_x = [1,1,1,2,2,2,3,3,3]
    coordenadas_y = [1,2,3,1,2,3,1,2,3]
    fichas = ["1","2","3","4","5","6","7","8"]
    movPosibles = [[1,3,9,9],
                   [0,2,4,9],
                   [1,5,9,9],
                   [0,4,6,9],
                   [1,3,5,7,9],
                   [2,4,8,9],
                   [3,7,9,9],
                   [4,6,8,9],
                   [5,7,9,9]]
    
    def __init__(self):
        self.estado = None
        self.heuristica = 0
        self.costo = 0
        self.explorado = 0
        self.ascendiente = None

    def posicion_x(self,coordenada):
        return self.coordenadas_x[self.estado.index(coordenada)]
    
    def posicion_y(self,coordenada):
        return self.coordenadas_y[self.estado.index(coordenada)]
    
    def distanciaManhatan(self,meta):
        suma = 0
        for j in self.fichas:
            disManX = abs(self.posicion_x(j) - meta.posicion_x(j))
            disManY = abs(self.posicion_y(j) - meta.posicion_y(j))
            suma = suma + disManX + disManY
        return suma
    
    def descendientes(self):
        vacioIndex = self.estado.index(" ")
        estAnterior = self.ascendiente
        descendientesList = list()
        j = 0
        while(self.movPosibles[vacioIndex][j] != 9):
            estActual = self.estado[:]
            estActual[vacioIndex] = self.estado[self.movPosibles[vacioIndex][j]]
            estActual[self.movPosibles[vacioIndex][j]] = " "
            j = j + 1
            if( estActual != estAnterior ):
                descendientesList.append(estActual)
        return descendientesList
    
    def imprimirPuzzle(self):
        print('  '.join(self.estado[0:3]))
        print('  '.join(self.estado[3:6]))
        print('  '.join(self.estado[6:9]))
        print('')
        print("Heurística: {}.  Costo: {}.  Costo total: {}.  Nodos visitados: {}".format(self.heuristica, self.costo, self.heuristica + self.costo, self.explorado))
        print("_____")
        print('')

if __name__ == "__main__":
    estados = []
    listaDoble = ListaDoble()
    estado_inicial = Puzzle()
    estado_final = Puzzle()

    estado_inicial.estado = list(input("Ingrese el estado inicial (considere el espacio vacío como la tecla espacio): "))
    estado_final.estado = list(input("Ingrese el estado final: "))

    tiempoInicio = time.time()

    estado_inicial.heuristica = estado_inicial.distanciaManhatan(estado_final)
    estado_inicial.costo = 0
    estado_inicial.explorado = 1

    print("")
    print("Estado inicial:")
    estado_inicial.imprimirPuzzle()
    print("Estado final:")
    estado_final.imprimirPuzzle()
    print("Solución:")

    listaDoble.agregar(estado_inicial)
    listaDoble.mejorNodo()
    mejorNodo = listaDoble.mejor.dato
    
    j=0
    while (j < 10000 and mejorNodo.estado != estado_final.estado):
    #obtiene descendientes del mejor nodo y los agrega a la lista
        for hijo in mejorNodo.descendientes():
            elemento = Puzzle()
            elemento.estado = hijo
            elemento.heuristica = elemento.distanciaManhatan(estado_final)
            elemento.costo = mejorNodo.costo + 1
            elemento.explorado = 0
            elemento.ascendiente = mejorNodo.estado
            listaDoble.agregar(elemento)
        #obtiene el mejor nodo de la lista
        listaDoble.mejorNodo()
        mejorNodo = listaDoble.mejor.dato 
        j=j+1

        
    for v in listaDoble.obtener():
      estados.append(v)

    estados.reverse()
  
    for e in estados:
         e.imprimirPuzzle()

    tiempoFinal = time.time()
    print("El tiempo de ejecución fue de " + str((tiempoFinal-tiempoInicio)/1000000) + " segundos.")
