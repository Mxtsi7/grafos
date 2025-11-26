from algoritmo_vecino_cercano import TSPVecinoMasCercano
import sys

# Definición de datos (se puede mover a un JSON o base de datos luego)
CIUDADES_DATA = {
    'Nairobi': (-1.2833, 36.8167),
    'Osorno': (-40.5739, -73.1360),
    'Rancagua': (-34.1667, -70.7333),
    'Pamplona': (42.8167, -1.6500),
    'Moscu': (55.7517, 37.6178),
    'Orlando': (28.5383, -81.3792),
    'San Jose': (37.3361, -121.8906)
}

def menu():
    print("\n" + "="*40)
    print("   TSP SOLVER - INTERFAZ DE CONTROL")
    print("="*40)
    print("1. Resolver desde una ciudad específica")
    print("2. Encontrar la mejor ruta (Multi-inicio)")
    print("3. Ver matriz de distancias")
    print("4. Salir")
    return input("\nSeleccione una opción (1-4): ")

def main():
    # Inicializamos el motor del algoritmo
    solver = TSPVecinoMasCercano(CIUDADES_DATA)
    
    while True:
        opcion = menu()
        
        if opcion == '1':
            print("\nCiudades disponibles:")
            for c in solver.ciudades: print(f" - {c}")
            
            ciudad = input("\nIngrese el nombre de la ciudad de inicio: ").strip()
            if ciudad not in solver.ciudades:
                print("¡Error! Ciudad no válida.")
                continue
                
            print(f"\nCalculando ruta desde {ciudad}...")
            resultado = solver.resolver(ciudad_inicio=ciudad, verbose=True)
            
            if resultado:
                print(f"\n>>> Ruta calculada: {resultado['longitud']:.2f} km")
                guardar = input("¿Desea ver/guardar el gráfico? (s/n): ").lower()
                if guardar == 's':
                    solver.visualizar_solucion(resultado)

        elif opcion == '2':
            print("\nEjecutando estrategia Multi-inicio...")
            res_multi = solver.resolver_multi_inicio(verbose=False)
            mejor = res_multi['mejor']
            
            print("\n" + "*"*40)
            print(f"MEJOR SOLUCIÓN ENCONTRADA")
            print("*"*40)
            print(f"Inicio óptimo: {solver.ciudades[mejor['ciudad_inicio']]}")
            print(f"Distancia total: {mejor['longitud']:.2f} km")
            
            guardar = input("\n¿Desea ver/guardar el gráfico de la mejor ruta? (s/n): ").lower()
            if guardar == 's':
                solver.visualizar_solucion(mejor, ruta_guardado="mejor_solucion.png")

        elif opcion == '3':
            # Podemos llamar métodos internos si es necesario, o crear un getter
            print(solver.matriz_distancias) # O implementar un método 'print_matrix' en la clase

        elif opcion == '4':
            print("Saliendo...")
            sys.exit()
            
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
