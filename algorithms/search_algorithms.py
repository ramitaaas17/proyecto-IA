"""
Algoritmos de búsqueda en grafos - VERSIÓN MEJORADA
Correcciones y optimizaciones aplicadas
"""

import random
import math
import heapq
from collections import deque

def busqueda_amplitud(grafo, nodo_ini, nodo_fin):
    """Búsqueda en amplitud (BFS) - Optimizada"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    visitados = set()
    cola = deque([(nodo_ini, [nodo_ini], 0)])
    nodos_expandidos = 0
    
    while cola:
        nodo_actual, camino, costo_acumulado = cola.popleft()
        
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        nodos_expandidos += 1
        
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
    """Búsqueda de costo uniforme (Dijkstra) - Optimizada con heapq"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    visitados = set()
    # heap: (costo, contador, nodo, camino)
    contador = 0
    heap = [(0, contador, nodo_ini, [nodo_ini])]
    nodos_expandidos = 0
    
    while heap:
        costo_actual, _, nodo_actual, camino = heapq.heappop(heap)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        nodos_expandidos += 1
        
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino, 'costo': costo_actual, 'nodos_expandidos': nodos_expandidos}
        
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual].items():
                if vecino not in visitados:
                    nuevo_costo = costo_actual + peso
                    nuevo_camino = camino + [vecino]
                    contador += 1
                    heapq.heappush(heap, (nuevo_costo, contador, vecino, nuevo_camino))
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_profundidad(grafo, nodo_ini, nodo_fin, max_profundidad=50):
    """Búsqueda en profundidad (DFS) - Con límite de seguridad"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    visitados = set()
    pila = [(nodo_ini, [nodo_ini], 0, 0)] 
    nodos_expandidos = 0
    
    while pila:
        nodo_actual, camino, costo_acumulado, profundidad = pila.pop()
        
        # Límite de seguridad para evitar ciclos infinitos
        if profundidad > max_profundidad:
            continue
        
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        nodos_expandidos += 1
        
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}
        
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual].items():
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    nuevo_costo = costo_acumulado + peso
                    pila.append((vecino, nuevo_camino, nuevo_costo, profundidad + 1))
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_profundidad_limitada(grafo, nodo_ini, nodo_fin, limite):
    """Búsqueda en profundidad con límite - Corregida"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    visitados = set()
    pila = [(nodo_ini, [nodo_ini], 0, 0)]
    nodos_expandidos = 0
    
    while pila:
        nodo_actual, camino, costo_acumulado, profundidad = pila.pop()
        
        if profundidad > limite:
            continue
        
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        nodos_expandidos += 1
        
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
    """Búsqueda en profundidad iterativa - CORREGIDA"""
    nodos_expandidos_total = 0
    
    for limite in range(max_profundidad + 1):
        resultado = busqueda_profundidad_limitada(grafo, nodo_ini, nodo_fin, limite)
        nodos_expandidos_total += resultado['nodos_expandidos']
        
        if resultado['exito']:
            resultado['nodos_expandidos'] = nodos_expandidos_total
            return resultado
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos_total}

