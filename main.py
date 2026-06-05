import tkinter as tk
from tkinter import ttk
import webbrowser
from pathlib import Path

from exportar import construir_tab_exportar
from graficas import construir_tab_graficas
from historial import construir_tab_historial
from interfaz import construir_tab_calculos

COLOR_FONDO = "#18211f"
COLOR_PANEL_OSCURO = "#26352f"
COLOR_CLARO = "#f7f1e5"
COLOR_VERDE = "#6f8f3f"

# Cuando publiques esta app en Streamlit Cloud, pega aqui el enlace real.
URL_STREAMLIT = ""
BASE_DIR = Path(__file__).resolve().parent
LOGO_UNICA = BASE_DIR / "logo_unica.png"


def crear_ventana():
    ventana = tk.Tk()
    ventana.title("Analizador de Elevador de Cangilones")
    ventana.geometry("1180x720")
    ventana.minsize(1040, 640)
    ventana.configure(bg=COLOR_FONDO)
    return ventana

def crear_encabezado(ventana):
    encabezado = tk.Frame(ventana, bg=COLOR_PANEL_OSCURO)
    
    try:
        ventana.logo_unica = tk.PhotoImage(file=str(LOGO_UNICA)).subsample(5, 5)
        tk.Label(encabezado, image=ventana.logo_unica, bg=COLOR_PANEL_OSCURO).pack(
            side="left",
            padx=(20, 10),
            pady=10,
        )
    except tk.TclError:
        ventana.logo_unica = None

    bloque_texto = tk.Frame(encabezado, bg=COLOR_PANEL_OSCURO)
    bloque_texto.pack(side="left", fill="x", expand=True)

    tk.Label(
        bloque_texto,
        text="Elevador de cangilones para granos",
        bg=COLOR_PANEL_OSCURO,
        fg=COLOR_CLARO,
        font=("Segoe UI", 23, "bold"),
    ).pack(anchor="w", padx=22, pady=(16, 2))
    
    tk.Label(
        bloque_texto,
        text="Estabilidad, caudal de evacuacion y riesgo operativo del sistema",
        bg=COLOR_PANEL_OSCURO,
        fg="#d8c9aa",
        font=("Segoe UI", 11),
    ).pack(anchor="w", padx=22, pady=(0, 14))
    
    return encabezado

def crear_pestanas(ventana):
    estilo = ttk.Style()
    estilo.theme_use("default")
    estilo.configure("TNotebook", background=COLOR_FONDO, borderwidth=0)
    estilo.configure("TNotebook.Tab", padding=(18, 8), font=("Segoe UI", 10))

    notebook = ttk.Notebook(ventana)
    tabs = [tk.Frame(notebook) for _ in range(4)]
    nombres = ["Analisis", "Historial", "Graficas", "Exportar"]
    for tab, nombre in zip(tabs, nombres):
        notebook.add(tab, text=nombre)
        
    return notebook, tabs

def crear_menu(ventana, notebook):
    menu = tk.Menu(ventana)

    archivo = tk.Menu(menu, tearoff=0)
    archivo.add_command(label="Salir", command=ventana.destroy)
    menu.add_cascade(label="Archivo", menu=archivo)

    navegacion = tk.Menu(menu, tearoff=0)
    for indice, nombre in enumerate(["Analisis", "Historial", "Graficas", "Exportar"]):
        navegacion.add_command(label=nombre, command=lambda i=indice: notebook.select(i))
    menu.add_cascade(label="Menu", menu=navegacion)

    web = tk.Menu(menu, tearoff=0)
    web.add_command(
        label="Abrir app en Streamlit",
        command=lambda: webbrowser.open(URL_STREAMLIT) if URL_STREAMLIT else print("Enlace web pendiente"),
    )
    web.add_command(label="Copiar enlace en consola", command=lambda: print(URL_STREAMLIT or "Enlace web pendiente"))
    menu.add_cascade(label="Web", menu=web)

    ayuda = tk.Menu(menu, tearoff=0)
    ayuda.add_command(
        label="Acerca del proyecto",
        command=lambda: notebook.select(0),
    )
    menu.add_cascade(label="Ayuda", menu=ayuda)

    return menu

