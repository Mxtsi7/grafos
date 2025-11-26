import sys
# Importamos ambas clases de sus respectivos archivos
from algoritmo_vecino_cercano  import TSPVecinoMasCercano
from algoritmo_exhautivo import TSPExhaustivo

# Base de datos de ciudades
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
    print("\n" + "="*50)
    print("   SISTEMA EXPERTO DE RUTAS - TSP SOLVER")
    print("="*50)
    print("1. Método Heurístico (Vecino Más Cercano)")
    print("2. Método Exacto (Búsqueda Exhaustiva)")
    print("3. Ver Matriz de Distancias")
    print("4. Salir")
    return input("\nSeleccione una estrategia (1-4): ")

def ejecutar_heuristico():
    print("\n--- MODO HEURÍSTICO (Rápido, Aproximado) ---")
    solver = TSPVecinoMasCercano(CIUDADES_DATA)
    
    print("1. Ruta desde ciudad específica")
    print("2. Mejor ruta (Multi-inicio)")
    sub_op = input("Opción: ")
    
    if sub_op == '1':
        print(f"\nCiudades: {', '.join(solver.ciudades)}")
        ciudad = input("Ciudad de inicio: ").strip()
        if ciudad in solver.ciudades:
            res = solver.resolver(ciudad, verbose=True)
            if res:
                solver.visualizar_solucion(res)
    elif sub_op == '2':
        res = solver.resolver_multi_inicio()
        if res['mejor']:
            print(f"\nMejor Heurística: {res['mejor']['longitud']:.2f} km")
            solver.visualizar_solucion(res['mejor'], ruta_guardado="mejor_heuristica.png")

def ejecutar_exhaustivo():
    print("\n--- MODO EXACTO (Lento, Óptimo Global) ---")
    n_ciudades = len(CIUDADES_DATA)
    if n_ciudades > 10:
        print(f"[ADVERTENCIA] {n_ciudades} ciudades es demasiado para el método exhaustivo.")
        confirmar = input("¿Continuar de todos modos? (s/n): ")
        if confirmar.lower() != 's': return

    solver = TSPExhaustivo(CIUDADES_DATA)
    print("Calculando todas las permutaciones posibles...")
    
    res = solver.resolver(guardar_proceso=True)
    
    print("\n" + "*"*40)
    print(f"SOLUCIÓN ÓPTIMA MATEMÁTICA")
    print("*"*40)
    print(f"Ruta: {' -> '.join([solver.ciudades[i] for i in res['tour']])}")
    print(f"Distancia mínima: {res['longitud']:.2f} km")
    print(f"Iteraciones: {res['iteraciones']:,}")
    print(f"Tiempo: {res['tiempo']:.4f} s")
    
    if input("\n¿Ver gráfico de la ruta óptima? (s/n): ").lower() == 's':
        solver.visualizar_solucion(res, ruta_guardado="ruta_optima.png")
        
    if input("¿Ver gráfico de convergencia? (s/n): ").lower() == 's':
        solver.visualizar_convergencia(res)

def main():
    while True:
        opcion = menu_principal()
        
        if opcion == '1':
            ejecutar_heuristico()
        elif opcion == '2':
            ejecutar_exhaustivo()
        elif opcion == '3':
            # Usamos cualquiera de los dos solvers para mostrar la matriz
            temp_solver = TSPVecinoMasCercano(CIUDADES_DATA)
            print(temp_solver.matriz_distancias)
        elif opcion == '4':
            print("Cerrando sistema.")
            sys.exit()
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
