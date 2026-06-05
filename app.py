import pandas as pd
import streamlit as st
from pathlib import Path
from Calculos import resumen_calculo

st.set_page_config(page_title="Elevador de Cangilones", layout="wide")

URL_STREAMLIT = "https://elevadordecangilonesparagranos.streamlit.app"
BASE_DIR = Path(__file__).resolve().parent
LOGO_UNICA = BASE_DIR / "logo_unica.png"
IMAGEN_ELEVADOR = BASE_DIR / "elevador_cangilones.png"

if "historial" not in st.session_state:
    st.session_state.historial = []

if "ingresado" not in st.session_state:
    st.session_state.ingresado = False

def pantalla_inicio():
    st.markdown("""
        <style>
        .stApp { background-color: #202c39; }
        .titulo { text-align: center; color: #f4b41a; font-family: 'Segoe UI', sans-serif; font-size: 3em; font-weight: bold; margin-bottom: 0px;}
        .subtitulo { text-align: center; color: #a0aab5; font-size: 1.2em; margin-top: 10px; margin-bottom: 20px;}
        .footer { text-align: center; color: #4a5568; font-size: 0.9em; margin-top: 80px;}
        hr { border-top: 2px solid #f4b41a; margin-top: 2em; margin-bottom: 2em; }
        </style>
    """, unsafe_allow_html=True)

    st.image(str(LOGO_UNICA), width=120)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<div class='titulo'>ANALIZADOR DE ELEVADOR DE CANGILONES</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitulo'>Proyecto Integrador — Mecánica</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("INGRESAR", type="primary", use_container_width=True):
            st.session_state.ingresado = True
            st.rerun()

    st.markdown("<div class='footer'>2026 — Proyecto Elevador UNICA</div>", unsafe_allow_html=True)

