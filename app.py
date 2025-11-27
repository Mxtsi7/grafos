import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from algoritmo_vecino_cercano import TSPVecinoMasCercano
from algoritmo_exhautivo import TSPExhaustivo

st.set_page_config(page_title="TSP Visualizer", layout="wide")

CIUDADES_BASE = {
    'Nairobi': (-1.2833, 36.8167), 'Osorno': (-40.5739, -73.1360),
    'Rancagua': (-34.1667, -70.7333), 'Pamplona': (42.8167, -1.6500),
    'Moscu': (55.7517, 37.6178), 'Orlando': (28.5383, -81.3792),
    'San Jose': (37.3361, -121.8906)
}

with st.sidebar:
    st.header("📍 Configuración")
    
    st.subheader("Selección de Ciudades")
    seleccion = []
    for ciudad in CIUDADES_BASE.keys():
        if st.checkbox(ciudad, value=True):
            seleccion.append(ciudad)
    
    datos_activos = {k: CIUDADES_BASE[k] for k in seleccion}
    
    if len(datos_activos) < 3:
        st.error("Mínimo 3 ciudades.")
        st.stop()
        
    generar_gif = st.checkbox("Generar Animaciones (GIF)", value=True)
    ver_matriz = st.checkbox("Mostrar Matriz de Distancias", value=False)

st.title("🚛 Visualización TSP: Heurística vs Exhaustiva")

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    df_map = pd.DataFrame([{'lat': v[0], 'lon': v[1]} for v in datos_activos.values()])
    st.map(df_map, height=250, zoom=1)
    st.caption(f"Mapa de {len(datos_activos)} ciudades seleccionadas.")

if ver_matriz:
    solver_temp = TSPVecinoMasCercano(datos_activos)
    df_dist = pd.DataFrame(solver_temp.matriz_distancias, 
                           index=seleccion, columns=seleccion)
    
    st.subheader("📏 Matriz de Distancias")
    tipo_vista = st.radio("Formato:", ["Tabla de Calor", "Heatmap Gráfico"], horizontal=True)
    
    if tipo_vista == "Tabla de Calor":
        st.dataframe(df_dist.style.background_gradient(cmap="Reds", axis=None).format("{:.0f}"))
    else:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(df_dist, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax)
        st.pyplot(fig)

if st.button("🚀 EJECUTAR COMPARATIVA", type="primary"):
    
    if len(datos_activos) > 9:
        st.warning("⚠️ Muchas ciudades para el método exhaustivo. Podría tardar.")

    col_heur, col_ex = st.columns(2)
    
    with col_heur:
        st.markdown("### 🔹 Heurística (Vecino Cercano)")
        solver_nn = TSPVecinoMasCercano(datos_activos)
        res_nn = solver_nn.resolver_multi_inicio()['mejor']
        
        st.success(f"Distancia: **{res_nn['longitud']:.2f} km**")
        st.info(f"Tiempo: {res_nn['tiempo']:.5f} s")
        
        if generar_gif:
            with st.spinner("Generando GIF Heurístico..."):
                solver_nn.animar_construccion(res_nn, "anim_nn.gif")
                st.image("anim_nn.gif", caption="Construcción Greedy (Paso a paso)")
        else:
            solver_nn.visualizar_solucion(res_nn, "plot_nn.png", mostrar=False)
            st.image("plot_nn.png")

    with col_ex:
        st.markdown("### 🔸 Exhaustiva (Óptimo Global)")
        with st.spinner("Calculando todas las permutaciones..."):
            solver_ex = TSPExhaustivo(datos_activos)
            res_ex = solver_ex.resolver(guardar_proceso=generar_gif)
        
        st.success(f"Distancia: **{res_ex['longitud']:.2f} km**")
        st.warning(f"Tiempo: {res_ex['tiempo']:.5f} s")
        
        # GIF o Imagen
        if generar_gif:
            with st.spinner("Generando GIF Exhaustivo..."):
                solver_ex.animar_busqueda(res_ex, "anim_ex.gif")
                st.image("anim_ex.gif", caption="Exploración de ciclos (Búsqueda)")
        else:
            solver_ex.visualizar_solucion(res_ex, "plot_ex.png", mostrar=False)
            st.image("plot_ex.png")

    st.divider()
    gap = ((res_nn['longitud'] - res_ex['longitud']) / res_ex['longitud']) * 100
    st.metric("GAP de Optimalidad (Error de la Heurística)", f"{gap:.2f}%", 
              delta_color="inverse" if gap > 0 else "normal")
