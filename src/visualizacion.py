"""
Funciones de visualización para el TSP
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from src.algoritmos import calcular_distancia_ruta


def visualizar_ruta(coordenadas, ruta, titulo="Ruta TSP", archivo=None):
    """
    Visualiza una ruta del TSP.
    
    Args:
        coordenadas: Lista de tuplas (x, y) con las coordenadas de cada ciudad
        ruta: Lista de índices de ciudades en orden de visita
        titulo: Título del gráfico
        archivo: Ruta para guardar la imagen (None = mostrar)
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Extraer coordenadas de la ruta
    ruta_completa = ruta + [ruta[0]]  # Volver al inicio
    x = [coordenadas[i][0] for i in ruta_completa]
    y = [coordenadas[i][1] for i in ruta_completa]
    
    # Dibujar la ruta
    ax.plot(x, y, 'b-', linewidth=2, alpha=0.7, label='Ruta')
    
    # Dibujar las ciudades
    for i, (cx, cy) in enumerate(coordenadas):
        if i == ruta[0]:
            # Ciudad inicial en verde
            ax.plot(cx, cy, 'go', markersize=12, label='Inicio', zorder=5)
        else:
            ax.plot(cx, cy, 'ro', markersize=8, zorder=5)
        ax.text(cx, cy, f'  {i}', fontsize=10, ha='left')
    
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_xlabel('Coordenada X')
    ax.set_ylabel('Coordenada Y')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_aspect('equal')
    
    plt.tight_layout()
    
    if archivo:
        plt.savefig(archivo, dpi=150, bbox_inches='tight')
        print(f"    → Imagen guardada: {archivo}")
        plt.close()
    else:
        plt.show()


def crear_animacion_busqueda(coordenadas, rutas, matriz_distancias, 
                            titulo="Búsqueda de Ruta Óptima", 
                            archivo="animacion.gif"):
    """
    Crea una animación del proceso de búsqueda.
    
    Args:
        coordenadas: Lista de tuplas (x, y) con las coordenadas de cada ciudad
        rutas: Lista de rutas a animar
        matriz_distancias: Matriz de distancias
        titulo: Título de la animación
        archivo: Archivo donde guardar la animación
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    mejor_distancia = float('inf')
    mejor_ruta_actual = None
    
    def actualizar(frame):
        nonlocal mejor_distancia, mejor_ruta_actual
        
        ax.clear()
        
        ruta_actual = rutas[frame]
        distancia_actual = calcular_distancia_ruta(ruta_actual, matriz_distancias)
        
        # Actualizar mejor ruta
        if distancia_actual < mejor_distancia:
            mejor_distancia = distancia_actual
            mejor_ruta_actual = ruta_actual
        
        # Dibujar ruta actual
        ruta_completa = ruta_actual + [ruta_actual[0]]
        x = [coordenadas[i][0] for i in ruta_completa]
        y = [coordenadas[i][1] for i in ruta_completa]
        
        ax.plot(x, y, 'b-', linewidth=2, alpha=0.5)
        
        # Dibujar ciudades
        for i, (cx, cy) in enumerate(coordenadas):
            ax.plot(cx, cy, 'ro', markersize=8, zorder=5)
            ax.text(cx, cy, f'  {i}', fontsize=10)
        
        # Información
        ax.set_title(f"{titulo}\nIteración: {frame+1}/{len(rutas)} | "
                    f"Distancia actual: {distancia_actual:.2f} | "
                    f"Mejor: {mejor_distancia:.2f}", 
                    fontsize=12)
        ax.set_xlabel('Coordenada X')
        ax.set_ylabel('Coordenada Y')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
    
    anim = FuncAnimation(fig, actualizar, frames=len(rutas), 
                        interval=200, repeat=True)
    
    if archivo:
        anim.save(archivo, writer='pillow', fps=5)
        print(f"    → Animación guardada: {archivo}")
        plt.close()
    else:
        plt.show()


def visualizar_comparacion(coordenadas, ruta1, ruta2, dist1, dist2,
                          etiqueta1="Ruta 1", etiqueta2="Ruta 2",
                          archivo=None):
    """
    Visualiza dos rutas lado a lado para comparación.
    
    Args:
        coordenadas: Lista de coordenadas de ciudades
        ruta1, ruta2: Rutas a comparar
        dist1, dist2: Distancias de cada ruta
        etiqueta1, etiqueta2: Etiquetas para cada ruta
        archivo: Archivo para guardar (None = mostrar)
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    for ax, ruta, dist, etiqueta in [(ax1, ruta1, dist1, etiqueta1),
                                      (ax2, ruta2, dist2, etiqueta2)]:
        ruta_completa = ruta + [ruta[0]]
        x = [coordenadas[i][0] for i in ruta_completa]
        y = [coordenadas[i][1] for i in ruta_completa]
        
        ax.plot(x, y, 'b-', linewidth=2, alpha=0.7)
        
        for i, (cx, cy) in enumerate(coordenadas):
            if i == ruta[0]:
                ax.plot(cx, cy, 'go', markersize=12, zorder=5)
            else:
                ax.plot(cx, cy, 'ro', markersize=8, zorder=5)
            ax.text(cx, cy, f'  {i}', fontsize=10)
        
        ax.set_title(f"{etiqueta}\nDistancia: {dist:.2f}", 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Coordenada X')
        ax.set_ylabel('Coordenada Y')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
    
    plt.tight_layout()
    
    if archivo:
        plt.savefig(archivo, dpi=150, bbox_inches='tight')
        print(f"    → Comparación guardada: {archivo}")
        plt.close()
    else:
        plt.show()
