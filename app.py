import pandas as pd
import streamlit as st
from pathlib import Path
from Calculos import resumen_calculo

st.set_page_config(page_title="Elevador de Cangilones", layout="wide", initial_sidebar_state="expanded")

BASE_DIR = Path(__file__).resolve().parent
LOGO_UNICA = BASE_DIR / "logo_unica.png"
IMAGEN_ELEVADOR = BASE_DIR / "elevador_cangilones.png"

if "historial" not in st.session_state:
    st.session_state.historial = []

if "ingresado" not in st.session_state:
    st.session_state.ingresado = False

def inyectar_estilos():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Montserrat', sans-serif;
            background-color: #0b0f19;
            color: #e2e8f0;
        }
        
        .stApp {
            background-color: #0b0f19;
            background-image: radial-gradient(circle at 50% 0%, #1a2235 0%, #0b0f19 70%);
        }
        
        h1, h2, h3 {
            color: #f4b41a !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #f4b41a 0%, #d48f00 100%);
            color: #0b0f19 !important;
            font-weight: 600;
            border: none;
            border-radius: 4px;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(244, 180, 26, 0.2);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(244, 180, 26, 0.4);
        }
        
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
            background-color: #121826;
            border: 1px solid #2d3748;
            color: #ffffff;
            border-radius: 4px;
        }
        
        div[data-testid="stMetricValue"] {
            color: #f4b41a;
            font-size: 2.5rem;
            font-weight: 800;
        }
        
        div[data-testid="stMetricLabel"] {
            color: #a0aec0;
            font-size: 1rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .tarjeta-premium {
            background-color: #1a2235;
            border: 1px solid #2d3748;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin-bottom: 2rem;
        }
        
        .titulo-portada {
            text-align: center;
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(to right, #ffffff, #a0aec0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0;
            padding-top: 2rem;
        }
        
        .subtitulo-portada {
            text-align: center;
            color: #f4b41a;
            font-size: 1.5rem;
            font-weight: 300;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-top: 1rem;
            margin-bottom: 4rem;
        }
        
        .footer {
            text-align: center;
            color: #4a5568;
            font-size: 0.85rem;
            margin-top: 5rem;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        hr {
            border-color: #2d3748;
            margin: 2rem 0;
        }
        
        [data-testid="stSidebar"] {
            background-color: #121826;
            border-right: 1px solid #2d3748;
        }
        </style>
    """, unsafe_allow_html=True)

def pantalla_inicio():
    inyectar_estilos()
    
    col_logo_izq, col_vacia = st.columns([1, 5])
    with col_logo_izq:
        st.image(str(LOGO_UNICA), width=100)
    
    st.markdown("<h1 class='titulo-portada'>ANALIZADOR DE ESTABILIDAD</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitulo-portada'>Elevador de Cangilones</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div class='tarjeta-premium'>", unsafe_allow_html=True)
        if st.button("INICIAR SISTEMA", use_container_width=True):
            st.session_state.ingresado = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<div class='footer'>2027 - UNIVERSIDAD CARDENAL MIGUEL OBANDO BRAVO</div>", unsafe_allow_html=True)

def aplicacion_principal():
    inyectar_estilos()
    
    with st.sidebar:
        st.image(str(LOGO_UNICA), width=150)
        st.markdown("### UNICA")
        menu = st.radio(
            "Menu",
            ["Inicio", "Analisis", "Historial", "Graficas", "Exportar"],
        )
        st.markdown("<br><br>", unsafe_allow_html=True)
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
            st.markdown("<div class='tarjeta-premium'>", unsafe_allow_html=True)
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Salida real", f"{r['salida_t_h']} t/h")
            k2.metric("Acumulacion", f"{r['volumen_acumulado_m3']} m3")
            k3.metric("Margen estabilidad", f"{r['margen_Nm']} N.m")
            k4.metric("Riesgo general", f"{r['riesgo_general'] * 100:.1f}%")
            st.write(f"Estado de estabilidad: **{r['estado_estabilidad']}**")
            st.write(f"Nivel de riesgo: **{r['nivel_riesgo']}**")
            st.markdown("</div>", unsafe_allow_html=True)

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

if not st.session_state.ingresado:
    pantalla_inicio()
else:
    aplicacion_principal()