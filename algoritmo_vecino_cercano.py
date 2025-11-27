import numpy as np
import matplotlib.pyplot as plt
import time
from math import radians, sin, cos, sqrt, atan2
from matplotlib.animation import FuncAnimation

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

    def resolver(self, ciudad_inicio=0, verbose=True):
        if isinstance(ciudad_inicio, str):
            try:
                ciudad_inicio = self.ciudades.index(ciudad_inicio)
            except ValueError:
                print("Ciudad no encontrada.")
                return None
        tiempo_inicio = time.time()
        tour = [ciudad_inicio]
        no_visitadas = set(range(self.n))
        no_visitadas.remove(ciudad_inicio)
        pasos_animacion = [tour.copy()] 
        ciudad_actual = ciudad_inicio
        while no_visitadas:
            candidato = min(no_visitadas, key=lambda c: self.matriz_distancias[ciudad_actual][c])
            tour.append(candidato)
            no_visitadas.remove(candidato)
            ciudad_actual = candidato
            pasos_animacion.append(tour.copy()) 
        tiempo_fin = time.time()
        
        return {
            'tour': tour,
            'longitud': self._calcular_longitud_tour(tour),
            'tiempo': tiempo_fin - tiempo_inicio,
            'pasos': pasos_animacion, 
            'ciudad_inicio': ciudad_inicio
        }

    def resolver_multi_inicio(self):
        mejor_res = None
        mejor_len = float('inf')
        for i in range(self.n):
            res = self.resolver(i, verbose=False)
            if res['longitud'] < mejor_len:
                mejor_len = res['longitud']
                mejor_res = res
        return {'mejor': mejor_res}

    def visualizar_solucion(self, resultado, ruta_guardado='solucion_heuristica.png', mostrar=True):
        if not resultado: return
        tour = resultado['tour']
        fig, ax = plt.subplots(figsize=(10, 8))
        
        ax.scatter(self.coordenadas[:, 1], self.coordenadas[:, 0], c='blue', s=100, zorder=5)
        ax.scatter(self.coordenadas[tour[0], 1], self.coordenadas[tour[0], 0], c='gold', s=150, marker='*', zorder=6, label='Inicio')
        
        for i, txt in enumerate(self.ciudades):
            ax.annotate(txt, (self.coordenadas[i, 1], self.coordenadas[i, 0]), xytext=(5, 5), textcoords='offset points')

        tour_ext = tour + [tour[0]]
        coords = self.coordenadas[tour_ext]
        ax.plot(coords[:, 1], coords[:, 0], 'b--', linewidth=2, label='Ruta Heurística')
        
        ax.set_title(f"Solución Heurística (Vecino Más Cercano): {resultado['longitud']:.2f} km\nTiempo: {resultado['tiempo']:.4f}s")
        ax.legend()
        
        if ruta_guardado: plt.savefig(ruta_guardado)
        if mostrar: plt.show()
        else: plt.close()

    def animar_construccion(self, resultado, nombre_archivo='animacion_heuristica.gif'):
        """Crea un GIF mostrando cómo se construye la ruta paso a paso"""
        pasos = resultado['pasos']
        fig, ax = plt.subplots(figsize=(10, 8))
        
        def update(frame):
            ax.clear()
            tour_parcial = pasos[frame]
            
            # Puntos base
            ax.scatter(self.coordenadas[:, 1], self.coordenadas[:, 0], c='gray', s=50, alpha=0.5)
            
            # Puntos visitados hasta el momento
            visitados_idx = tour_parcial
            coords_vis = self.coordenadas[visitados_idx]
            ax.scatter(coords_vis[:, 1], coords_vis[:, 0], c='blue', s=100, zorder=5)
            
            # Etiquetas
            for i in range(self.n):
                color_txt = 'black' if i in visitados_idx else 'gray'
                ax.annotate(self.ciudades[i], (self.coordenadas[i, 1], self.coordenadas[i, 0]), color=color_txt)
            
            # Líneas del tour parcial
            if len(tour_parcial) > 1:
                ax.plot(coords_vis[:, 1], coords_vis[:, 0], 'b-', linewidth=2)
            
            # Si es el último frame, cerramos el ciclo
            if frame == len(pasos) - 1:
                coords_finales = self.coordenadas[tour_parcial + [tour_parcial[0]]]
                ax.plot(coords_finales[:, 1], coords_finales[:, 0], 'b--', linewidth=2)
                titulo = f"Heurística completada: {resultado['longitud']:.2f} km"
            else:
                titulo = f"Paso {frame+1}: Visitando {self.ciudades[tour_parcial[-1]]}"
            
            ax.set_title(titulo)

        # Añadimos un frame extra al final para pausa
        frames_total = len(pasos)
        ani = FuncAnimation(fig, update, frames=frames_total, interval=600, repeat_delay=2000)
        ani.save(nombre_archivo, writer='pillow', fps=1.5)
        print(f"Animación guardada como: {nombre_archivo}")
        plt.close()
