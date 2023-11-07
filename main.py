import networkx as nx
import matplotlib.pyplot as plt
import heapq
import matplotlib.pyplot as plt
plt.ion()  # Habilitar modo interactivo


def crear_topologia():
    # Solicitar al usuario el número de nodos
    numero_nodos = int(input("Ingrese el número de nodos: "))

    # Crear un diccionario para almacenar las conexiones entre nodos y sus costos
    grafo = {}

    # Crear un conjunto para rastrear las conexiones que ya han sido ingresadas
    conexiones_registradas = set()

    # Recopilar información de conexiones
    for nodo in range(1, numero_nodos + 1):
        conexiones = input(f"Ingrese los nodos conectados al nodo {nodo} (separados por espacios): ").split()
        conexiones = [int(n) for n in conexiones]

        # Crear una entrada para el nodo en el grafo si no existe
        if nodo not in grafo:
            grafo[nodo] = {}

        for conexion in conexiones:
            # Verificar si la conexión ya ha sido ingresada (ej. A->B o B->A)
            if (nodo, conexion) not in conexiones_registradas and (conexion, nodo) not in conexiones_registradas:
                costo = float(input(f"Ingrese el costo de transmisión entre el nodo {nodo} y el nodo {conexion}: "))
                grafo[nodo][conexion] = costo

                # Registrar la conexión para evitar información redundante
                conexiones_registradas.add((nodo, conexion))
                conexiones_registradas.add((conexion, nodo))

    return grafo


def crear_tabla_enrutamiento(grafo):
    # Supongamos que 'grafo' es tu grafo de conexiones y costos

    # Crear una tabla de enrutamiento
    tabla_enrutamiento = {}

    # Recorrer todos los nodos como posibles orígenes
    for origen in grafo:
        # Usar el algoritmo de Dijkstra para encontrar las rutas más cortas desde 'origen' a todos los demás nodos
        rutas_mas_cortas = {}
        nodos_sin_visitar = set(grafo.keys())

        rutas_mas_cortas[origen] = (0, [origen])  # Costo desde el origen a sí mismo es 0
        while nodos_sin_visitar:
            nodo_actual = None
            for nodo in nodos_sin_visitar:
                if nodo in rutas_mas_cortas:
                    if nodo_actual is None or rutas_mas_cortas[nodo][0] < rutas_mas_cortas[nodo_actual][0]:
                        nodo_actual = nodo

            if nodo_actual is None:
                break

            nodos_sin_visitar.remove(nodo_actual)
            costo_actual, camino_actual = rutas_mas_cortas[nodo_actual]

            for conexion, costo in grafo[nodo_actual].items():
                if conexion not in rutas_mas_cortas:
                    costo_total = costo_actual + costo
                    camino = camino_actual + [conexion]

                    if conexion not in rutas_mas_cortas or costo_total < rutas_mas_cortas[conexion][0]:
                        rutas_mas_cortas[conexion] = (costo_total, camino)

        # Almacenar las rutas más cortas desde 'origen' a todos los demás nodos en la tabla de enrutamiento
        for destino, (costo, camino) in rutas_mas_cortas.items():
            if origen != destino:
                if origen not in tabla_enrutamiento:
                    tabla_enrutamiento[origen] = {}
                if destino not in tabla_enrutamiento[origen] or costo < tabla_enrutamiento[origen][destino][0]:
                    tabla_enrutamiento[origen][destino] = (costo, camino)

    return tabla_enrutamiento

def esbozar_grafico(tabla_enrutamiento):
    # Supongamos que 'tabla_enrutamiento' es tu tabla de enrutamiento

    # Crear un objeto de grafo dirigido con NetworkX
    G = nx.DiGraph()

    # Recorrer la tabla de enrutamiento y agregar arcos al grafo
    for origen, rutas in tabla_enrutamiento.items():
        for destino, (costo, camino) in rutas.items():
            # Agregar un arco desde 'origen' a 'destino' con un atributo de costo
            G.add_edge(origen, destino, weight=costo)

    # Crear una representación gráfica del grafo
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_size=800, node_color='lightblue', font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Mostrar el gráfico
    # Mostrar la gráfica
    plt.title('Tabla de Enrutamiento')
    plt.axis('off')
    plt.pause(0.001)  # Mostrar la gráfica durante 1 ms

    # Luego puedes continuar con otras operaciones, como consultar la tabla de enrutamiento o los caminos


def camino_menos_nodos(grafo, inicio, destino):
    visitados = set()
    cola = [(0, inicio, [])]

    while cola:
        (costo, nodo, camino) = heapq.heappop(cola)

        if nodo in visitados:
            continue

        camino = camino + [nodo]

        if nodo == destino:
            return camino

        visitados.add(nodo)

        for siguiente_nodo in grafo[nodo]:
            if siguiente_nodo not in visitados:
                costo_siguiente = 1  # Cada conexión cuenta como un nodo visitado
                heapq.heappush(cola, (costo + costo_siguiente, siguiente_nodo, camino))

    return []


def camino_menos_costo(grafo, inicio, destino):
    visitados = set()
    cola = [(0, inicio, [])]

    while cola:
        (costo, nodo, camino) = heapq.heappop(cola)

        if nodo in visitados:
            continue

        camino = camino + [nodo]

        if nodo == destino:
            return camino

        visitados.add(nodo)

        for siguiente_nodo in grafo[nodo]:
            if siguiente_nodo not in visitados:
                costo_siguiente = grafo[nodo][siguiente_nodo]
                heapq.heappush(cola, (costo + costo_siguiente, siguiente_nodo, camino))

    return []


def mostrar_tabla_enrutamiento(tabla_enrutamiento):
    # Imprimir la tabla de enrutamiento
    print("Tabla de enrutamiento:")
    for origen, rutas in tabla_enrutamiento.items():
        print(f"Desde el nodo {origen}:")
        for destino, (costo, camino) in rutas.items():
            print(f"- Hacia el nodo {destino}, Costo: {costo}, Camino: {camino}")

def consultar_caminos(grafo):
    inicio = int(input("Ingrese el nodo de inicio: "))
    destino = int(input("Ingrese el nodo de destino: "))

    # Encontrar el camino con menos nodos
    camino_nodos = camino_menos_nodos(grafo, inicio, destino)

    # Encontrar el camino con menos costo
    camino_costo = camino_menos_costo(grafo, inicio, destino)

    print(f"Camino con menos nodos: {camino_nodos}")
    print(f"Camino con menos costo: {camino_costo}")



print("Este programa permite introducir una topología de red basada en nodos "
      "para crear posteriormente una tabla de Routing, esbozar un gráfico de "
      "la misma e inlcuso consultar el mejor camino de un nodo a otro en términos de costo o de menor número de nodos. "
      "Para ello, siga las instrucciones siguientes: ")

while True:
    opcion = input("¿Desea crear una nueva topología, ver el gráfico, consultar la tabla de enrutamiento o salir? (nueva/gráfico/tabla/consulta/salir): ")

    if opcion.lower() == 'salir':
        break

    if opcion.lower() == 'nueva':
        grafo = crear_topologia()
        tabla_enrutamiento = crear_tabla_enrutamiento(grafo)

    if opcion.lower() == 'gráfico':
        esbozar_grafico(tabla_enrutamiento)
        plt.pause(0.001)  # Mostrar la gráfica durante 1 ms

    if opcion.lower() == 'tabla':
        mostrar_tabla_enrutamiento(tabla_enrutamiento)

    if opcion.lower() == 'consulta':
        consultar_caminos(grafo)