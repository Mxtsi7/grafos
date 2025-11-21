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

        # Convertir nombre a índice si es necesario
        if isinstance(ciudad_inicio, str):
            try:
                ciudad_inicio = self.ciudades.index(ciudad_inicio)
            except ValueError:
                print(f"[ERROR] La ciudad de inicio '{ciudad_inicio}' no se encuentra en el diccionario de ciudades.")
                return None
        
        if verbose:
            print("="*70)
            print("HEURÍSTICA CONSTRUCTIVA: VECINO MÁS CERCANO")
            print("="*70)
            print(f"Número de ciudades: {self.n}")
            print(f"Ciudad inicial: {self.ciudades[ciudad_inicio]}")
            print(f"Estrategia: GREEDY (en cada paso elige la opción localmente óptima)")
            print(f"Complejidad temporal: O(n²)")
            print("="*70)
        
        tiempo_inicio = time.time()
        
        # PASO 1: Inicializar tour con ciudad inicial
        tour = [ciudad_inicio]
        no_visitadas = set(range(self.n))
        no_visitadas.remove(ciudad_inicio)
        
        # Variables para visualización
        pasos = [tour.copy()]  # Guardar estado después de cada decisión
        decisiones = []  # Guardar información de cada decisión greedy
        
        ciudad_actual = ciudad_inicio
        
        if verbose:
            print(f"\nPASO 0 - Inicialización:")
            print(f"  Tour inicial: [{self.ciudades[ciudad_inicio]}]")
            print(f"  Ciudades por visitar: {len(no_visitadas)}")
        
        # PASO 2: Construcción greedy iterativa
        numero_paso = 1
        while no_visitadas:
            if verbose:
                print(f"\n{'─'*70}")
                print(f"PASO {numero_paso} - Desde {self.ciudades[ciudad_actual]}")
                print(f"{'─'*70}")
            
            # Calcular distancias a todas las ciudades no visitadas
            distancias_a_no_visitadas = {
                ciudad: self.matriz_distancias[ciudad_actual][ciudad] 
                for ciudad in no_visitadas
            }
            
            # DECISIÓN GREEDY: Elegir la ciudad más cercana
            ciudad_mas_cercana = min(distancias_a_no_visitadas, 
                                     key=distancias_a_no_visitadas.get)
            distancia_mas_cercana = distancias_a_no_visitadas[ciudad_mas_cercana]
            
            # Guardar información de la decisión
            info_decision = {
                'paso': numero_paso,
                'desde': ciudad_actual,
                'hacia': ciudad_mas_cercana,
                'distancia': distancia_mas_cercana,
                'opciones': distancias_a_no_visitadas.copy(),
                'num_opciones': len(distancias_a_no_visitadas)
            }
            decisiones.append(info_decision)
            
            if verbose:
                print(f"  Ciudades candidatas ({len(distancias_a_no_visitadas)}):")
                # Mostrar todas las opciones ordenadas por distancia
                for ciudad, dist in sorted(distancias_a_no_visitadas.items(), 
                                          key=lambda x: x[1]):
                    marcador = ">>> ELEGIDA <<<" if ciudad == ciudad_mas_cercana else ""
                    print(f"    {self.ciudades[ciudad]:20s} : {dist:8.2f} km  {marcador}")
                
                print(f"\n  DECISIÓN GREEDY: Ir a {self.ciudades[ciudad_mas_cercana]}")
                print(f"  Razón: Es la ciudad no visitada más cercana ({distancia_mas_cercana:.2f} km)")
            
            # Actualizar tour y conjunto de no visitadas
            tour.append(ciudad_mas_cercana)
            pasos.append(tour.copy())
            no_visitadas.remove(ciudad_mas_cercana)
            ciudad_actual = ciudad_mas_cercana
            
            numero_paso += 1
        
        # PASO 3: Cerrar el ciclo (regresar al inicio)
        distancia_regreso = self.matriz_distancias[tour[-1]][tour[0]]
        longitud_final = self._calcular_longitud_tour(tour)
        
        tiempo_fin = time.time()
        tiempo_ejecucion = tiempo_fin - tiempo_inicio
        
        if verbose:
            print(f"\n{'='*70}")
            print(f"PASO FINAL - Cerrar el ciclo")
            print(f"{'='*70}")
            print(f"  Última ciudad: {self.ciudades[tour[-1]]}")
            print(f"  Regresar a: {self.ciudades[tour[0]]}")
            print(f"  Distancia de regreso: {distancia_regreso:.2f} km")
            
            print("\n" + "="*70)
            print("SOLUCIÓN HEURÍSTICA CONSTRUIDA")
            print("="*70)
            print(f"Ruta π_NN: {' → '.join([self.ciudades[i] for i in tour])} → {self.ciudades[tour[0]]}")
            print(f"Longitud total L_NN: {longitud_final:.2f} km")
            print(f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos")
            print(f"Pasos de construcción: {len(tour)}")
            print(f"Característica: Solución construida greedily (puede no ser óptima)")
            print("="*70)
        
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

        print("="*70)
        print("VECINO MÁS CERCANO - ESTRATEGIA MULTI-INICIO")
        print("="*70)
        print(f"Intentos totales: {self.n} (una por cada ciudad inicial)")
        print(f"Objetivo: Encontrar la mejor solución greedy posible")
        print("="*70)
        
        mejor_resultado = None
        mejor_longitud = float('inf')
        todos_resultados = []
        
        for idx_inicio in range(self.n):
            print(f"\n{'─'*70}")
            print(f"Intento {idx_inicio+1}/{self.n}: Iniciando desde {self.ciudades[idx_inicio]}")
            print(f"{'─'*70}")
            
            resultado = self.resolver(ciudad_inicio=idx_inicio, verbose=verbose)
            
            # Solo si la resolución fue exitosa
            if resultado:
                todos_resultados.append(resultado)
                print(f"  Longitud obtenida: {resultado['longitud']:.2f} km")
                
                if resultado['longitud'] < mejor_longitud:
                    mejor_longitud = resultado['longitud']
                    mejor_resultado = resultado
                    print(f" NUEVA MEJOR SOLUCIÓN")
        
        if not mejor_resultado:
            print("\n[ERROR] No se pudo resolver para ninguna ciudad de inicio.")
            return {'mejor': None, 'todos_intentos': []}
            
        print("\n" + "="*70)
        print("RESULTADO MULTI-INICIO")
        print("="*70)
        print(f"Mejor ciudad inicial: {self.ciudades[mejor_resultado['ciudad_inicio']]}")
        print(f"Mejor longitud: {mejor_resultado['longitud']:.2f} km")
        print(f"Longitudes encontradas:")
        for i, res in enumerate(todos_resultados):
            marcador = "<<<" if res['longitud'] == mejor_longitud else ""
            print(f"  Desde {self.ciudades[res['ciudad_inicio']]:20s}: {res['longitud']:8.2f} km {marcador}")
        print("="*70)
        
        return {
            'mejor': mejor_resultado,
            'todos_intentos': todos_resultados
        }
    
    def visualizar_solucion(self, resultado, ruta_guardado='solucion_heuristica.png'):
        if not resultado: return
        tour = resultado['tour']
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Plotear todas las ciudades
        ax.scatter(self.coordenadas[:, 1], self.coordenadas[:, 0], 
                  c='darkblue', s=300, zorder=5, alpha=0.9,
                  edgecolors='black', linewidths=2)
        
        # Resaltar ciudad inicial con estrella dorada
        idx_inicio = resultado['ciudad_inicio']
        ax.scatter(self.coordenadas[idx_inicio, 1], self.coordenadas[idx_inicio, 0], 
                  c='gold', s=500, zorder=6, marker='*',
                  edgecolors='black', linewidths=3, label='Ciudad Inicial')
        
        # Nombres de ciudades
        for i, ciudad in enumerate(self.ciudades):
            color = 'gold' if i == idx_inicio else 'white'
            ax.annotate(ciudad, (self.coordenadas[i, 1], self.coordenadas[i, 0]), 
                       xytext=(10, 10), textcoords='offset points', 
                       fontsize=11, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor=color, alpha=0.8))
        
        # Dibujar la ruta heurística
        tour_extendido = tour + [tour[0]]
        coordenadas_tour = self.coordenadas[tour_extendido]
        ax.plot(coordenadas_tour[:, 1], coordenadas_tour[:, 0], 
               c='blue', linewidth=3, alpha=0.8, zorder=3, label='Ruta Heurística (Greedy)')
        
        # Flechas direccionales y numeración
        for i in range(len(tour)):
            inicio = tour[i]
            fin = tour[(i+1) % len(tour)]
            
            # Flecha
            ax.annotate('', 
                       xy=(self.coordenadas[fin, 1], self.coordenadas[fin, 0]),
                       xytext=(self.coordenadas[inicio, 1], self.coordenadas[inicio, 0]),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='blue', alpha=0.7))
            
            # Número de paso en el punto medio
            medio_x = (self.coordenadas[inicio, 1] + self.coordenadas[fin, 1]) / 2
            medio_y = (self.coordenadas[inicio, 0] + self.coordenadas[fin, 0]) / 2
            ax.text(medio_x, medio_y, str(i+1), 
                   fontsize=10, color='white', fontweight='bold',
                   bbox=dict(boxstyle='circle', facecolor='blue', alpha=0.9))
        
        ax.set_title(f'HEURÍSTICA CONSTRUCTIVA: VECINO MÁS CERCANO\n'
                    f'Longitud L_NN = {resultado["longitud"]:.2f} km | '
                    f'Tiempo: {resultado["tiempo"]*1000:.2f} ms | '
                    f'Inicio: {self.ciudades[idx_inicio]}',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Longitud (grados)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Latitud (grados)', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=12, loc='best')
        
        plt.tight_layout()
        
        if ruta_guardado:
            plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
            print(f"\n Visualización guardada: {ruta_guardado}")
        
        plt.show()
    
    def animar_construccion(self, resultado, ruta_guardado='animacion_construccion.gif'):
        if not resultado: 
            print("No se pudo resolver el TSP, no se genera animación.")
            return

        pasos = resultado['pasos']
        decisiones = resultado['decisiones']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        
        def actualizar(cuadro):
            ax1.clear()
            ax2.clear()
            
            tour_actual = pasos[cuadro]
            
            # Ciudades no visitadas (gris claro)
            ax1.scatter(self.coordenadas[:, 1], self.coordenadas[:, 0], 
                       c='lightgray', s=250, zorder=3, alpha=0.5,
                       edgecolors='gray', linewidths=1)
            
            # Ciudades visitadas (azul)
            if tour_actual:
                coordenadas_visitadas = self.coordenadas[tour_actual]
                ax1.scatter(coordenadas_visitadas[:, 1], coordenadas_visitadas[:, 0], 
                           c='blue', s=300, zorder=5, alpha=0.9,
                           edgecolors='black', linewidths=2)
            
            # Nombres de ciudades
            for i, ciudad in enumerate(self.ciudades):
                if i in tour_actual:
                    color = 'blue'
                    peso = 'bold'
                    tamanio = 11
                else:
                    color = 'gray'
                    peso = 'normal'
                    tamanio = 9
                ax1.annotate(ciudad, (self.coordenadas[i, 1], self.coordenadas[i, 0]), 
                           xytext=(6, 6), textcoords='offset points', 
                           fontsize=tamanio, fontweight=peso, color=color)
            
            # Ruta construida hasta el momento
            if len(tour_actual) > 1:
                coordenadas_tour = self.coordenadas[tour_actual]
                ax1.plot(coordenadas_tour[:, 1], coordenadas_tour[:, 0], 
                        c='blue', linewidth=3, alpha=0.7, zorder=4)
                
                # Resaltar ÚLTIMA conexión agregada (en verde)
                if len(tour_actual) >= 2:
                    ultimos_dos = self.coordenadas[tour_actual[-2:]]
                    ax1.plot(ultimos_dos[:, 1], ultimos_dos[:, 0], 
                            c='green', linewidth=5, alpha=0.9, zorder=4.5,
                            label='Última decisión greedy')
            
            # En el último cuadro, cerrar el ciclo
            if cuadro == len(pasos) - 1:
                ax1.plot([self.coordenadas[tour_actual[-1], 1], self.coordenadas[tour_actual[0], 1]],
                        [self.coordenadas[tour_actual[-1], 0], self.coordenadas[tour_actual[0], 0]],
                        c='blue', linewidth=3, alpha=0.7, linestyle='--', zorder=4,
                        label='Regreso al inicio')
            
            ax1.set_title(f'Construcción Greedy - Paso {cuadro}/{len(pasos)-1}\n'
                         f'Ciudades visitadas: {len(tour_actual)}/{self.n}', 
                         fontsize=14, fontweight='bold')
            ax1.set_xlabel('Longitud')
            ax1.set_ylabel('Latitud')
            ax1.grid(True, alpha=0.3)
            if len(tour_actual) > 1:
                ax1.legend(fontsize=10)

            ax2.axis('off')
            
            if cuadro > 0 and cuadro <= len(decisiones):
                # Mostrar información de la decisión greedy
                decision = decisiones[cuadro-1]
                
                texto = f"╔{'═'*50}╗\n"
                texto += f"║  PASO {decision['paso']:2d} - DECISIÓN GREEDY{' '*23}║\n"
                texto += f"╠{'═'*50}╣\n\n"
                texto += f"  Ciudad actual: {self.ciudades[decision['desde']]}\n\n"
                texto += f"  Opciones disponibles ({decision['num_opciones']}):\n"
                texto += f"  {'─'*46}\n"
                
                # Mostrar todas las opciones ordenadas
                opciones_ordenadas = sorted(decision['opciones'].items(), 
                                           key=lambda x: x[1])
                
                for idx_ciudad, dist in opciones_ordenadas:
                    if idx_ciudad == decision['hacia']:
                        marcador = "✓✓✓"
                        prefijo = ">>>"
                        sufijo = "<<<"
                    else:
                        marcador = "   "
                        prefijo = "   "
                        sufijo = "   "
                    
                    nombre = self.ciudades[idx_ciudad]
                    texto += f"  {marcador} {prefijo} {nombre:15s}: {dist:7.2f} km {sufijo}\n"
                
                texto += f"\n  {'─'*46}\n"
                texto += f"  DECISIÓN: Viajar a {self.ciudades[decision['hacia']]}\n"
                texto += f"  CRITERIO: Mínima distancia ({decision['distancia']:.2f} km)\n"
                texto += f"  ESTRATEGIA: Greedy (elección localmente óptima)\n"
                
                ax2.text(0.05, 0.5, texto, 
                        fontsize=10, verticalalignment='center',
                        family='monospace',
                        bbox=dict(boxstyle='round,pad=1', facecolor='lightyellow', 
                                 alpha=0.9, edgecolor='orange', linewidth=2))
            
            elif cuadro == 0:
                # Pantalla inicial
                texto = f"╔{'═'*40}╗\n"
                texto += f"║  INICIO DEL ALGORITMO{' '*18}║\n"
                texto += f"╠{'═'*40}╣\n\n"
                texto += f"  Ciudad inicial:\n"
                texto += f"  {self.ciudades[resultado['ciudad_inicio']]}\n\n"
                texto += f"  Algoritmo:\n"
                texto += f"  Vecino Más Cercano (Greedy)\n\n"
                texto += f"  Estrategia:\n"
                texto += f"  En cada paso, ir a la ciudad\n"
                texto += f"  no visitada más cercana\n"
                
                ax2.text(0.1, 0.5, texto, 
                        fontsize=11, verticalalignment='center',
                        family='monospace', fontweight='bold',
                        bbox=dict(boxstyle='round,pad=1', facecolor='lightgreen', 
                                 alpha=0.9, edgecolor='darkgreen', linewidth=2))
            
            else:
                # Pantalla final
                longitud_total = self._calcular_longitud_tour(tour_actual)
                texto = f"╔{'═'*40}╗\n"
                texto += f"║  TOUR COMPLETADO{' '*23}║\n"
                texto += f"╠{'═'*40}╣\n\n"
                texto += f"  Longitud total:\n"
                texto += f"  {longitud_total:.2f} km\n\n"
                texto += f"  Número de pasos:\n"
                texto += f"  {len(tour_actual)}\n\n"
                texto += f"  Tiempo de construcción:\n"
                texto += f"  {resultado['tiempo']*1000:.2f} ms\n\n"
                texto += f"  Nota:\n"
                texto += f"  Solución construida con\n"
                texto += f"  estrategia greedy\n"
                texto += f"  (puede no ser óptima)\n"
                
                ax2.text(0.1, 0.5, texto, 
                        fontsize=11, verticalalignment='center',
                        family='monospace', fontweight='bold',
                        bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', 
                                 alpha=0.9, edgecolor='darkblue', linewidth=2))
        
        animacion = FuncAnimation(fig, actualizar, frames=len(pasos)+1, 
                                 interval=1200, repeat=True)
        
        if ruta_guardado:
            escritor = PillowWriter(fps=1)
            animacion.save(ruta_guardado, writer=escritor)
            print(f" Animación guardada: {ruta_guardado}")
        
        plt.show()
        return animacion
    
    def imprimir_matriz_distancias(self):
        print("\n" + "="*90)
        print("MATRIZ DE DISTANCIAS D (en kilómetros)")
        print("="*90)
        
        # Encabezado
        encabezado = " " * 18 + " | "
        for ciudad in self.ciudades:
            encabezado += f"{ciudad[:12]:>14}"
        print(encabezado)
        print("-" * 90)
        
        # Filas
        for i, ciudad in enumerate(self.ciudades):
            fila = f"{ciudad[:18]:18} | "
            for j in range(self.n):
                if i == j:
                    fila += "       -      "
                else:
                    fila += f"{self.matriz_distancias[i][j]:13.2f} "
            print(fila)
        print("="*90 + "\n")

