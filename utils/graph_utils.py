"""
Utilidades para trabajar con grafos
Funciones para leer archivos y generar heurísticas
"""

import re
import random

def leer_grafo(archivo):
    """
    Lee un grafo desde un archivo de texto
    El archivo puede tener diferentes formatos (G.add_edge o líneas simples)
    
    Args:
        archivo: ruta del archivo a leer
    
    Returns:
        dict: diccionario con el grafo (estructura: {nodo: {vecino: peso}})
    """
    grafo = {}
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                
                # Ignorar líneas vacías o comentarios
                if not linea or linea.startswith('#') or linea.startswith('puertos') or linea.startswith('['):
                    continue
                
                # Detectar formato G.add_edge
                if 'G.add_edge' in linea:
                    match = re.search(r"G\.add_edge\('([^']+)',\s*'([^']+)',\s*weight=(\d+(?:\.\d+)?)\)", linea)
                    if match:
                        origen = match.group(1)
                        destino = match.group(2)
                        peso = float(match.group(3))
                    else:
                        continue
                else:
                    # Formato simple: origen, destino, peso
                    partes = linea.split(',')
                    if len(partes) != 3:
                        continue
                    
                    origen = partes[0].strip()
                    destino = partes[1].strip()
                    
                    try:
                        peso = float(partes[2].strip())
                    except ValueError:
                        continue
                
                # Agregar aristas en ambas direcciones (grafo no dirigido)
                if origen not in grafo:
                    grafo[origen] = {}
                grafo[origen][destino] = peso
                
                if destino not in grafo:
                    grafo[destino] = {}
                grafo[destino][origen] = peso
    
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {archivo}")
    except Exception as e:
        raise Exception(f"Error al leer el archivo: {str(e)}")
    
    return grafo

def generar_heuristica(grafo, objetivo, seed=17):
    """
    Genera una heurística aleatoria para cada nodo del grafo
    El nodo objetivo siempre tendrá heurística 0
    
    Args:
        grafo: diccionario con el grafo
        objetivo: nodo objetivo (tendrá heurística 0)
        seed: semilla para números aleatorios
    
    Returns:
        dict: diccionario con la heurística de cada nodo
    """
    random.seed(seed)
    heuristica = {}
    
    # Generar valores aleatorios para todos los nodos
    for nodo in grafo.keys():
        heuristica[nodo] = random.randint(20, 50)
    
    # El objetivo siempre tiene heurística 0
    heuristica[objetivo] = 0
    
    return heuristica

def validar_grafo(grafo):
    """
    Valida que el grafo tenga una estructura correcta
    
    Args:
        grafo: diccionario con el grafo
    
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not grafo:
        return False, "El grafo está vacío"
    
    if len(grafo) < 2:
        return False, "El grafo debe tener al menos 2 nodos"
    
    # Verificar que todos los nodos tengan al menos una arista
    for nodo, vecinos in grafo.items():
        if not vecinos:
            return False, f"El nodo '{nodo}' no tiene conexiones"
    
    return True, "Grafo válido"

def obtener_estadisticas_grafo(grafo):
    """
    Obtiene estadísticas básicas del grafo
    
    Args:
        grafo: diccionario con el grafo
    
    Returns:
        dict: estadísticas del grafo
    """
    num_nodos = len(grafo)
    num_aristas = sum(len(vecinos) for vecinos in grafo.values()) // 2
    
    # Calcular grado promedio
    grados = [len(vecinos) for vecinos in grafo.values()]
    grado_promedio = sum(grados) / num_nodos if num_nodos > 0 else 0
    
    # Calcular peso promedio de aristas
    pesos = []
    for vecinos in grafo.values():
        pesos.extend(vecinos.values())
    peso_promedio = sum(pesos) / len(pesos) if pesos else 0
    
    return {
        'num_nodos': num_nodos,
        'num_aristas': num_aristas,
        'grado_promedio': grado_promedio,
        'peso_promedio': peso_promedio
    }