# 🗺️ Problema del Viajante (TSP) - Proyecto de Teoría de Grafos

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Academic-green.svg)](LICENSE)

## 📋 Descripción

Implementación completa del **Problema del Viajante (Traveling Salesman Problem - TSP)** para el curso de Teoría de Grafos (INFO1158). El proyecto incluye:

- 🔍 **Búsqueda exhaustiva** (fuerza bruta) - encuentra la solución óptima
- ⚡ **Algoritmo del vecino más cercano** (heurística greedy) - solución rápida aproximada
- 📊 **Visualizaciones interactivas** - gráficos de rutas y comparaciones
- 🎬 **Animaciones** - visualización del proceso de búsqueda
- ⏱️ **Análisis de rendimiento** - comparación de tiempos de ejecución

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Mxtsi7/grafos.git
cd grafos

# 2. (Opcional) Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual:
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Ejecución Básica

```bash
# Ejecutar el programa con las ciudades de ejemplo
python main.py
```

**Salida esperada:**
```
============================================================
  PROBLEMA DEL VIAJANTE (TSP)
  Teoría de Grafos - INFO1158
============================================================

[1] Cargando coordenadas de ciudades...
    ✓ 6 ciudades cargadas

[2] Calculando matriz de distancias...
    ✓ Matriz 6x6 calculada

[3] Ejecutando búsqueda exhaustiva...
    ✓ Mejor ruta: [0, 2, 5, 3, 1, 4]
    ✓ Distancia total: 187.35
    ✓ Tiempo de ejecución: 0.0023 segundos

[4] Ejecutando algoritmo del vecino más cercano...
    ✓ Ruta encontrada: [0, 1, 3, 5, 2, 4]
    ✓ Distancia total: 195.42
    ✓ Tiempo de ejecución: 0.0001 segundos

[5] Comparación de algoritmos:
    Diferencia de distancia: 8.07
    Factor de velocidad: 23.00x más rápido (NN)

[6] Generando visualizaciones...
    → Imagen guardada: resultados/ruta_exhaustiva.png
    → Imagen guardada: resultados/ruta_vecino_cercano.png
    ✓ Visualizaciones guardadas en /resultados

[7] Guardando resultados...
    ✓ Resultados guardados en resultados.json

============================================================
  ✓ Proceso completado exitosamente
============================================================
```

---

## 📂 Estructura del Proyecto

```
grafos/
├── 📁 data/
│   └── ciudades_ejemplo.csv          # 6 ciudades de prueba (x, y)
│
├── 📁 src/
│   ├── algoritmos.py                 # Implementación de algoritmos TSP
│   ├── visualizacion.py              # Funciones de gráficos y animaciones
│   └── utils.py                      # Utilidades (distancias, E/S)
│
├── 📁 resultados/                    # Resultados generados (creado automáticamente)
│   ├── ruta_exhaustiva.png           # Visualización de mejor ruta
│   ├── ruta_vecino_cercano.png       # Visualización de ruta greedy
│   └── resultados.json               # Datos de ejecución
│
├── 📄 main.py                        # Programa principal
├── 📄 requirements.txt               # Dependencias del proyecto
└── 📄 README.md                      # Este archivo
```

---

## 📚 Cómo Funciona el Código

### 1️⃣ Flujo Principal (`main.py`)

El programa sigue este flujo:

```python
# Paso 1: Cargar datos de ciudades desde CSV
coordenadas = cargar_ciudades('data/ciudades_ejemplo.csv')
# Resultado: [(10, 20), (30, 40), (50, 10), ...]

# Paso 2: Calcular matriz de distancias euclidianas
matriz_distancias = calcular_matriz_distancias(coordenadas)
# Resultado: Matriz NxN donde matriz[i][j] = distancia entre ciudad i y j

# Paso 3: Ejecutar búsqueda exhaustiva
mejor_ruta, distancia = busqueda_exhaustiva(matriz_distancias)
# Prueba TODAS las permutaciones posibles y encuentra la óptima

# Paso 4: Ejecutar vecino más cercano (greedy)
ruta_nn, distancia_nn = vecino_mas_cercano(matriz_distancias)
# En cada paso, va a la ciudad más cercana no visitada

# Paso 5: Generar visualizaciones
visualizar_ruta(coordenadas, mejor_ruta, archivo="resultados/ruta.png")

# Paso 6: Guardar resultados en JSON
guardar_resultados(resultados, 'resultados/resultados.json')
```

