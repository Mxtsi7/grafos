# Información de las Ciudades

Coordenadas geográficas reales (latitud, longitud) en formato decimal.

| Ciudad | Latitud | Longitud | País |
|--------|---------|----------|------|
| Nairobi | -1.28333 | 36.81667 | Kenia |
| Osorno | -40.57395 | -73.13348 | Chile |
| Rancagua | -34.17083 | -70.74444 | Chile |
| Pamplona | 42.81687 | -1.64323 | España |
| Moscú | 55.75222 | 37.61556 | Rusia |
| Orlando | 28.53834 | -81.37924 | Estados Unidos |
| San José | 9.92807 | -84.09072 | Costa Rica |

## Notas

- Las coordenadas están en formato decimal (WGS84)
- Latitud: valores negativos = Sur, positivos = Norte
- Longitud: valores negativos = Oeste, positivos = Este
- El archivo `ciudades_ejemplo.csv` contiene estas coordenadas en el orden listado arriba

## Distancias Aproximadas

Estas ciudades están distribuidas globalmente:
- **Hemisferio Sur**: Nairobi, Osorno, Rancagua
- **Hemisferio Norte**: Pamplona, Moscú, Orlando, San José
- **América**: Osorno, Rancagua, Orlando, San José
- **Europa**: Pamplona, Moscú
- **África**: Nairobi

## Uso en el Proyecto

El programa calculará las distancias euclidianas entre estas coordenadas para resolver el TSP.
Debido a que son coordenadas geográficas reales en un plano esférico, las distancias calculadas
serán aproximaciones. Para mayor precisión con coordenadas geográficas, se podría usar la
fórmula de Haversine (ver documentación en README.md).