def busqueda_codiciosa(grafo, nodo_ini, nodo_fin, heuristica):
    """Búsqueda codiciosa (Greedy) - Optimizada con heapq"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    visitados = set()
    # heap: (h, contador, nodo, camino, costo)
    contador = 0
    heap = [(heuristica[nodo_ini], contador, nodo_ini, [nodo_ini], 0)]
    nodos_expandidos = 0
    
    while heap:
        _, _, nodo_actual, camino, costo_acumulado = heapq.heappop(heap)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        nodos_expandidos += 1
        
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}
        
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual].items():
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    nuevo_costo = costo_acumulado + peso
                    contador += 1
                    heapq.heappush(heap, (heuristica[vecino], contador, vecino, nuevo_camino, nuevo_costo))
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_a_estrella(grafo, nodo_ini, nodo_fin, heuristica):
    """Búsqueda A* - OPTIMIZADA con heapq"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    visitados = set()
    # heap: (f, contador, nodo, camino, g)
    contador = 0
    h_ini = heuristica.get(nodo_ini, 0)
    heap = [(h_ini, contador, nodo_ini, [nodo_ini], 0)]
    nodos_expandidos = 0
    
    while heap:
        f_actual, _, nodo_actual, camino, g_actual = heapq.heappop(heap)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        nodos_expandidos += 1
        
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino, 'costo': g_actual, 'nodos_expandidos': nodos_expandidos}
        
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual].items():
                if vecino not in visitados:
                    nuevo_g = g_actual + peso
                    h_vecino = heuristica.get(vecino, 0)
                    nuevo_f = nuevo_g + h_vecino
                    nuevo_camino = camino + [vecino]
                    contador += 1
                    heapq.heappush(heap, (nuevo_f, contador, vecino, nuevo_camino, nuevo_g))
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_a_estrella_ponderado(grafo, nodo_ini, nodo_fin, heuristica, W=1.3):
    """Búsqueda A* ponderado - Optimizada"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    visitados = set()
    contador = 0
    h_ini = heuristica.get(nodo_ini, 0)
    heap = [(W * h_ini, contador, nodo_ini, [nodo_ini], 0)]
    nodos_expandidos = 0
    
    while heap:
        _, _, nodo_actual, camino, g_actual = heapq.heappop(heap)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        nodos_expandidos += 1
        
        if nodo_actual == nodo_fin:
            return {'exito': True, 'camino': camino, 'costo': g_actual, 'nodos_expandidos': nodos_expandidos}
        
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual].items():
                if vecino not in visitados:
                    nuevo_g = g_actual + peso
                    h_vecino = heuristica.get(vecino, 0)
                    nuevo_f = nuevo_g + W * h_vecino
                    nuevo_camino = camino + [vecino]
                    contador += 1
                    heapq.heappush(heap, (nuevo_f, contador, vecino, nuevo_camino, nuevo_g))
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_beam(grafo, nodo_ini, nodo_fin, heuristica, ancho_haz=2):
    """Búsqueda Beam - Mejorada"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    nivel_actual = [(heuristica.get(nodo_ini, 0), nodo_ini, [nodo_ini], 0)]
    visitados = set()
    nodos_expandidos = 0
    max_iteraciones = 100
    
    for iteracion in range(max_iteraciones):
        if not nivel_actual:
            break
        
        # Ordenar por heurística y mantener solo los mejores
        nivel_actual.sort(key=lambda x: x[0])
        nivel_actual = nivel_actual[:ancho_haz]
        
        siguiente_nivel = []
        
        for h_actual, nodo_actual, camino, costo in nivel_actual:
            if nodo_actual in visitados:
                continue
            
            visitados.add(nodo_actual)
            nodos_expandidos += 1
            
            if nodo_actual == nodo_fin:
                return {'exito': True, 'camino': camino, 'costo': costo, 'nodos_expandidos': nodos_expandidos}
            
            if nodo_actual in grafo:
                for vecino, peso in grafo[nodo_actual].items():
                    if vecino not in visitados:
                        h_vecino = heuristica.get(vecino, 0)
                        siguiente_nivel.append((
                            h_vecino,
                            vecino,
                            camino + [vecino],
                            costo + peso
                        ))
        
        nivel_actual = siguiente_nivel
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_branch_and_bound(grafo, nodo_ini, nodo_fin):
    """Búsqueda Branch and Bound - Optimizada con heapq"""
    if nodo_ini == nodo_fin:
        return {'exito': True, 'camino': [nodo_ini], 'costo': 0, 'nodos_expandidos': 0}
    
    # heap: (costo, contador, camino)
    contador = 0
    heap = [(0, contador, [nodo_ini])]
    mejor_solucion = None
    mejor_costo = float('inf')
    visitados_con_costo = {}
    nodos_expandidos = 0
    
    while heap:
        costo_actual, _, camino = heapq.heappop(heap)
        nodo_actual = camino[-1]
        
        # Poda por costo
        if costo_actual >= mejor_costo:
            continue
        
        # Poda por visitados con mejor costo
        if nodo_actual in visitados_con_costo and visitados_con_costo[nodo_actual] <= costo_actual:
            continue
        
        visitados_con_costo[nodo_actual] = costo_actual
        nodos_expandidos += 1
        
        if nodo_actual == nodo_fin:
            if costo_actual < mejor_costo:
                mejor_costo = costo_actual
                mejor_solucion = camino
            continue
        
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual].items():
                if vecino not in camino:  # Evitar ciclos
                    nuevo_costo = costo_actual + peso
                    if nuevo_costo < mejor_costo:
                        contador += 1
                        heapq.heappush(heap, (nuevo_costo, contador, camino + [vecino]))
    
    if mejor_solucion:
        return {'exito': True, 'camino': mejor_solucion, 'costo': mejor_costo, 'nodos_expandidos': nodos_expandidos}
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos}

