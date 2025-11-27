import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
import pydeck as pdk  
from algoritmo_vecino_cercano import TSPVecinoMasCercano
from algoritmo_exhautivo import TSPExhaustivo

st.set_page_config(page_title="TSP Lab", layout="wide", page_icon="🚛")

CIUDADES_BASE = {
    'Nairobi': (-1.28333, 36.81667),   
    'Osorno': (-40.57395, -73.13348),  
    'Rancagua': (-34.17083, -70.74444),
    'Pamplona': (42.81687, -1.64323),  
    'Moscu': (55.75222, 37.61556),    
    'Orlando': (28.53834, -81.37924),  
    'San Jose': (37.33939, -121.89496) 
}


def animar_recorrido(placeholder, solver, pasos, titulo_base, velocidad=0.1, es_exhaustivo=False):
    fig, ax = plt.subplots(figsize=(5, 4))
    pad = 1.0
    try:
        ax.set_xlim(solver.coordenadas[:, 1].min()-pad, solver.coordenadas[:, 1].max()+pad)
        ax.set_ylim(solver.coordenadas[:, 0].min()-pad, solver.coordenadas[:, 0].max()+pad)
    except ValueError:
        pass 

    if len(pasos) > 50:
        indices = np.linspace(0, len(pasos)-1, 50, dtype=int)
        pasos_filtrados = [pasos[i] for i in indices]
        if pasos[-1] != pasos_filtrados[-1]:
            pasos_filtrados.append(pasos[-1])
        pasos = pasos_filtrados

    for i, paso_data in enumerate(pasos):
        ax.clear()
        
        if es_exhaustivo:
            tour_actual, longitud, es_mejor = paso_data
            titulo = f"{titulo_base}\nEval: {longitud:.1f} km"
            color_linea = 'green' if es_mejor else 'gray'
            grosor = 2 if es_mejor else 1
        else:
            tour_actual = paso_data
            longitud = solver._calcular_longitud_tour(tour_actual)
            titulo = f"{titulo_base}\nPaso {i+1}"
            color_linea = 'blue'
            grosor = 2

        ax.scatter(solver.coordenadas[:, 1], solver.coordenadas[:, 0], c='lightgray', s=50)
        
        if len(tour_actual) > 0:
            coords_tour = solver.coordenadas[tour_actual]
            ax.scatter(coords_tour[:, 1], coords_tour[:, 0], c=color_linea, s=80)
            
            if len(tour_actual) > 1:
                ax.plot(coords_tour[:, 1], coords_tour[:, 0], color=color_linea, linewidth=grosor)
                
                if es_exhaustivo or (not es_exhaustivo and i == len(pasos)-1):
                    coords_cierre = solver.coordenadas[[tour_actual[-1], tour_actual[0]]]
                    ax.plot(coords_cierre[:, 1], coords_cierre[:, 0], color=color_linea, linestyle='--', linewidth=grosor)

        for idx, txt in enumerate(solver.ciudades):
            ax.annotate(txt, (solver.coordenadas[idx, 1], solver.coordenadas[idx, 0]), fontsize=8)

        ax.set_title(titulo, fontsize=10)
        ax.axis('off')
        
        placeholder.pyplot(fig)
        time.sleep(velocidad)
    
    plt.close(fig)

with st.sidebar:
    st.markdown("#### ⚙️ Configuración")
    seleccion = []
    col_sel = st.columns(2)
    for i, ciudad in enumerate(CIUDADES_BASE.keys()):
        with col_sel[i % 2]:
            if st.checkbox(ciudad, value=True, key=f"chk_{ciudad}"):
                seleccion.append(ciudad)
    
    datos_activos = {k: CIUDADES_BASE[k] for k in seleccion}
    if len(datos_activos) < 3: st.stop()

    st.divider()
    ciudad_inicio = st.selectbox("Inicio Heurística:", list(datos_activos.keys()))
    st.divider()
    animar = st.checkbox("Animar proceso", value=True)
    velocidad = st.slider("Velocidad animación", 0.01, 0.5, 0.1)