### 2️⃣ Algoritmos (`src/algoritmos.py`)

#### 🔍 Búsqueda Exhaustiva (Fuerza Bruta)

```python
def busqueda_exhaustiva(matriz_distancias):
    """
    Cómo funciona:
    1. Fija la primera ciudad (por simetría del problema)
    2. Genera TODAS las permutaciones de las ciudades restantes
    3. Para cada permutación:
       - Calcula la distancia total del recorrido
       - Si es menor que la mejor actual, la guarda
    4. Retorna la mejor ruta encontrada
    
    Complejidad: O(n!) - muy lento para n > 10
    Garantía: Encuentra la solución ÓPTIMA
    """
```

**Ejemplo con 4 ciudades:**
```
Ciudad 0 fija, permutaciones de [1,2,3]:
  [0,1,2,3] → distancia = 95
  [0,1,3,2] → distancia = 102
  [0,2,1,3] → distancia = 88  ← MEJOR
  [0,2,3,1] → distancia = 97
  [0,3,1,2] → distancia = 105
  [0,3,2,1] → distancia = 91
```

#### ⚡ Vecino Más Cercano (Greedy)

```python
def vecino_mas_cercano(matriz_distancias, ciudad_inicial=0):
    """
    Cómo funciona:
    1. Empieza en ciudad_inicial
    2. Repite hasta visitar todas:
       - Busca la ciudad más cercana NO visitada
       - Muévete a esa ciudad
       - Márcala como visitada
    3. Vuelve a la ciudad inicial
    
    Complejidad: O(n²) - rápido incluso para n grande
    Garantía: Solución aproximada (puede no ser óptima)
    """
```

**Ejemplo paso a paso:**
```
Inicio: Ciudad 0, No visitadas: {1,2,3}
  Distancias desde 0: 1→10, 2→15, 3→20
  → Más cercana: 1 (distancia 10)

Actual: Ciudad 1, No visitadas: {2,3}
  Distancias desde 1: 2→35, 3→25
  → Más cercana: 3 (distancia 25)

Actual: Ciudad 3, No visitadas: {2}
  Distancias desde 3: 2→30
  → Única opción: 2 (distancia 30)

Ruta final: [0,1,3,2] → distancia total = 10+25+30+15 = 80
```

### 3️⃣ Utilidades (`src/utils.py`)

#### Cálculo de Distancias

```python
def calcular_distancia_euclidiana(punto1, punto2):
    """
    Fórmula: d = √[(x₂-x₁)² + (y₂-y₁)²]
    
    Ejemplo:
    punto1 = (0, 0)
    punto2 = (3, 4)
    distancia = √[(3-0)² + (4-0)²] = √[9 + 16] = √25 = 5
    """
    return np.sqrt((punto1[0] - punto2[0])**2 + 
                   (punto1[1] - punto2[1])**2)
```

#### Matriz de Distancias

```python
def calcular_matriz_distancias(coordenadas):
    """
    Crea una matriz NxN donde:
    - matriz[i][j] = distancia entre ciudad i y ciudad j
    - matriz[i][i] = 0 (distancia de una ciudad a sí misma)
    - matriz[i][j] = matriz[j][i] (simétrica)
    
    Ejemplo con 3 ciudades:
    coordenadas = [(0,0), (3,0), (3,4)]
    
    matriz = [[0.0, 3.0, 5.0],   # Desde ciudad 0
              [3.0, 0.0, 4.0],   # Desde ciudad 1
              [5.0, 4.0, 0.0]]   # Desde ciudad 2
    """
```

### 4️⃣ Visualizaciones (`src/visualizacion.py`)

```python
def visualizar_ruta(coordenadas, ruta, titulo, archivo):
    """
    Crea un gráfico mostrando:
    - Círculos para cada ciudad
    - Líneas conectando las ciudades en el orden de la ruta
    - Números identificando cada ciudad
    - Ciudad inicial en color diferente (verde)
    - Grid para referencia
    
    El gráfico se guarda como imagen PNG
    """
```