def busqueda_hill_climbing(grafo, nodo_ini, nodo_fin, heuristica, max_iteraciones=20):
    """Búsqueda Hill Climbing - Mejorada"""
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
        mejor_heuristica = heuristica.get(nodo_actual, float('inf'))
        mejor_peso = 0
        
        for vecino, peso in grafo[nodo_actual].items():
            h_vecino = heuristica.get(vecino, float('inf'))
            if vecino not in camino and h_vecino < mejor_heuristica:
                mejor_vecino = vecino
                mejor_heuristica = h_vecino
                mejor_peso = peso
        
        if mejor_vecino is None:
            break
        
        camino.append(mejor_vecino)
        costo_acumulado += mejor_peso
        nodo_actual = mejor_vecino
    
    exito = nodo_actual == nodo_fin
    return {'exito': exito, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}

def busqueda_random_restart_hill_climbing(grafo, nodo_ini, nodo_fin, heuristica, max_reinicios=3, pasos_por_intento=10):
    """Búsqueda Hill Climbing con reinicios aleatorios - Mejorada"""
    mejor_resultado = None
    nodos_expandidos_total = 0
    
    for reinicio in range(max_reinicios):
        inicio_actual = nodo_ini if reinicio == 0 else random.choice(list(grafo.keys()))
        
        resultado = busqueda_hill_climbing(grafo, inicio_actual, nodo_fin, heuristica, pasos_por_intento)
        nodos_expandidos_total += resultado['nodos_expandidos']
        
        if resultado['exito']:
            resultado['nodos_expandidos'] = nodos_expandidos_total
            return resultado
        
        if mejor_resultado is None or (resultado['camino'] and 
           len(resultado['camino']) > len(mejor_resultado.get('camino', []))):
            mejor_resultado = resultado.copy()
    
    if mejor_resultado:
        mejor_resultado['nodos_expandidos'] = nodos_expandidos_total
        return mejor_resultado
    
    return {'exito': False, 'camino': [], 'costo': 0, 'nodos_expandidos': nodos_expandidos_total}

def busqueda_simulated_annealing(grafo, nodo_ini, nodo_fin, heuristica, temperatura_inicial=100, tasa_enfriamiento=0.95, max_iteraciones=100):
    """Búsqueda Simulated Annealing - Mejorada"""
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
        h_actual = heuristica.get(nodo_actual, 0)
        h_vecino = heuristica.get(vecino_elegido, 0)
        
        delta_e = h_vecino - h_actual
        
        if delta_e < 0 or (temperatura > 0 and random.random() < math.exp(-delta_e / temperatura)):
            camino.append(vecino_elegido)
            costo_acumulado += peso
            nodo_actual = vecino_elegido
        
        temperatura *= tasa_enfriamiento
        
        if temperatura < 0.01:
            break
    
    exito = nodo_actual == nodo_fin
    return {'exito': exito, 'camino': camino, 'costo': costo_acumulado, 'nodos_expandidos': nodos_expandidos}