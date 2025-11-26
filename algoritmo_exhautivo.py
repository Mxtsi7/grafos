import numpy as np
import matplotlib.pyplot as plt
import time
from itertools import permutations
from math import radians, sin, cos, sqrt, atan2
from matplotlib.animation import FuncAnimation

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
        
        # Guardamos solo una muestra de tours para la animación (ej. cada N iteraciones) para no saturar memoria
        tours_para_animacion = [] 
        
        for perm in permutations(ciudades_restantes):
            tour = [inicio_fijo] + list(perm)
            longitud = self._calcular_longitud_tour(tour)
            iteraciones += 1
            
            if guardar_proceso:
                todos_tours.append(tour.copy())
                todas_longitudes.append(longitud)
                # Guardar cada X iteraciones o si es un nuevo mejor (para la animación)
                if longitud < mejor_longitud or iteraciones % max(1, int(np.math.factorial(self.n-1)/50)) == 0:
                    tours_para_animacion.append((tour.copy(), longitud, longitud < mejor_longitud))

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
            'todos_tours': todos_tours,
            'tours_animacion': tours_para_animacion, # Nueva lista optimizada para GIF
            'convergencia': mejor_hasta_ahora
        }

    def visualizar_solucion(self, resultado, ruta_guardado='solucion_exhaustiva.png', mostrar=True):
        if not resultado: return
        tour = resultado['tour']
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Dibujar ciudades
        ax.scatter(self.coordenadas[:, 1], self.coordenadas[:, 0], c='red', s=100, zorder=5)
        for i, txt in enumerate(self.ciudades):
            ax.annotate(txt, (self.coordenadas[i, 1], self.coordenadas[i, 0]), xytext=(5, 5), textcoords='offset points')
            
        # Dibujar ruta óptima
        tour_ext = tour + [tour[0]]
        coords_tour = self.coordenadas[tour_ext]
        ax.plot(coords_tour[:, 1], coords_tour[:, 0], 'g-', linewidth=2, label='Óptimo Global')
        
        ax.set_title(f"Solución Exhaustiva (Óptima): {resultado['longitud']:.2f} km\nTiempo: {resultado['tiempo']:.4f}s")
        ax.legend()
        
        if ruta_guardado: plt.savefig(ruta_guardado)
        if mostrar: plt.show()
        else: plt.close()

    def animar_busqueda(self, resultado, nombre_archivo='animacion_exhaustiva.gif'):
        """Genera un GIF mostrando las rutas probadas y cómo encuentra la óptima"""
        if not resultado.get('tours_animacion'):
            print("No hay datos de proceso para animar.")
            return

        datos = resultado['tours_animacion']
        # Limitar frames si son demasiados (máximo 100 frames para que no pese mucho)
        if len(datos) > 100:
            indices = np.linspace(0, len(datos)-1, 100, dtype=int)
            datos = [datos[i] for i in indices]
            # Asegurar que el óptimo final esté incluido
            if resultado['tour'] != datos[-1][0]:
                datos.append((resultado['tour'], resultado['longitud'], True))

        fig, ax = plt.subplots(figsize=(10, 8))
        
        def update(frame):
            ax.clear()
            tour_actual, longitud, es_mejor = datos[frame]
            
            # Fondo estático (Ciudades)
            ax.scatter(self.coordenadas[:, 1], self.coordenadas[:, 0], c='black', s=50, zorder=5)
            for i, txt in enumerate(self.ciudades):
                ax.annotate(txt, (self.coordenadas[i, 1], self.coordenadas[i, 0]))
            
            # Ruta actual
            tour_ext = tour_actual + [tour_actual[0]]
            coords = self.coordenadas[tour_ext]
            
            color = 'green' if es_mejor else 'gray'
            width = 3 if es_mejor else 1
            alpha = 1.0 if es_mejor else 0.4
            
            ax.plot(coords[:, 1], coords[:, 0], color=color, linewidth=width, alpha=alpha)
            titulo = f"Evaluando Ruta: {longitud:.2f} km"
            if es_mejor: titulo += " (¡NUEVO ÓPTIMO!)"
            ax.set_title(titulo)

        ani = FuncAnimation(fig, update, frames=len(datos), interval=200)
        ani.save(nombre_archivo, writer='pillow', fps=5)
        print(f"Animación guardada como: {nombre_archivo}")
        plt.close()