if __name__ == "__main__":
    
    # PASO 1: Definir el conjunto de ciudades (CON COORDENADAS REALES)
    ciudades = {
        'Nairobi': (-1.2833, 36.8167), # Kenia
        'Osorno': (-40.5739, -73.1360), # Chile
        'Rancagua': (-34.1667, -70.7333), # Chile
        'Pamplona': (42.8167, -1.6500), # España
        'Moscu': (55.7517, 37.6178), # Rusia
        'Orlando': (28.5383, -81.3792), # EE. UU.
        'San Jose': (37.3361, -121.8906) # San José, California, EE. UU.
    }
    
    # PASO 2: Crear instancia del resolvedor heurístico
    resolvedor = TSPVecinoMasCercano(ciudades)
    
    # PASO 3: Mostrar matriz de distancias
    resolvedor.imprimir_matriz_distancias()
    
    # PASO 4: Resolver con heurística desde una ciudad específica
    print("\n" + "="*70)
    print("EJECUCIÓN: Heurística desde ciudad específica")
    print("="*70)
    # COORRECCIÓN: Usar una ciudad que esté en el diccionario
    resultado = resolvedor.resolver(ciudad_inicio='Nairobi', verbose=True)
    
    # Se debe verificar que se obtuvo un resultado antes de intentar visualizar
    if resultado:
        # PASO 5: Visualizar la solución heurística
        resolvedor.visualizar_solucion(resultado, ruta_guardado='solucion_heuristica.png')
        
        # PASO 6: Crear animación del proceso constructivo
        resolvedor.animar_construccion(resultado, ruta_guardado='construccion_greedy.gif')
    
        # PASO 7 (OPCIONAL): Probar multi-inicio para mejor solución
        print("\n\n" + "="*70)
        print("EJECUCIÓN MEJORADA: Multi-inicio")
        print("="*70)
        resultado_multi = resolvedor.resolver_multi_inicio(verbose=False)
        
        # Visualizar la mejor solución encontrada
        if resultado_multi['mejor']:
            resolvedor.visualizar_solucion(resultado_multi['mejor'], 
                                        ruta_guardado='mejor_solucion_heuristica.png')
    
        print("\n" + "="*70)
        print(" HEURÍSTICA CONSTRUCTIVA COMPLETADA")
        print("="*70)
        print("Archivos generados:")
        print("  1. solucion_heuristica.png - Solución desde ciudad específica")
        print("  2. construccion_greedy.gif - Animación del proceso constructivo")
        print("  3. mejor_solucion_heuristica.png - Mejor solución multi-inicio")
        print("="*70)