---

## 🛠️ Uso Avanzado

### Usar tus propias ciudades

1. Crea un archivo CSV en `data/` con este formato:
```csv
x,y
10,20
30,40
50,10
70,60
```

2. Modifica `main.py` (línea ~21):
```python
coordenadas = cargar_ciudades('data/mis_ciudades.csv')
```

### Generar ciudades aleatorias

```python
from src.utils import generar_ciudades_aleatorias, guardar_ciudades_csv

# Generar 10 ciudades aleatorias
coords = generar_ciudades_aleatorias(n=10, semilla=42)
guardar_ciudades_csv(coords, 'data/ciudades_aleatorias.csv')
```

### Crear animaciones

```python
from src.algoritmos import obtener_todas_rutas
from src.visualizacion import crear_animacion_busqueda

# Generar rutas (cuidado con n > 8)
rutas = obtener_todas_rutas(n_ciudades=6, max_rutas=100)

crear_animacion_busqueda(
    coordenadas, 
    rutas, 
    matriz_distancias,
    archivo='resultados/animacion.gif'
)
```

---

## 📊 Algoritmos: Complejidad y Rendimiento

### Comparación

| Ciudades | Exhaustiva (s) | Vecino Cercano (s) | Factor |
|----------|----------------|---------------------|--------|
| 5        | 0.001         | 0.0001              | 10x    |
| 6        | 0.002         | 0.0001              | 20x    |
| 7        | 0.015         | 0.0001              | 150x   |
| 8        | 0.120         | 0.0002              | 600x   |
| 9        | 1.080         | 0.0002              | 5400x  |
| 10       | ~11.0         | 0.0003              | ~37000x|
| 15       | ~varios días | 0.0005              | - |

**Recomendación:**
- ≤ 10 ciudades: Usa búsqueda exhaustiva
- \> 10 ciudades: Usa solo vecino más cercano

### Número de Permutaciones

```
n=5:   4! = 24 rutas
n=10:  9! = 362,880 rutas
n=15:  14! = 87,178,291,200 rutas (!)
```

---

## 🧪 Testing y Verificación

### Verificar instalación

```bash
python -c "import numpy, matplotlib, pandas; print('✓ Librerías OK')"
```

### Probar con ejemplo mínimo

```python
from src.utils import calcular_matriz_distancias
from src.algoritmos import busqueda_exhaustiva, vecino_mas_cercano

# Cuadrado de 4 ciudades
coords = [(0,0), (1,0), (1,1), (0,1)]
matriz = calcular_matriz_distancias(coords)

ruta_opt, dist_opt = busqueda_exhaustiva(matriz)
ruta_nn, dist_nn = vecino_mas_cercano(matriz)

print(f"Óptima: {ruta_opt} -> {dist_opt:.2f}")  # Debería ser 4.0
print(f"Greedy: {ruta_nn} -> {dist_nn:.2f}")
```

---

## 🐛 Solución de Problemas

### Error: `ModuleNotFoundError`
```bash
pip install -r requirements.txt
```

### Error: `FileNotFoundError`
Asegúrate de estar en la carpeta correcta:
```bash
cd grafos/
python main.py
```

### Programa muy lento
Demasiadas ciudades. Comenta la búsqueda exhaustiva:
```python
# mejor_ruta, dist = busqueda_exhaustiva(matriz)  # Comentar esta línea
```

---

## 🎓 Conceptos Teóricos

### ¿Qué es el TSP?

El Problema del Viajante busca la ruta más corta que:
1. Visita cada ciudad exactamente una vez
2. Regresa a la ciudad de origen
3. Minimiza la distancia total recorrida

### Complejidad Computacional

- **Clase:** NP-difícil
- **Rutas posibles:** (n-1)!/2
- **Ejemplo:** 10 ciudades = 181,440 rutas

### Aplicaciones Prácticas

- 🚚 Optimización de rutas de entrega
- 🏭 Planificación de producción
- 🔬 Secuenciación de ADN
- 📡 Diseño de circuitos

---

## 👥 Autores

Grupo de Teoría de Grafos - INFO1158

## 📄 Licencia

Proyecto académico

---

**⭐ Si este proyecto te fue útil, dale una estrella en GitHub!**
