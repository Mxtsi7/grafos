import numpy as np
import time
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

    def resolver(self, ciudad_inicio=0):
        if isinstance(ciudad_inicio, str):
            try: ciudad_inicio = self.ciudades.index(ciudad_inicio)
            except ValueError: return None

        t_start = time.time()
        tour = [ciudad_inicio]
        no_visitadas = set(range(self.n)) - {ciudad_inicio}
        pasos = [tour.copy()]
        
        actual = ciudad_inicio
        while no_visitadas:
            siguiente = min(no_visitadas, key=lambda c: self.matriz_distancias[actual][c])
            tour.append(siguiente)
            no_visitadas.remove(siguiente)
            actual = siguiente
            pasos.append(tour.copy())

        return {
            'tour': tour,
            'longitud': self._calcular_longitud_tour(tour),
            'tiempo': time.time() - t_start,
            'pasos': pasos,
            'ciudad_inicio': ciudad_inicio
        }
