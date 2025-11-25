"""
Algoritmos de búsqueda en grafos
Contiene todas las funciones de búsqueda sin cambios en su lógica
"""

import random
import math
from collections import deque

def busqueda_amplitud(grafo, nodo_ini, nodo_fin):
    """Búsqueda en amplitud (BFS)"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    visitados = set()
    cola = deque([(nodo_ini, [nodo_ini], 0)])
    nodos_expandidos = 0
    
    while cola:
        nodo_actual, camino, costo_acumulado = cola.popleft()
        nodos_expandidos += 1
        
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}
        
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual].items():
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    nuevo_costo = costo_acumulado + peso
                    cola.append((vecino, nuevo_camino, nuevo_costo))
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_costo_uniforme(grafo, nodo_ini, nodo_fin):
    """Búsqueda de costo uniforme (Dijkstra)"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    dist = {nodo: float('inf') for nodo in grafo.keys()}
    prev = {nodo: None for nodo in grafo.keys()}
    dist[nodo_ini] = 0
    
    Q = list(grafo.keys())
    nodos_expandidos = 0
    
    while Q:
        u = min(Q, key=lambda x: dist[x])
        Q.remove(u)
        nodos_expandidos += 1
        
        if u == nodo_fin:
            camino = []
            nodo_actual = nodo_fin
            while nodo_actual is not None:
                camino.insert(0, nodo_actual)
                nodo_actual = prev[nodo_actual]
            
            return {'exito': True, 'camino': camino, 'costo': dist[nodo_fin], 'nodos_expandidos': nodos_expandidos}
        
        if u in grafo:
            for v, peso in grafo[u].items():
                alt = dist[u] + peso
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_profundidad(grafo, nodo_ini, nodo_fin):
    """Búsqueda en profundidad (DFS)"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    visitados = set()
    pila = [(nodo_ini, [nodo_ini], 0)]
    nodos_expandidos = 0
    
    while pila:
        nodo_actual, camino, costo_acumulado = pila.pop()
        nodos_expandidos += 1
        
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}
        
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual].items():
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    nuevo_costo = costo_acumulado + peso
                    pila.append((vecino, nuevo_camino, nuevo_costo))
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_profundidad_limitada(grafo, nodo_ini, nodo_fin, limite):
    """Búsqueda en profundidad con límite"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    visitados = set()
    pila = [(nodo_ini, [nodo_ini], 0, 0)]
    nodos_expandidos = 0
    
    while pila:
        nodo_actual, camino, costo_acumulado, profundidad = pila.pop()
        nodos_expandidos += 1
        
        if profundidad > limite:
            continue
        
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}
        
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual].items():
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    nuevo_costo = costo_acumulado + peso
                    pila.append((vecino, nuevo_camino, nuevo_costo, profundidad + 1))
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_profundidad_iterativa(grafo, nodo_ini, nodo_fin, max_profundidad=10):
    """Búsqueda en profundidad iterativa"""
    for limite in range(max_profundidad + 1):
        resultado = busqueda_profundidad_limitada(grafo, nodo_ini, nodo_fin, limite)
        if resultado['exito']:
            return resultado
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': 0}

