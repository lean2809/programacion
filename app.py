import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Elevador de Cangilones", layout="wide", initial_sidebar_state="expanded")

BASE_DIR = Path(__file__).resolve().parent
LOGO_UNICA = BASE_DIR / "logo_unica.png"
IMAGEN_ELEVADOR = BASE_DIR / "elevador_cangilones.png"

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
        
    st.markdown("<div class='footer'>2027 — UNIVERSIDAD CARDENAL MIGUEL OBANDO BRAVO</div>", unsafe_allow_html=True)

def aplicacion_principal():
    inyectar_estilos()
    
    with st.sidebar:
        st.image(str(LOGO_UNICA), width=120)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        opcion = st.radio(
            "NAVEGACIÓN",
            ["Panel de Control", "Configuración de Variables", "Registro de Operaciones", "Análisis Gráfico"]
        )
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.button("Cerrar Sesión", use_container_width=True):
            st.session_state.ingresado = False
            st.rerun()

    st.markdown("<h1>CENTRO DE MANDO</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    if opcion == "Panel de Control":
        st.markdown("<div class='tarjeta-premium'>", unsafe_allow_html=True)
        st.markdown("<h3>Indicadores de Rendimiento</h3>", unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Salida Real", "0.00 t/h")
        m2.metric("Acumulación", "0.00 m3")
        m3.metric("Margen Estabilidad", "0.00 N.m")
        m4.metric("Riesgo General", "0.0%")
        st.markdown("</div>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.markdown("<div class='tarjeta-premium'>", unsafe_allow_html=True)
            st.markdown("<h3>Esquema Estructural</h3>", unsafe_allow_html=True)
            st.image(str(IMAGEN_ELEVADOR), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_b:
            st.markdown("<div class='tarjeta-premium'>", unsafe_allow_html=True)
            st.markdown("<h3>Estado del Sistema</h3>", unsafe_allow_html=True)
            st.success("Conexión Estable")
            st.info("Módulos Calibrados")
            st.warning("Esperando Entrada de Datos")
            st.markdown("</div>", unsafe_allow_html=True)

    elif opcion == "Configuración de Variables":
        st.markdown("<div class='tarjeta-premium'>", unsafe_allow_html=True)
        st.markdown("<h3>Parámetros de Entrada</h3>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.number_input("Flujo de entrada (t/h)", value=18.0)
            st.number_input("Humedad del grano (%)", value=16.0)
            st.number_input("Velocidad de correa (m/s)", value=1.25)
        with c2:
            st.number_input("Tiempo observado (min)", value=12.0)
            st.number_input("Altura del elevador (m)", value=8.0)
            st.number_input("Masa de estructura (kg)", value=1150.0)
        with c3:
            st.number_input("Empuje lateral (N)", value=90.0)
            st.number_input("Altura del empuje (m)", value=5.5)
            st.number_input("Horas sin mantenimiento", value=950.0)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Procesar Datos Operativos", type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

    elif opcion == "Registro de Operaciones":
        st.markdown("<div class='tarjeta-premium'>", unsafe_allow_html=True)
        st.markdown("<h3>Base de Datos Histórica</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif opcion == "Análisis Gráfico":
        st.markdown("<div class='tarjeta-premium'>", unsafe_allow_html=True)
        st.markdown("<h3>Visualización de Tendencias</h3>", unsafe_allow_html=True)
        st.selectbox("Seleccione Métrica", ["Riesgo Operativo", "Flujo vs Salida", "Probabilidad de Falla"])
        st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.ingresado:
    pantalla_inicio()
else:
    aplicacion_principal()