import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation, PillowWriter
from math import radians, sin, cos, sqrt, atan2

class TSPVecinoMasCercano:
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
        R = 6371.0  # Radio de la Tierra en km
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

    def resolver(self, ciudad_inicio=0, verbose=True):
        if isinstance(ciudad_inicio, str):
            try:
                ciudad_inicio = self.ciudades.index(ciudad_inicio)
            except ValueError:
                print(f"[ERROR] La ciudad de inicio '{ciudad_inicio}' no se encuentra en el diccionario.")
                return None

        if verbose:
            print(f"Iniciando cálculo desde: {self.ciudades[ciudad_inicio]}")

        tiempo_inicio = time.time()
        tour = [ciudad_inicio]
        no_visitadas = set(range(self.n))
        no_visitadas.remove(ciudad_inicio)
        pasos = [tour.copy()]
        decisiones = []
        ciudad_actual = ciudad_inicio

        numero_paso = 1
        while no_visitadas:
            distancias_a_no_visitadas = {
                ciudad: self.matriz_distancias[ciudad_actual][ciudad]
                for ciudad in no_visitadas
            }
            ciudad_mas_cercana = min(distancias_a_no_visitadas, key=distancias_a_no_visitadas.get)
            distancia_mas_cercana = distancias_a_no_visitadas[ciudad_mas_cercana]

            info_decision = {
                'paso': numero_paso,
                'desde': ciudad_actual,
                'hacia': ciudad_mas_cercana,
                'distancia': distancia_mas_cercana,
                'opciones': distancias_a_no_visitadas.copy(),
                'num_opciones': len(distancias_a_no_visitadas)
            }
            decisiones.append(info_decision)
            tour.append(ciudad_mas_cercana)
            pasos.append(tour.copy())
            no_visitadas.remove(ciudad_mas_cercana)
            ciudad_actual = ciudad_mas_cercana
            numero_paso += 1

        distancia_regreso = self.matriz_distancias[tour[-1]][tour[0]]
        longitud_final = self._calcular_longitud_tour(tour)
        tiempo_fin = time.time()
        tiempo_ejecucion = tiempo_fin - tiempo_inicio

        return {
            'tour': tour,
            'longitud': longitud_final,
            'tiempo': tiempo_ejecucion,
            'pasos': pasos,
            'decisiones': decisiones,
            'ciudad_inicio': ciudad_inicio,
            'distancia_regreso': distancia_regreso
        }

    def resolver_multi_inicio(self, verbose=False):
        mejor_resultado = None
        mejor_longitud = float('inf')
        todos_resultados = []

        for idx_inicio in range(self.n):
            resultado = self.resolver(ciudad_inicio=idx_inicio, verbose=verbose)
            if resultado:
                todos_resultados.append(resultado)
                if resultado['longitud'] < mejor_longitud:
                    mejor_longitud = resultado['longitud']
                    mejor_resultado = resultado
        
        return {'mejor': mejor_resultado, 'todos_intentos': todos_resultados}

    def visualizar_solucion(self, resultado, ruta_guardado='solucion_heuristica.png', mostrar=True):
        if not resultado: return
        tour = resultado['tour']
        idx_inicio = resultado['ciudad_inicio']
        
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.scatter(self.coordenadas[:, 1], self.coordenadas[:, 0], c='darkblue', s=300, zorder=5, alpha=0.9, edgecolors='black')
        ax.scatter(self.coordenadas[idx_inicio, 1], self.coordenadas[idx_inicio, 0], c='gold', s=500, zorder=6, marker='*', edgecolors='black', label='Inicio')

        for i, ciudad in enumerate(self.ciudades):
            ax.annotate(ciudad, (self.coordenadas[i, 1], self.coordenadas[i, 0]), xytext=(10, 10), textcoords='offset points', fontsize=11, fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

        tour_extendido = tour + [tour[0]]
        coordenadas_tour = self.coordenadas[tour_extendido]
        ax.plot(coordenadas_tour[:, 1], coordenadas_tour[:, 0], c='blue', linewidth=3, alpha=0.8, zorder=3)

        ax.set_title(f'Ruta Heurística: {resultado["longitud"]:.2f} km', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        if ruta_guardado:
            plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
            print(f"Imagen guardada en: {ruta_guardado}")
        
        if mostrar:
            plt.show()
        else:
            plt.close() # Importante cerrar si no se muestra para liberar memoria