def crear_pie(ventana):
    pie = tk.Label(
        ventana,
        text="Proyecto integrador de Mecanica - Ingenieria Industrial",
        bg=COLOR_FONDO,
        fg="#d8c9aa",
        font=("Segoe UI", 9),
    )
    return pie

def crear_pantalla_inicio(ventana, encabezado, notebook, menu_principal, pie):
    # Crear la pantalla que cubre todo con fondo oscuro
    pantalla = tk.Frame(ventana, bg="#202c39")
    pantalla.pack(fill="both", expand=True)
    
    # Colocar logo arriba a la izquierda
    if ventana.logo_unica:
        tk.Label(pantalla, image=ventana.logo_unica, bg="#202c39").pack(anchor="nw", padx=20, pady=20)
    
    # Contenedor central para alinear los elementos
    centro = tk.Frame(pantalla, bg="#202c39")
    centro.place(relx=0.5, rely=0.5, anchor="center")
    
    # Icono placeholder (texto)
    tk.Label(centro, text="🏭⚙️", bg="#202c39", fg="white", font=("Segoe UI", 60)).pack(pady=(0, 10))
    
    # Título principal (Color amarillo)
    tk.Label(
        centro, 
        text="ANALIZADOR DE ELEVADOR DE CANGILONES", 
        bg="#202c39", fg="#f4b41a", font=("Segoe UI", 28, "bold")
    ).pack()
    
    # Subtítulo
    tk.Label(
        centro, 
        text="Proyecto Integrador — Mecánica", 
        bg="#202c39", fg="#a0aab5", font=("Segoe UI", 12)
    ).pack(pady=(5, 30))
    
    # Línea separadora amarilla
    tk.Frame(centro, bg="#f4b41a", height=3, width=600).pack(pady=20)
    
    # Función que destruye la portada y muestra la interfaz principal
    def ingresar():
        pantalla.destroy()  
        ventana.config(menu=menu_principal)  
        encabezado.pack(fill="x")
        notebook.pack(fill="both", expand=True)  
        pie.pack(fill="x", pady=6) 
        
    # Botón Rojo
    btn_ingresar = tk.Button(
        centro, text="▶ INGRESAR", command=ingresar, 
        bg="#ff4b4b", fg="white", font=("Segoe UI", 12, "bold"), 
        relief="flat", width=25, pady=8, activebackground="#e64343", activeforeground="white",
        cursor="hand2"
    )
    btn_ingresar.pack(pady=20)
    
    # Footer de la portada
    tk.Label(
        pantalla, text="© 2026 — Proyecto Elevador UNICA", 
        bg="#202c39", fg="#4a5568", font=("Segoe UI", 9)
    ).pack(side="bottom", pady=20)


if __name__ == "__main__":
    historial = []
    
    # 1. Creamos la ventana base
    ventana = crear_ventana()
    
    # 2. Construimos los elementos de la interfaz pero aún NO los mostramos (no hacemos pack)
    encabezado = crear_encabezado(ventana)
    notebook, tabs = crear_pestanas(ventana)
    menu_principal = crear_menu(ventana, notebook)
    pie = crear_pie(ventana)
    
    # 3. Construimos el contenido interior de las pestañas
    tab_analisis, tab_historial, tab_graficas, tab_exportar = tabs
    construir_tab_calculos(tab_analisis, historial)
    construir_tab_historial(tab_historial, historial)
    construir_tab_graficas(tab_graficas, historial)
    construir_tab_exportar(tab_exportar, historial)
    
    # 4. Lanzamos la pantalla de inicio sobre la ventana base
    crear_pantalla_inicio(ventana, encabezado, notebook, menu_principal, pie)
    
    # 5. Arrancamos la aplicación
    ventana.mainloop()