st.title("🚛 TSP Visualizer (Live)")

df_pdk = pd.DataFrame([
    {'lat': v[0], 'lon': v[1], 'name': k} 
    for k, v in datos_activos.items()
])

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=20,
        longitude=0,
        zoom=1,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df_pdk,
            get_position='[lon, lat]',
            get_color='[255, 75, 75, 200]', 
            get_radius=500000, 
            pickable=True,
        ),
        pdk.Layer(
            "TextLayer",
            data=df_pdk,
            get_position='[lon, lat]',
            get_text="name",
            get_color=[0, 0, 0, 255],
            get_size=20,
            get_alignment_baseline="'bottom'",
        ),
    ],
))

with st.expander("📏 Ver Matriz de Distancias", expanded=False):
    solver_temp = TSPVecinoMasCercano(datos_activos)
    nombres_ciudades = list(datos_activos.keys())
    df_matriz = pd.DataFrame(
        solver_temp.matriz_distancias, 
        index=nombres_ciudades, 
        columns=nombres_ciudades
    )
    st.dataframe(df_matriz, use_container_width=True)

if 'res_nn' not in st.session_state:
    st.session_state.res_nn = None
    st.session_state.res_ex = None
    st.session_state.needs_animation = False

if st.button("🚀 EJECUTAR", type="primary", use_container_width=True):
    with st.spinner("Calculando..."):
        solver_nn = TSPVecinoMasCercano(datos_activos)
        st.session_state.res_nn = solver_nn.resolver(ciudad_inicio=ciudad_inicio)
        st.session_state.solver_nn_obj = solver_nn

        solver_ex = TSPExhaustivo(datos_activos)
        st.session_state.res_ex = solver_ex.resolver(guardar_proceso=True)
        st.session_state.solver_ex_obj = solver_ex
        
        st.session_state.needs_animation = True
        st.rerun()

if st.session_state.res_nn:
    res_nn = st.session_state.res_nn
    res_ex = st.session_state.res_ex
    
    col_h, col_e = st.columns(2)
    
    with col_h:
        st.markdown("#### 🔹 Heurística")
        c1, c2 = st.columns(2)
        c1.metric("Distancia", f"{res_nn['longitud']:.2f}")
        c2.metric("Tiempo", f"{res_nn['tiempo']:.4f}s")
        
        plot_h = st.empty()
        if not st.session_state.needs_animation or not animar:
             animar_recorrido(plot_h, st.session_state.solver_nn_obj, [res_nn['tour']], "Final", 0, False)

    with col_e:
        st.markdown("#### 🔸 Exhaustiva")
        c1, c2 = st.columns(2)
        c1.metric("Distancia", f"{res_ex['longitud']:.2f}")
        c2.metric("Tiempo", f"{res_ex['tiempo']:.4f}s")
        
        plot_e = st.empty()
        if not st.session_state.needs_animation or not animar:
             animar_recorrido(plot_e, st.session_state.solver_ex_obj, [(res_ex['tour'], res_ex['longitud'], True)], "Final", 0, True)

    if st.session_state.needs_animation and animar:
        with col_h:
            animar_recorrido(plot_h, st.session_state.solver_nn_obj, res_nn['pasos'], "Construyendo...", velocidad, False)
        
        with col_e:
            animar_recorrido(plot_e, st.session_state.solver_ex_obj, res_ex['tours_animacion'], "Buscando...", velocidad, True)
        
        st.session_state.needs_animation = False
        st.rerun()

    st.divider()
    gap = ((res_nn['longitud'] - res_ex['longitud']) / res_ex['longitud']) * 100
    st.info(f"**GAP:** {gap:.2f}% | **Speedup:** {res_ex['tiempo']/res_nn['tiempo']:.1f}x")
    
    if st.button("🔄 Repetir Animación"):
        st.session_state.needs_animation = True
        st.rerun()
