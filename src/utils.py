"""
Funciones auxiliares para el TSP
"""

import numpy as np
import pandas as pd
import json


def calcular_distancia_euclidiana(punto1, punto2):
    """
    Calcula la distancia euclidiana entre dos puntos.
    
    Args:
        punto1: Tupla (x, y)
        punto2: Tupla (x, y)
    
    Returns:
        float: Distancia euclidiana
    """
    return np.sqrt((punto1[0] - punto2[0])**2 + (punto1[1] - punto2[1])**2)


def calcular_matriz_distancias(coordenadas):
    """
    Calcula la matriz de distancias entre todas las ciudades.
    
    Args:
        coordenadas: Lista de tuplas (x, y) con coordenadas de ciudades
    
    Returns:
        numpy.ndarray: Matriz NxN de distancias
    """
    n = len(coordenadas)
    matriz = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                matriz[i][j] = calcular_distancia_euclidiana(
                    coordenadas[i], coordenadas[j]
                )
    
    return matriz


def cargar_ciudades(archivo):
    """
    Carga las coordenadas de ciudades desde un archivo CSV.
    
    Args:
        archivo: Ruta al archivo CSV con columnas 'x' e 'y'
    
    Returns:
        list: Lista de tuplas (x, y)
    """
    df = pd.read_csv(archivo)
    coordenadas = list(zip(df['x'], df['y']))
    return coordenadas


def guardar_resultados(resultados, archivo):
    """
    Guarda los resultados en formato JSON.
    
    Args:
        resultados: Diccionario con los resultados
        archivo: Ruta del archivo JSON de salida
    """
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)


def generar_ciudades_aleatorias(n, rango_x=(0, 100), rango_y=(0, 100), semilla=None):
    """
    Genera coordenadas aleatorias para ciudades.
    
    Args:
        n: Número de ciudades
        rango_x: Tupla (min, max) para coordenadas x
        rango_y: Tupla (min, max) para coordenadas y
        semilla: Semilla para reproducibilidad
    
    Returns:
        list: Lista de tuplas (x, y)
    """
    if semilla is not None:
        np.random.seed(semilla)
    
    x = np.random.uniform(rango_x[0], rango_x[1], n)
    y = np.random.uniform(rango_y[0], rango_y[1], n)
    
    return list(zip(x, y))


def guardar_ciudades_csv(coordenadas, archivo):
    """
    Guarda coordenadas de ciudades en formato CSV.
    
    Args:
        coordenadas: Lista de tuplas (x, y)
        archivo: Ruta del archivo CSV de salida
    """
    df = pd.DataFrame(coordenadas, columns=['x', 'y'])
    df.to_csv(archivo, index=False)
    print(f"Ciudades guardadas en: {archivo}")