def aplicacion_principal():
    with st.sidebar:
        st.image(str(LOGO_UNICA), width=150)
        st.markdown("### UNICA")
        menu = st.radio(
            "Menu",
            ["Inicio", "Analisis", "Historial", "Graficas", "Exportar", "Enlace web"],
        )
        if URL_STREAMLIT:
            st.link_button("Abrir app publicada", URL_STREAMLIT, use_container_width=True)
        else:
            st.caption("Enlace web pendiente de publicacion")

        if st.button("Volver a Portada"):
            st.session_state.ingresado = False
            st.rerun()

    col_logo, col_titulo = st.columns([1, 5])
    with col_logo:
        st.image(str(LOGO_UNICA), width=105)
    with col_titulo:
        st.title("Elevador de cangilones para granos")
        st.caption("Analisis de estabilidad, acumulacion en bota y riesgo operativo")

    if menu == "Inicio":
        st.subheader("Proyecto integrador de Mecanica")
        st.write(
            "Esta aplicacion organiza el analisis del elevador de cangilones: "
            "capacidad de evacuacion, acumulacion de grano, centro de masa, "
            "estabilidad y riesgos de operacion."
        )
        if URL_STREAMLIT:
            st.info(f"App publicada en Streamlit: {URL_STREAMLIT}")
        else:
            st.info("Cuando publiques esta app en Streamlit Cloud, pega el enlace real en app.py y main.py.")
        st.image(str(IMAGEN_ELEVADOR), use_container_width=True)

    elif menu == "Analisis":
        st.subheader("Datos del turno")
        c1, c2, c3 = st.columns(3)

        with c1:
            flujo = st.number_input("Flujo de entrada (t/h)", min_value=0.01, value=18.0)
            humedad = st.number_input("Humedad del grano (%)", min_value=0.0, value=16.0)
            velocidad = st.number_input("Velocidad de correa (m/s)", min_value=0.01, value=1.25)
            capacidad = st.number_input("Capacidad del cangilon (L)", min_value=0.01, value=3.5)
            cangilones = st.number_input("Cangilones por metro", min_value=0.01, value=2.4)
            densidad = st.number_input("Densidad del grano (t/m3)", min_value=0.01, value=0.72)

        with c2:
            tiempo = st.number_input("Tiempo observado (min)", min_value=0.01, value=12.0)
            altura = st.number_input("Altura del elevador (m)", min_value=0.01, value=8.0)
            masa_estructura = st.number_input("Masa de estructura (kg)", min_value=0.01, value=1150.0)
            masa_grano = st.number_input("Masa de grano en banda (kg)", min_value=0.0, value=280.0)
            desplazamiento = st.number_input("Desplazamiento de carga (m)", value=0.32)
            base = st.number_input("Ancho de base (m)", min_value=0.01, value=1.35)

        with c3:
            viento = st.number_input("Empuje lateral (N)", min_value=0.0, value=90.0)
            altura_viento = st.number_input("Altura del empuje (m)", min_value=0.0, value=5.5)
            horas = st.number_input("Horas sin mantenimiento", min_value=0.01, value=950.0)
            impurezas = st.number_input("Impurezas (g/kg)", min_value=0.0, value=3.0)
            tension = st.number_input("Tension de correa (kN)", min_value=0.01, value=8.5)

        if st.button("Analizar turno", type="primary"):
            resultado = resumen_calculo(
                flujo,
                humedad,
                velocidad,
                capacidad,
                cangilones,
                densidad,
                tiempo,
                altura,
                masa_estructura,
                masa_grano,
                desplazamiento,
                base,
                viento,
                altura_viento,
                horas,
                impurezas,
                tension,
            )
            st.session_state.historial.append(resultado)

        if st.session_state.historial:
            r = st.session_state.historial[-1]
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Salida real", f"{r['salida_t_h']} t/h")
            k2.metric("Acumulacion", f"{r['volumen_acumulado_m3']} m3")
            k3.metric("Margen estabilidad", f"{r['margen_Nm']} N.m")
            k4.metric("Riesgo general", f"{r['riesgo_general'] * 100:.1f}%")
            st.write(f"Estado de estabilidad: **{r['estado_estabilidad']}**")
            st.write(f"Nivel de riesgo: **{r['nivel_riesgo']}**")

    elif menu == "Historial":
        if st.session_state.historial:
            df = pd.DataFrame(st.session_state.historial)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Todavia no hay registros.")

    elif menu == "Graficas":
        if st.session_state.historial:
            df = pd.DataFrame(st.session_state.historial)
            opcion = st.selectbox("Grafica", ["Riesgo", "Entrada vs salida", "Atasco vs rotura"])
            if opcion == "Riesgo":
                st.line_chart(df["riesgo_general"] * 100)
            elif opcion == "Entrada vs salida":
                st.bar_chart(df[["flujo_entrada_t_h", "salida_t_h"]])
            else:
                st.line_chart(df[["prob_atasco", "prob_rotura"]] * 100)
        else:
            st.info("Registra un analisis para ver graficas.")

    elif menu == "Exportar":
        if st.session_state.historial:
            df = pd.DataFrame(st.session_state.historial)
            st.download_button(
                "Descargar CSV",
                df.to_csv(index=False).encode("utf-8-sig"),
                "bitacora_elevador_cangilones.csv",
                "text/csv",
            )
            st.download_button(
                "Descargar TXT",
                df.to_string(index=False).encode("utf-8"),
                "reporte_elevador_cangilones.txt",
                "text/plain",
            )
        else:
            st.info("No hay datos para exportar.")

    else:
        st.subheader("Enlace de la aplicacion web")
        if URL_STREAMLIT:
            st.write("La aplicacion publicada se abre desde este enlace:")
            st.code(URL_STREAMLIT)
            st.link_button("Abrir en Streamlit", URL_STREAMLIT)
        else:
            st.warning("Todavia no se ha colocado el enlace real de esta app.")
            st.write("Publica el proyecto en Streamlit Cloud y luego reemplaza `URL_STREAMLIT` por el enlace generado.")

if not st.session_state.ingresado:
    pantalla_inicio()
else:
    aplicacion_principal()