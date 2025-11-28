import numpy as np
import time
from math import radians, sin, cos, sqrt, atan2

class TSPVecinoMasCercano:
    def __init__(self, datos_ciudades):
        # Asigna la lista de nombres de las ciudades
        self.ciudades = list(datos_ciudades.keys())
        # Asigna las coordenadas de las ciudades como un array de numpy
        self.coordenadas = np.array(list(datos_ciudades.values()))
        # Asigna el número de ciudades
        self.n = len(self.ciudades)
        # Calcula y asigna la matriz de distancias entre ciudades
        self.matriz_distancias = self._calcular_matriz_distancias()

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
    def resolver(self, ciudad_inicio=0):
        # Si la ciudad de inicio es un string
        if isinstance(ciudad_inicio, str):
            # Intenta obtener el índice de la ciudad
            try: ciudad_inicio = self.ciudades.index(ciudad_inicio)
            # Si la ciudad no existe, retorna None
            except ValueError: return None

        # Guarda el tiempo de inicio
        t_start = time.time()
        # Inicializa el tour con la ciudad de inicio
        tour = [ciudad_inicio]
        # Crea un conjunto de ciudades no visitadas
        no_visitadas = set(range(self.n)) - {ciudad_inicio}
        # Inicializa la lista de pasos para la animación
        pasos = [tour.copy()]
        # Establece la ciudad actual como la ciudad de inicio
        actual = ciudad_inicio
        # Mientras haya ciudades no visitadas
        while no_visitadas:
            # Encuentra la ciudad no visitada más cercana a la actual
            siguiente = min(no_visitadas, key=lambda c: self.matriz_distancias[actual][c])
            # Agrega la siguiente ciudad al tour
            tour.append(siguiente)
            # Elimina la siguiente ciudad de las no visitadas
            no_visitadas.remove(siguiente)
            # Actualiza la ciudad actual
            actual = siguiente
            # Agrega el estado actual del tour a los pasos de la animación
            pasos.append(tour.copy())

        # Retorna un diccionario con los resultados
        return {
            'tour': tour,
            'longitud': self._calcular_longitud_tour(tour),
            # El tiempo total de ejecución
            'tiempo': time.time() - t_start,
            # Los pasos de la animación
            'pasos': pasos,
            # La ciudad de inicio utilizada
            'ciudad_inicio': ciudad_inicio
        }
