import numpy as np
import matplotlib.pyplot as plt
import time
import math
from itertools import permutations
from math import radians, sin, cos, sqrt, atan2
from matplotlib.animation import FuncAnimation, PillowWriter

class TSPExhaustivo:
    def __init__(self, datos_ciudades):
        self.ciudades = list(datos_ciudades.keys())
        self.coordenadas = np.array(list(datos_ciudades.values()))
        self.n = len(self.ciudades)
        self.matriz_distancias = self._calcular_matriz_distancias()

    def _distancia_haversine(self, coord1, coord2):
        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        R = 6371.0
        return R * c

    def _calcular_matriz_distancias(self):
        D = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    D[i][j] = self._distancia_haversine(self.coordenadas[i], self.coordenadas[j])
        return D

    def _calcular_longitud_tour(self, tour):
        longitud = 0
        for i in range(len(tour)):
            longitud += self.matriz_distancias[tour[i]][tour[(i+1) % len(tour)]]
        return longitud

    def resolver(self, guardar_proceso=True):
        tiempo_inicio = time.time()
        inicio_fijo = 0
        ciudades_restantes = list(range(1, self.n))
        
        mejor_tour = None
        mejor_longitud = float('inf')
        iteraciones = 0
        
        todos_tours = []
        todas_longitudes = []
        mejor_hasta_ahora = []

        for perm in permutations(ciudades_restantes):
            tour = [inicio_fijo] + list(perm)
            longitud = self._calcular_longitud_tour(tour)
            iteraciones += 1

            if guardar_proceso:
                todos_tours.append(tour.copy())
                todas_longitudes.append(longitud)

            if longitud < mejor_longitud:
                mejor_longitud = longitud
                mejor_tour = tour.copy()
                mejor_hasta_ahora.append((iteraciones, mejor_longitud))

        tiempo_fin = time.time()
        tiempo_ejecucion = tiempo_fin - tiempo_inicio

        return {
            'tour': mejor_tour,
            'longitud': mejor_longitud,
            'tiempo': tiempo_ejecucion,
            'iteraciones': iteraciones,
            'todos_tours': todos_tours if guardar_proceso else None,
            'todas_longitudes': todas_longitudes if guardar_proceso else None,
            'convergencia': mejor_hasta_ahora
        }

    def visualizar_solucion(self, resultado, ruta_guardado='solucion_exhaustiva.png', mostrar=True):
        if not resultado: return
        tour = resultado['tour']
        
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.scatter(self.coordenadas[:, 1], self.coordenadas[:, 0], c='darkred', s=300, zorder=5, alpha=0.9, edgecolors='black')
        
        for i, ciudad in enumerate(self.ciudades):
            ax.annotate(ciudad, (self.coordenadas[i, 1], self.coordenadas[i, 0]), xytext=(8, 8), textcoords='offset points', fontsize=11, fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

        tour_extendido = tour + [tour[0]]
        coordenadas_tour = self.coordenadas[tour_extendido]
        ax.plot(coordenadas_tour[:, 1], coordenadas_tour[:, 0], c='green', linewidth=3, alpha=0.8, zorder=3, label='Ruta Óptima')

        ax.set_title(f'Solución Óptima (Exhaustiva): {resultado["longitud"]:.2f} km', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        if ruta_guardado:
            plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
            print(f"Imagen guardada en: {ruta_guardado}")
        
        if mostrar:
            plt.show()
        else:
            plt.close()

    def visualizar_convergencia(self, resultado, ruta_guardado='convergencia_exhaustiva.png', mostrar=True):
        if not resultado['convergencia']: return
        
        convergencia = resultado['convergencia']
        iteraciones = [x[0] for x in convergencia]
        longitudes = [x[1] for x in convergencia]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(iteraciones, longitudes, marker='o', linewidth=2, markersize=8, color='blue', alpha=0.7)
        ax.axhline(y=resultado['longitud'], color='green', linestyle='--', linewidth=2, label=f'Óptimo: {resultado["longitud"]:.2f} km')
        
        ax.set_title('Convergencia a la Solución Óptima', fontsize=14)
        ax.set_xlabel('Iteración')
        ax.set_ylabel('Longitud (km)')
        ax.grid(True, alpha=0.3)
        
        if ruta_guardado:
            plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
        
        if mostrar:
            plt.show()
        else:
            plt.close()