def busqueda_codiciosa(grafo, nodo_ini, nodo_fin, heuristica):
    """Búsqueda codiciosa (Greedy)"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    visitados = set()
    cola = [(nodo_ini, [nodo_ini], 0)]
    nodos_expandidos = 0
    
    while cola:
        cola.sort(key=lambda x: heuristica[x[0]])
        nodo_actual, camino, costo_acumulado = cola.pop(0)
        nodos_expandidos += 1
        
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}
        
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual].items():
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    nuevo_costo = costo_acumulado + peso
                    cola.append((vecino, nuevo_camino, nuevo_costo))
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_a_estrella(grafo, nodo_ini, nodo_fin, heuristica):
    """Búsqueda A*"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    visitados = set()
    cola = [(nodo_ini, [nodo_ini], 0)]
    nodos_expandidos = 0
    
    while cola:
        cola.sort(key=lambda x: x[2] + heuristica[x[0]])
        nodo_actual, camino, costo_acumulado = cola.pop(0)
        nodos_expandidos += 1
        
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}
        
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual].items():
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    nuevo_costo = costo_acumulado + peso
                    cola.append((vecino, nuevo_camino, nuevo_costo))
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_a_estrella_ponderado(grafo, nodo_ini, nodo_fin, heuristica, W=1.3):
    """Búsqueda A* ponderado"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    visitados = set()
    cola = [(nodo_ini, [nodo_ini], 0)]
    nodos_expandidos = 0
    
    while cola:
        cola.sort(key=lambda x: x[2] + W * heuristica[x[0]])
        nodo_actual, camino, costo_acumulado = cola.pop(0)
        nodos_expandidos += 1
        
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}
        
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual].items():
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    nuevo_costo = costo_acumulado + peso
                    cola.append((vecino, nuevo_camino, nuevo_costo))
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_beam(grafo, nodo_ini, nodo_fin, heuristica, ancho_haz=2):
    """Búsqueda Beam"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    camino = [(nodo_ini, [nodo_ini], 0)]
    nodos_expandidos = 0
    max_iteraciones = 20
    
    for iteracion in range(max_iteraciones):
        if not camino:
            break
        
        camino.sort(key=lambda x: heuristica[x[0]])
        camino = camino[:ancho_haz]
        
        nodo_actual, camino_actual, costo_actual = camino[0]
        nodos_expandidos += 1
        
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino_actual, 'costo': costo_actual, 'nodos_expandidos': nodos_expandidos}
        
        nuevos_caminos = []
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual].items():
                nuevo_camino = camino_actual + [vecino]
                nuevo_costo = costo_actual + peso
                nuevos_caminos.append((vecino, nuevo_camino, nuevo_costo))
        
        camino.pop(0)
        camino.extend(nuevos_caminos)
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_branch_and_bound(grafo, nodo_ini, nodo_fin):
    """Búsqueda Branch and Bound"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    camino = {0: [nodo_ini]}
    costo_solucion_actual = None
    camino_solucion_actual = None
    nodos_visitados = []
    nodos_expandidos = 0
    
    while camino:
        llave_camino_menor_costo = min(camino.keys())
        camino_actual = camino[llave_camino_menor_costo]
        nodo_actual = camino_actual[-1]
        
        if costo_solucion_actual is None or llave_camino_menor_costo < costo_solucion_actual:
            if nodo_actual not in nodos_visitados:
                nodos_expandidos += 1
                
                if nodo_actual in grafo:
                    sucesores = grafo[nodo_actual]
                    
                    for sucesor, peso in sucesores.items():
                        costo_acumulado = llave_camino_menor_costo + peso
                        camino_actualizado = camino_actual + [sucesor]
                        camino[costo_acumulado] = camino_actualizado
                        
                        if sucesor == nodo_fin:
                            costo_solucion_actual = costo_acumulado
                            camino_solucion_actual = camino_actualizado
                
                nodos_visitados.append(nodo_actual)
            
            del camino[llave_camino_menor_costo]
        else:
            del camino[llave_camino_menor_costo]
    
    if costo_solucion_actual is not None:
        return {'exito': True, 'camino': camino_solucion_actual, 'costo': costo_solucion_actual, 'nodos_expandidos': nodos_expandidos}
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_hill_climbing(grafo, nodo_ini, nodo_fin, heuristica, max_iteraciones=20):
    """Búsqueda Hill Climbing"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    camino = [nodo_ini]
    costo_acumulado = 0
    nodo_actual = nodo_ini
    nodos_expandidos = 0
    
    for iteracion in range(max_iteraciones):
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}
        
        nodos_expandidos += 1
        
        if nodo_actual not in grafo:
            break
        
        mejor_vecino = None
        mejor_heuristica = heuristica[nodo_actual]
        mejor_peso = 0
        
        for vecino, peso in grafo[nodo_actual].items():
            if vecino not in camino and heuristica[vecino] < mejor_heuristica:
                mejor_vecino = vecino
                mejor_heuristica = heuristica[vecino]
                mejor_peso = peso
        
        if mejor_vecino is None:
            break
        
        camino.append(mejor_vecino)
        costo_acumulado += mejor_peso
        nodo_actual = mejor_vecino
    
    if nodo_actual == nodo_fin:
        return {'exito': True, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}
    
    return {'exito': False, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}

def busqueda_random_restart_hill_climbing(grafo, nodo_ini, nodo_fin, heuristica, max_reinicios=3, pasos_por_intento=10):
    """Búsqueda Hill Climbing con reinicios aleatorios"""
    mejor_resultado = None
    intentos_totales = 0
    
    for reinicio in range(max_reinicios):
        inicio_actual = nodo_ini if reinicio == 0 else random.choice(list(grafo.keys()))
        
        resultado = busqueda_hill_climbing(grafo, inicio_actual, nodo_fin, heuristica, pasos_por_intento)
        intentos_totales += resultado['nodos_expandidos']
        
        if resultado['exito']:
            resultado['nodos_expandidos'] = intentos_totales
            return resultado
        
        if mejor_resultado is None or (resultado['camino'] and len(resultado['camino']) > len(mejor_resultado['camino'])):
            mejor_resultado = resultado
    
    if mejor_resultado:
        mejor_resultado['nodos_expandidos'] = intentos_totales
        return mejor_resultado
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': intentos_totales}

def busqueda_simulated_annealing(grafo, nodo_ini, nodo_fin, heuristica, temperatura_inicial=100, tasa_enfriamiento=0.95, max_iteraciones=100):
    """Búsqueda Simulated Annealing"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    camino = [nodo_ini]
    costo_acumulado = 0
    nodo_actual = nodo_ini
    temperatura = temperatura_inicial
    nodos_expandidos = 0
    
    for iteracion in range(max_iteraciones):
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}
        
        nodos_expandidos += 1
        
        if nodo_actual not in grafo:
            break
        
        vecinos = [(v, p) for v, p in grafo[nodo_actual].items() if v not in camino]
        
        if not vecinos:
            break
        
        vecino_elegido, peso = random.choice(vecinos)
        
        delta_e = heuristica[vecino_elegido] - heuristica[nodo_actual]
        
        if delta_e < 0 or random.random() < math.exp(-delta_e / temperatura):
            camino.append(vecino_elegido)
            costo_acumulado += peso
            nodo_actual = vecino_elegido
        
        temperatura *= tasa_enfriamiento
        
        if temperatura < 0.01:
            break
    
    if nodo_actual == nodo_fin:
        return {'exito': True, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}
    
    return {'exito': False, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}