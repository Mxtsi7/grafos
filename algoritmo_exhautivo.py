import numpy as np
import time
import math
from itertools import permutations
from math import radians, sin, cos, sqrt, atan2

class TSPExhaustivo:
    def __init__(self, datos_ciudades):
        # Asigna la lista de nombres de las ciudades
        self.ciudades = list(datos_ciudades.keys())
        # Asigna las coordenadas de las ciudades como un array de numpy
        self.coordenadas = np.array(list(datos_ciudades.values()))
        # Asigna el número de ciudades
        self.n = len(self.ciudades)
        # Calcula y asigna la matriz de distancias entre ciudades
        self.matriz_distancias = self._calcular_matriz_distancias()

    # Define el método para calcular la distancia haversine entre dos coordenadas
    def _distancia_haversine(self, coord1, coord2):
        # Convierte las coordenadas de grados a radianes
        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        # Convierte las coordenadas de grados a radianes
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])
        # Aplica la fórmula de haversine
        a = sin((lat2-lat1)/2)**2 + cos(lat1) * cos(lat2) * sin((lon2-lon1)/2)**2
        # Calcula la distancia angular
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        # Retorna la distancia en kilómetros
        return 6371.0 * c

    def _calcular_matriz_distancias(self):
        # Inicializa una matriz de ceros de tamaño n x n
        D = np.zeros((self.n, self.n))
        # Itera sobre todas las ciudades
        for i in range(self.n):
            # Itera sobre todas las ciudades
            for j in range(self.n):
                # Si no es la misma ciudad
                if i != j:
                    # Calcula la distancia haversine y la asigna a la matriz
                    D[i][j] = self._distancia_haversine(self.coordenadas[i], self.coordenadas[j])

        return D

    def _calcular_longitud_tour(self, tour):
        # Retorna la suma de las distancias entre ciudades consecutivas en el tour
        return sum(self.matriz_distancias[tour[i]][tour[(i+1) % len(tour)]] for i in range(len(tour)))

    # Define el método principal para resolver el TSP
    def resolver(self, guardar_proceso=True):
        # Guarda el tiempo de inicio
        t_start = time.time()
        # Crea una lista de las ciudades restantes a visitar
        ciudades_restantes = list(range(1, self.n))
        # Inicializa el mejor tour y la mejor longitud
        mejor_tour, mejor_len = None, float('inf')
        # Inicializa la lista para guardar los tours de la animación
        tours_animacion = []
        # Inicializa el contador de iteraciones
        iteraciones = 0
        # Calcula la frecuencia con la que se guardarán los tours para la animación
        frecuencia = max(1, int(math.factorial(self.n-1)/50))

        # Itera sobre todas las permutaciones de las ciudades restantes
        for perm in permutations(ciudades_restantes):
            # Crea el tour completo comenzando desde la ciudad 0
            tour = [0] + list(perm)
            # Calcula la longitud del tour actual
            longitud = self._calcular_longitud_tour(tour)
            # Incrementa el contador de iteraciones
            iteraciones += 1
            # Si la longitud actual es menor que la mejor longitud encontrada hasta ahora
            if longitud < mejor_len:
                # Actualiza la mejor longitud
                mejor_len = longitud
                # Actualiza el mejor tour
                mejor_tour = tour.copy()

            # Si se debe guardar el proceso
            if guardar_proceso:
                # Agrega el tour actual a la lista de animación, marcándolo como una mejora
                tours_animacion.append((tour.copy(), longitud, True))

            # Si se debe guardar el proceso y se ha alcanzado la frecuencia
            elif guardar_proceso and iteraciones % frecuencia == 0:
                # Agrega el tour actual a la lista de animación
                tours_animacion.append((tour.copy(), longitud, False))

        return {
            'tour': mejor_tour,
            'longitud': mejor_len,
            # El tiempo total de ejecución
            'tiempo': time.time() - t_start,
            'tours_animacion': tours_animacion
        }
