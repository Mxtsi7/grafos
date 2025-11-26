import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
import time
from matplotlib.animation import FuncAnimation, PillowWriter
from math import radians, sin, cos, sqrt, atan2
import math

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
    
    def resolver(self, guardar_proceso=True):

        print("="*70)
        print("BÚSQUEDA EXHAUSTIVA - MÉTODO EXACTO")
        print("="*70)
        print(f"Ciudades a visitar: {self.n}")
        print(f"Permutaciones totales: {math.factorial(self.n-1):,}")
        print(f"Complejidad: O({self.n}!)")
        print("="*70)
        
        tiempo_inicio = time.time()
        
        # Fijamos ciudad inicial (evita soluciones rotadas equivalentes)
        inicio_fijo = 0
        ciudades_restantes = list(range(1, self.n))
        
        # Variables de seguimiento
        mejor_tour = None
        mejor_longitud = float('inf')
        iteraciones = 0
        
        # Para visualización del proceso
        todos_tours = []
        todas_longitudes = []
        mejor_hasta_ahora = []
        
        print("Iniciando evaluación sistemática...")
        
        # Evaluar cada permutación posible
        for perm in permutations(ciudades_restantes):
            tour = [inicio_fijo] + list(perm)
            longitud = self._calcular_longitud_tour(tour)
            
            iteraciones += 1
            
            if guardar_proceso:
                todos_tours.append(tour.copy())
                todas_longitudes.append(longitud)
            
            # Actualizar mejor solución
            if longitud < mejor_longitud:
                mejor_longitud = longitud
                mejor_tour = tour.copy()
                mejor_hasta_ahora.append((iteraciones, mejor_longitud))
                
                print(f" Nueva mejor solución en iteración {iteraciones}:")
                print(f" Ruta: {' → '.join([self.ciudades[i] for i in mejor_tour])}")
                print(f" Longitud: {mejor_longitud:.2f} km\n")
            
            # Actualización de progreso
            if iteraciones % 500 == 0:
                transcurrido = time.time() - tiempo_inicio
                print(f"[Progreso] {iteraciones:,} rutas evaluadas | "
                      f"Tiempo: {transcurrido:.2f}s | Mejor: {mejor_longitud:.2f} km")
        
        tiempo_fin = time.time()
        tiempo_ejecucion = tiempo_fin - tiempo_inicio
        
        # Resultados finales
        print("\n" + "="*70)
        print("SOLUCIÓN ÓPTIMA ENCONTRADA")
        print("="*70)
        print(f"Ruta óptima π⋆: {' → '.join([self.ciudades[i] for i in mejor_tour])} → {self.ciudades[mejor_tour[0]]}")
        print(f"Longitud L⋆: {mejor_longitud:.2f} km")
        print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")
        print(f"Iteraciones totales: {iteraciones:,}")
        print(f"Promedio por iteración: {(tiempo_ejecucion/iteraciones)*1000:.4f} ms")
        print("="*70)
        
        return {
            'tour': mejor_tour,
            'longitud': mejor_longitud,
            'tiempo': tiempo_ejecucion,
            'iteraciones': iteraciones,
            'todos_tours': todos_tours if guardar_proceso else None,
            'todas_longitudes': todas_longitudes if guardar_proceso else None,
            'convergencia': mejor_hasta_ahora
        }
    
    def visualizar_solucion(self, resultado, ruta_guardado='solucion_exhaustiva.png'):
        tour = resultado['tour']
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Plotear ciudades
        ax.scatter(self.coordenadas[:, 1], self.coordenadas[:, 0], 
                  c='darkred', s=300, zorder=5, alpha=0.9, 
                  edgecolors='black', linewidths=2)
        
        # Nombres de ciudades
        for i, ciudad in enumerate(self.ciudades):
            ax.annotate(ciudad, (self.coordenadas[i, 1], self.coordenadas[i, 0]), 
                       xytext=(8, 8), textcoords='offset points', 
                       fontsize=11, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
        
        # Dibujar ruta óptima
        tour_extendido = tour + [tour[0]]
        coordenadas_tour = self.coordenadas[tour_extendido]
        ax.plot(coordenadas_tour[:, 1], coordenadas_tour[:, 0], 
               c='green', linewidth=3, alpha=0.8, zorder=3, label='Ruta Óptima')
        
        # Flechas direccionales
        for i in range(len(tour)):
            idx_inicio = tour[i]
            idx_fin = tour[(i+1) % len(tour)]
            
            ax.annotate('', 
                       xy=(self.coordenadas[idx_fin, 1], self.coordenadas[idx_fin, 0]),
                       xytext=(self.coordenadas[idx_inicio, 1], self.coordenadas[idx_inicio, 0]),
                       arrowprops=dict(arrowstyle='->', lw=2, color='green', alpha=0.7))
            
            # Numerar orden de visita
            medio_x = (self.coordenadas[idx_inicio, 1] + self.coordenadas[idx_fin, 1]) / 2
            medio_y = (self.coordenadas[idx_inicio, 0] + self.coordenadas[idx_fin, 0]) / 2
            ax.text(medio_x, medio_y, str(i+1), 
                   fontsize=9, color='white', fontweight='bold',
                   bbox=dict(boxstyle='circle', facecolor='green', alpha=0.8))
        
        ax.set_title(f'SOLUCIÓN ÓPTIMA - BÚSQUEDA EXHAUSTIVA\n'
                    f'Longitud L⋆ = {resultado["longitud"]:.2f} km | '
                    f'Tiempo: {resultado["tiempo"]:.4f}s | '
                    f'Iteraciones: {resultado["iteraciones"]:,}',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Longitud', fontsize=12, fontweight='bold')
        ax.set_ylabel('Latitud', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=11, loc='best')
        
        plt.tight_layout()
        
        if ruta_guardado:
            plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
            print(f"\n✓ Visualización guardada: {ruta_guardado}")
        
        plt.show()
    
    def visualizar_convergencia(self, resultado, ruta_guardado='convergencia_exhaustiva.png'):
        if not resultado['convergencia']:
            print("No hay datos de convergencia para visualizar")
            return
        
        convergencia = resultado['convergencia']
        iteraciones = [x[0] for x in convergencia]
        longitudes = [x[1] for x in convergencia]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(iteraciones, longitudes, marker='o', linewidth=2, 
               markersize=8, color='blue', alpha=0.7)
        ax.axhline(y=resultado['longitud'], color='green', linestyle='--', 
                  linewidth=2, label=f'Óptimo Global: {resultado["longitud"]:.2f} km')
        
        ax.set_title('CONVERGENCIA A LA SOLUCIÓN ÓPTIMA', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Iteración', fontsize=12)
        ax.set_ylabel('Mejor Longitud Encontrada (km)', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=11)
        
        plt.tight_layout()
        
        if ruta_guardado:
            plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
            print(f"✓ Gráfico de convergencia guardado: {ruta_guardado}")
        
        plt.show()
    
    def animar_proceso_busqueda(self, resultado, ruta_guardado='animacion_busqueda.gif', 
                               max_cuadros=50):
        """
        Crea animación mostrando el proceso de búsqueda
        Muestra muestras representativas del proceso
        """
        if resultado['todos_tours'] is None:
            print("No se guardó el proceso de búsqueda")
            return
        
        # Seleccionar frames representativos
        total_tours = len(resultado['todos_tours'])
        if total_tours > max_cuadros:
            indices = np.linspace(0, total_tours-1, max_cuadros, dtype=int)
        else:
            indices = list(range(total_tours))
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        mejor_longitud_hasta_ahora = float('inf')
        
        def actualizar(idx_cuadro):
            ax.clear()
            
            idx = indices[idx_cuadro]
            tour_actual = resultado['todos_tours'][idx]
            longitud_actual = resultado['todas_longitudes'][idx]
            
            # Actualizar mejor encontrado
            nonlocal mejor_longitud_hasta_ahora
            if longitud_actual < mejor_longitud_hasta_ahora:
                mejor_longitud_hasta_ahora = longitud_actual
            
            # Ciudades
            ax.scatter(self.coordenadas[:, 1], self.coordenadas[:, 0], 
                      c='red', s=200, zorder=5, alpha=0.8)
            
            # Nombres
            for i, ciudad in enumerate(self.ciudades):
                ax.annotate(ciudad, (self.coordenadas[i, 1], self.coordenadas[i, 0]), 
                           xytext=(5, 5), textcoords='offset points', 
                           fontsize=9, fontweight='bold')
            
            # Ruta actual
            tour_extendido = tour_actual + [tour_actual[0]]
            coordenadas_tour = self.coordenadas[tour_extendido]
            
            # Color según si es mejor o no
            color = 'green' if longitud_actual == mejor_longitud_hasta_ahora else 'gray'
            alfa = 0.9 if longitud_actual == mejor_longitud_hasta_ahora else 0.4
            
            ax.plot(coordenadas_tour[:, 1], coordenadas_tour[:, 0], 
                   c=color, linewidth=2, alpha=alfa, zorder=3)
            
            ax.set_title(f'Búsqueda Exhaustiva - Evaluando Rutas\n'
                        f'Ruta {idx+1}/{total_tours} | '
                        f'Longitud actual: {longitud_actual:.2f} km | '
                        f'Mejor hasta ahora: {mejor_longitud_hasta_ahora:.2f} km',
                        fontsize=12, fontweight='bold')
            ax.set_xlabel('Longitud')
            ax.set_ylabel('Latitud')
            ax.grid(True, alpha=0.3)
        
        animacion = FuncAnimation(fig, actualizar, frames=len(indices), 
                            interval=200, repeat=True)
        
        if ruta_guardado:
            escritor = PillowWriter(fps=5)
            animacion.save(ruta_guardado, writer=escritor)
            print(f"✓ Animación guardada: {ruta_guardado}")
        
        plt.show()
        return animacion
    
    def imprimir_matriz_distancias(self):
        print("\n" + "="*80)
        print("MATRIZ DE DISTANCIAS D (en kilómetros)")
        print("="*80)
        
        # Encabezado
        encabezado = " " * 15 + " | "
        for ciudad in self.ciudades:
            encabezado += f"{ciudad[:10]:>12}"
        print(encabezado)
        print("-" * 80)
        
        # Filas
        for i, ciudad in enumerate(self.ciudades):
            fila = f"{ciudad[:15]:15} | "
            for j in range(self.n):
                if i == j:
                    fila += "      -     "
                else:
                    fila += f"{self.matriz_distancias[i][j]:11.2f} "
            print(fila)
        print("="*80 + "\n")

if __name__ == "__main__":
    
    # Definir ciudades (PERSONALIZA SEGÚN TU PROYECTO)
    ciudades = {
        'Nairobi': (-1.2833, 36.8167), 
        'Osorno': (-40.5739, -73.1360), 
        'Rancagua': (-34.1667, -70.7333), 
        'Pamplona': (42.8167, -1.6500), 
        'Moscu': (55.7517, 37.6178), 
        'Orlando': (28.5383, -81.3792), 
        'San Jose': (37.3361, -121.8906) 
    }
    
    # Crear solver
    resolvedor = TSPExhaustivo(ciudades)
    
    # Mostrar matriz de distancias
    resolvedor.imprimir_matriz_distancias()
    
    # Resolver con búsqueda exhaustiva
    resultado = resolvedor.resolver(guardar_proceso=True)
    
    # Visualizar solución óptima
    resolvedor.visualizar_solucion(resultado, ruta_guardado='tour_optimo.png')
    
    # Visualizar convergencia
    resolvedor.visualizar_convergencia(resultado, ruta_guardado='convergencia.png')
    
    # Crear animación del proceso
    resolvedor.animar_proceso_busqueda(resultado, ruta_guardado='animacion_busqueda.gif', max_cuadros=40)
    
    print(" BÚSQUEDA EXHAUSTIVA COMPLETADA")
    print("Archivos generados:")
    print(" tour_optimo.png")
    print(" convergencia.png")
    print(" animacion_busqueda.gif")