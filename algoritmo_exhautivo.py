import numpy as np
import time
import math
from itertools import permutations
from math import radians, sin, cos, sqrt, atan2

class TSPExhaustivo:
    def __init__(self, datos_ciudades):
        self.ciudades = list(datos_ciudades.keys())
        self.coordenadas = np.array(list(datos_ciudades.values()))
        self.n = len(self.ciudades)
        self.matriz_distancias = self._calcular_matriz_distancias()

    def _distancia_haversine(self, coord1, coord2):
        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])
        a = sin((lat2-lat1)/2)**2 + cos(lat1) * cos(lat2) * sin((lon2-lon1)/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return 6371.0 * c

    def _calcular_matriz_distancias(self):
        D = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    D[i][j] = self._distancia_haversine(self.coordenadas[i], self.coordenadas[j])
        return D

    def _calcular_longitud_tour(self, tour):
        return sum(self.matriz_distancias[tour[i]][tour[(i+1) % len(tour)]] for i in range(len(tour)))

    def resolver(self, guardar_proceso=True):
        t_start = time.time()
        ciudades_restantes = list(range(1, self.n))
        
        mejor_tour, mejor_len = None, float('inf')
        tours_animacion = []
        iteraciones = 0
        frecuencia = max(1, int(math.factorial(self.n-1)/50))

        for perm in permutations(ciudades_restantes):
            tour = [0] + list(perm)
            longitud = self._calcular_longitud_tour(tour)
            iteraciones += 1
            
            if longitud < mejor_len:
                mejor_len = longitud
                mejor_tour = tour.copy()
                if guardar_proceso:
                    tours_animacion.append((tour.copy(), longitud, True))
            elif guardar_proceso and iteraciones % frecuencia == 0:
                tours_animacion.append((tour.copy(), longitud, False))

        return {
            'tour': mejor_tour,
            'longitud': mejor_len,
            'tiempo': time.time() - t_start,
            'tours_animacion': tours_animacion
        }
