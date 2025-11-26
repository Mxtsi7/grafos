import sys
import time
from algoritmo_vecino_cercano import TSPVecinoMasCercano
from algoritmo_exhautivo import TSPExhaustivo

# === DATOS DE EJEMPLO (Puedes cambiarlos por tus 6-9 ciudades) ===
CIUDADES_DATA = {
    'Nairobi': (-1.2833, 36.8167),
    'Osorno': (-40.5739, -73.1360),
    'Rancagua': (-34.1667, -70.7333),
    'Pamplona': (42.8167, -1.6500),
    'Moscu': (55.7517, 37.6178),
    'Orlando': (28.5383, -81.3792),
    'San Jose': (37.3361, -121.8906)
}

def menu_principal():
    print("\n" + "="*60)
    print(" SISTEMA EXPERTO DE RUTAS - TSP SOLVER (Evaluación 2)")
    print("="*60)
    print("1. Heurística: Vecino Más Cercano (Rápido)")
    print("2. Exacto: Búsqueda Exhaustiva (Óptimo)")
    print("3. COMPARATIVA COMPLETA (Cálculo de GAP y Animaciones)")
    print("4. Salir")
    return input("\nSeleccione opción: ")

def ejecutar_heuristico():
    print("\n--- Heurística Constructiva ---")
    solver = TSPVecinoMasCercano(CIUDADES_DATA)
    res = solver.resolver_multi_inicio()['mejor']
    
    print(f"Mejor ruta encontrada: {res['longitud']:.2f} km")
    solver.visualizar_solucion(res, "heuristica_plot.png")
    
    if input("¿Generar animación GIF? (s/n): ").lower() == 's':
        solver.animar_construccion(res, "animacion_heuristica.gif")

def ejecutar_exhaustivo():
    n = len(CIUDADES_DATA)
    if n > 10:
        print(f"¡Cuidado! {n} ciudades tomarán mucho tiempo.")
        if input("¿Continuar? (s/n): ").lower() != 's': return

    print("\n--- Búsqueda Exhaustiva ---")
    solver = TSPExhaustivo(CIUDADES_DATA)
    print("Calculando...")
    res = solver.resolver()
    
    print(f"Óptimo Global: {res['longitud']:.2f} km")
    solver.visualizar_solucion(res, "exhaustiva_plot.png")
    
    if input("¿Generar animación GIF? (s/n): ").lower() == 's':
        solver.animar_busqueda(res, "animacion_exhaustiva.gif")

def ejecutar_comparativa():
    print("\n" + "*"*50)
    print(" EJECUTANDO ANÁLISIS COMPARATIVO")
    print("*"*50)
    
    # 1. Ejecutar Exhaustivo
    print("1. Ejecutando Método Exacto...")
    solver_ex = TSPExhaustivo(CIUDADES_DATA)
    res_ex = solver_ex.resolver(guardar_proceso=True) # Necesario para animar si se pide
    
    # 2. Ejecutar Heurístico (Multi-inicio para ser justos)
    print("2. Ejecutando Método Heurístico...")
    solver_nn = TSPVecinoMasCercano(CIUDADES_DATA)
    res_nn = solver_nn.resolver_multi_inicio()['mejor']
    
    # 3. Calcular Métricas
    l_opt = res_ex['longitud']
    l_nn = res_nn['longitud']
    gap = ((l_nn - l_opt) / l_opt) * 100
    
    t_ex = res_ex['tiempo']
    t_nn = res_nn['tiempo']
    speedup = t_ex / t_nn if t_nn > 0 else 0
    
    # 4. Reporte
    print("\n" + "-"*50)
    print(" RESULTADOS FINALES")
    print("-"*50)
    print(f"{'Métrica':<20} | {'Exhaustivo (Óptimo)':<20} | {'Vecino Cercano (Heurística)':<20}")
    print("-" * 70)
    print(f"{'Distancia (km)':<20} | {l_opt:<20.2f} | {l_nn:<20.2f}")
    print(f"{'Tiempo (s)':<20} | {t_ex:<20.4f} | {t_nn:<20.4f}")
    print("-" * 70)
    print(f"GAP DE OPTIMALIDAD: {gap:.2f}% (Cuanto más bajo, mejor)")
    print(f"DIFERENCIA DE TIEMPO: El heurístico es {speedup:.1f}x veces más rápido")
    
    # 5. Generar Entregables Automáticos
    print("\nGenerando gráficos y animaciones para el informe...")
    solver_ex.visualizar_solucion(res_ex, "comparacion_exhaustiva.png", mostrar=False)
    solver_nn.visualizar_solucion(res_nn, "comparacion_heuristica.png", mostrar=False)
    
    # Generar GIFs automáticamente
    solver_ex.animar_busqueda(res_ex, "animacion_exhaustiva.gif")
    solver_nn.animar_construccion(res_nn, "animacion_heuristica.gif")
    
    print("\n[ÉXITO] Archivos generados:")
    print("- comparacion_exhaustiva.png")
    print("- comparacion_heuristica.png")
    print("- animacion_exhaustiva.gif")
    print("- animacion_heuristica.gif")

def main():
    while True:
        op = menu_principal()
        if op == '1': ejecutar_heuristico()
        elif op == '2': ejecutar_exhaustivo()
        elif op == '3': ejecutar_comparativa()
        elif op == '4': sys.exit()
        else: print("Opción inválida")

if __name__ == "__main__":
    main()
