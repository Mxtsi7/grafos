#!/usr/bin/env python3
"""
Problema del Viajante (TSP) - Programa Principal
Curso: Teoría de Grafos - INFO1158
"""

import os
import time
from src.algoritmos import busqueda_exhaustiva, vecino_mas_cercano
from src.visualizacion import visualizar_ruta, crear_animacion_busqueda
from src.utils import cargar_ciudades, calcular_matriz_distancias, guardar_resultados


def main():
    print("="*60)
    print("  PROBLEMA DEL VIAJANTE (TSP)")
    print("  Teoría de Grafos - INFO1158")
    print("="*60)
    print()
    
    # Crear carpeta de resultados si no existe
    os.makedirs('resultados', exist_ok=True)
    
    # Cargar datos de ciudades
    print("[1] Cargando coordenadas de ciudades...")
    coordenadas = cargar_ciudades('data/ciudades_ejemplo.csv')
    n_ciudades = len(coordenadas)
    print(f"    ✓ {n_ciudades} ciudades cargadas\n")
    
    # Calcular matriz de distancias
    print("[2] Calculando matriz de distancias...")
    matriz_distancias = calcular_matriz_distancias(coordenadas)
    print(f"    ✓ Matriz {n_ciudades}x{n_ciudades} calculada\n")
    
    # Algoritmo de búsqueda exhaustiva
    print("[3] Ejecutando búsqueda exhaustiva...")
    inicio = time.time()
    mejor_ruta_exhaustiva, distancia_exhaustiva = busqueda_exhaustiva(matriz_distancias)
    tiempo_exhaustiva = time.time() - inicio
    print(f"    ✓ Mejor ruta: {mejor_ruta_exhaustiva}")
    print(f"    ✓ Distancia total: {distancia_exhaustiva:.2f}")
    print(f"    ✓ Tiempo de ejecución: {tiempo_exhaustiva:.4f} segundos\n")
    
    # Algoritmo del vecino más cercano
    print("[4] Ejecutando algoritmo del vecino más cercano...")
    inicio = time.time()
    ruta_nn, distancia_nn = vecino_mas_cercano(matriz_distancias, ciudad_inicial=0)
    tiempo_nn = time.time() - inicio
    print(f"    ✓ Ruta encontrada: {ruta_nn}")
    print(f"    ✓ Distancia total: {distancia_nn:.2f}")
    print(f"    ✓ Tiempo de ejecución: {tiempo_nn:.4f} segundos\n")
    
    # Comparación de resultados
    print("[5] Comparación de algoritmos:")
    print(f"    Diferencia de distancia: {abs(distancia_exhaustiva - distancia_nn):.2f}")
    print(f"    Factor de velocidad: {tiempo_exhaustiva/tiempo_nn:.2f}x más rápido (NN)\n")
    
    # Visualización
    print("[6] Generando visualizaciones...")
    visualizar_ruta(coordenadas, mejor_ruta_exhaustiva, 
                   titulo="Mejor Ruta - Búsqueda Exhaustiva",
                   archivo="resultados/ruta_exhaustiva.png")
    visualizar_ruta(coordenadas, ruta_nn,
                   titulo="Ruta - Vecino Más Cercano",
                   archivo="resultados/ruta_vecino_cercano.png")
    print("    ✓ Visualizaciones guardadas en /resultados\n")
    
    # Guardar resultados
    print("[7] Guardando resultados...")
    resultados = {
        'n_ciudades': n_ciudades,
        'exhaustiva': {
            'ruta': mejor_ruta_exhaustiva,
            'distancia': distancia_exhaustiva,
            'tiempo': tiempo_exhaustiva
        },
        'vecino_cercano': {
            'ruta': ruta_nn,
            'distancia': distancia_nn,
            'tiempo': tiempo_nn
        }
    }
    guardar_resultados(resultados, 'resultados/resultados.json')
    print("    ✓ Resultados guardados en resultados.json\n")
    
    print("="*60)
    print("  ✓ Proceso completado exitosamente")
    print("="*60)


if __name__ == "__main__":
    main()
