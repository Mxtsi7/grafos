# Problema del Viajante (TSP) - Proyecto de Teoría de Grafos

## Descripción
Implementación del Problema del Viajante (Traveling Salesman Problem) utilizando diferentes algoritmos:
- Búsqueda exhaustiva (fuerza bruta)
- Algoritmo del vecino más cercano (Nearest Neighbor)

Incluye visualizaciones animadas del proceso de búsqueda de rutas.

## Requisitos
- Python 3.8 o superior
- Librerías especificadas en `requirements.txt`

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Mxtsi7/grafos.git
cd grafos

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
# Ejecutar el programa principal
python main.py
```

## Estructura del Proyecto

```
grafos/
├── data/
│   └── ciudades_ejemplo.csv    # Coordenadas de ciudades de ejemplo
├── src/
│   ├── algoritmos.py           # Implementación de algoritmos TSP
│   ├── visualizacion.py        # Funciones de visualización y animación
│   └── utils.py                # Funciones auxiliares
├── resultados/                 # Carpeta para guardar resultados (se crea automáticamente)
├── main.py                     # Punto de entrada del programa
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
```

## Características

- ✅ Cálculo de distancias euclidianas entre ciudades
- ✅ Algoritmo de búsqueda exhaustiva
- ✅ Algoritmo del vecino más cercano
- ✅ Visualización de rutas
- ✅ Animaciones del proceso de búsqueda
- ✅ Comparación de tiempos de ejecución
- ✅ Generación de matrices de distancia

## Autores

Grupo de Teoría de Grafos

## Licencia

Proyecto académico - INFO1158
