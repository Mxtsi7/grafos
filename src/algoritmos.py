"""
Algoritmos para el Problema del Viajante (TSP)
"""

import itertools
import numpy as np


def calcular_distancia_ruta(ruta, matriz_distancias):
    """
    Calcula la distancia total de una ruta dada.
    
    Args:
        ruta: Lista de índices de ciudades en orden de visita
        matriz_distancias: Matriz de distancias entre ciudades
    
    Returns:
        float: Distancia total de la ruta (incluyendo regreso al origen)
    """
    distancia_total = 0
    n = len(ruta)
    
    for i in range(n):
        ciudad_actual = ruta[i]
        ciudad_siguiente = ruta[(i + 1) % n]  # Volver al inicio
        distancia_total += matriz_distancias[ciudad_actual][ciudad_siguiente]
    
    return distancia_total


def busqueda_exhaustiva(matriz_distancias):
    """
    Encuentra la ruta óptima usando búsqueda exhaustiva (fuerza bruta).
    Prueba todas las permutaciones posibles.
    
    Args:
        matriz_distancias: Matriz NxN de distancias entre ciudades
    
    Returns:
        tuple: (mejor_ruta, distancia_minima)
    """
    n = len(matriz_distancias)
    ciudades = list(range(n))
    
    # Fijar la primera ciudad (por simetría)
    ciudad_inicial = ciudades[0]
    ciudades_restantes = ciudades[1:]
    
    mejor_ruta = None
    distancia_minima = float('inf')
    
    # Probar todas las permutaciones de las ciudades restantes
    for permutacion in itertools.permutations(ciudades_restantes):
        ruta = [ciudad_inicial] + list(permutacion)
        distancia = calcular_distancia_ruta(ruta, matriz_distancias)
        
        if distancia < distancia_minima:
            distancia_minima = distancia
            mejor_ruta = ruta
    
    return mejor_ruta, distancia_minima


def vecino_mas_cercano(matriz_distancias, ciudad_inicial=0):
    """
    Algoritmo del vecino más cercano (greedy heuristic).
    En cada paso, visita la ciudad no visitada más cercana.
    
    Args:
        matriz_distancias: Matriz NxN de distancias entre ciudades
        ciudad_inicial: Índice de la ciudad de inicio (default: 0)
    
    Returns:
        tuple: (ruta, distancia_total)
    """
    n = len(matriz_distancias)
    visitadas = {ciudad_inicial}
    ruta = [ciudad_inicial]
    ciudad_actual = ciudad_inicial
    
    # Visitar todas las ciudades
    while len(visitadas) < n:
        distancia_minima = float('inf')
        ciudad_mas_cercana = None
        
        # Buscar la ciudad no visitada más cercana
        for ciudad in range(n):
            if ciudad not in visitadas:
                distancia = matriz_distancias[ciudad_actual][ciudad]
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    ciudad_mas_cercana = ciudad
        
        # Moverse a la ciudad más cercana
        visitadas.add(ciudad_mas_cercana)
        ruta.append(ciudad_mas_cercana)
        ciudad_actual = ciudad_mas_cercana
    
    # Calcular distancia total
    distancia_total = calcular_distancia_ruta(ruta, matriz_distancias)
    
    return ruta, distancia_total


def obtener_todas_rutas(n_ciudades, max_rutas=None):
    """
    Genera todas las rutas posibles (útil para animaciones).
    
    Args:
        n_ciudades: Número de ciudades
        max_rutas: Máximo número de rutas a generar (None = todas)
    
    Returns:
        list: Lista de todas las rutas
    """
    ciudades = list(range(n_ciudades))
    ciudad_inicial = ciudades[0]
    ciudades_restantes = ciudades[1:]
    
    todas_rutas = []
    
    for i, permutacion in enumerate(itertools.permutations(ciudades_restantes)):
        if max_rutas and i >= max_rutas:
            break
        ruta = [ciudad_inicial] + list(permutacion)
        todas_rutas.append(ruta)
    
    return todas_rutas
