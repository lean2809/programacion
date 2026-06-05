import pandas as pd
import streamlit as st
from pathlib import Path
from Calculos import resumen_calculo

st.set_page_config(page_title="Elevador de Cangilones", layout="wide")

URL_STREAMLIT = ""
BASE_DIR = Path(__file__).resolve().parent
LOGO_UNICA = BASE_DIR / "logo_unica.png"
IMAGEN_ELEVADOR = BASE_DIR / "elevador_cangilones.png"

# Inicializar estados de la sesion
if "historial" not in st.session_state:
    st.session_state.historial = []

if "ingresado" not in st.session_state:
    st.session_state.ingresado = False

# --- PANTALLA DE INICIO (PORTADA) ---
def pantalla_inicio():
    # CSS para imitar los colores oscuros, amarillos y el formato de la imagen
    st.markdown("""
        <style>
        .stApp { background-color: #202c39; }
        .titulo { text-align: center; color: #f4b41a; font-family: 'Segoe UI', sans-serif; font-size: 3em; font-weight: bold; margin-bottom: 0px;}
        .subtitulo { text-align: center; color: #a0aab5; font-size: 1.2em; margin-top: 10px; margin-bottom: 20px;}
        .icono { text-align: center; color: white; font-size: 5em; margin-bottom: -10px;}
        .footer { text-align: center; color: #4a5568; font-size: 0.9em; margin-top: 80px;}
        hr { border-top: 2px solid #f4b41a; margin-top: 2em; margin-bottom: 2em; }
        </style>
    """, unsafe_allow_html=True)

    # Logo UNICA arriba a la izquierda
    st.image(str(LOGO_UNICA), width=120)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Icono central (Elevador/Maquinaria)
    st.markdown("<div class='icono'>🏭⚙️</div>", unsafe_allow_html=True)
    
    # Textos del proyecto
    st.markdown("<div class='titulo'>ANALIZADOR DE ELEVADOR DE CANGILONES</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitulo'>Proyecto Integrador — Mecánica</div>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)

    # Botón centrado
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # El type="primary" en Streamlit genera el botón de color rojo/destacado
        if st.button("▶ INGRESAR", type="primary", use_container_width=True):
            st.session_state.ingresado = True
            st.rerun()

    st.markdown("<div class='footer'>© 2026 — Proyecto Elevador UNICA</div>", unsafe_allow_html=True)


# --- APLICACIÓN PRINCIPAL ---
def aplicacion_principal():
    # Todo el código original de tu interfaz Streamlit va aquí adentro.
    with st.sidebar:
        st.image(str(LOGO_UNICA), width=150)
        st.markdown("### UNICA")
        menu = st.radio(
            "Menu",
            ["Inicio", "Analisis", "Historial", "Graficas", "Exportar", "Enlace web"],
        )
        
        # Botón para regresar a la portada si lo deseas
        if st.button("Volver a Portada"):
            st.session_state.ingresado = False
            st.rerun()

    col_logo, col_titulo = st.columns([1, 5])
    with col_logo:
        st.image(str(LOGO_UNICA), width=105)
    with col_titulo:
        st.title("Elevador de cangilones para granos")
        st.caption("Analisis de estabilidad, acumulacion en bota y riesgo operativo")



# Lógica de enrutamiento
if not st.session_state.ingresado:
    pantalla_inicio()
else:
    aplicacion_principal()