import tkinter as tk
from tkinter import messagebox

from Calculos import resumen_calculo


COLOR_FONDO = "#18211f"
COLOR_PANEL = "#f7f1e5"
COLOR_PANEL_OSCURO = "#26352f"
COLOR_TEXTO = "#18211f"
COLOR_VERDE = "#6f8f3f"
COLOR_TIERRA = "#b06f37"


def campo(panel, texto, fila, valor, ancho=12):
    tk.Label(panel, text=texto, bg=COLOR_PANEL, fg=COLOR_TEXTO, anchor="w").grid(
        row=fila,
        column=0,
        sticky="we",
        padx=(12, 6),
        pady=4,
    )
    entrada = tk.Entry(panel, width=ancho, relief="flat", bg="#fffdf7")
    entrada.insert(0, valor)
    entrada.grid(row=fila, column=1, sticky="we", padx=(6, 12), pady=4)
    return entrada


def tarjeta_resultado(panel, titulo, valor, detalle=""):
    caja = tk.Frame(panel, bg="#fffdf7", highlightbackground="#ddc7a1", highlightthickness=1)
    caja.pack(fill="x", padx=14, pady=5)
    tk.Label(caja, text=titulo, bg="#fffdf7", fg="#5a4630", font=("Segoe UI", 9, "bold")).pack(
        anchor="w",
        padx=10,
        pady=(8, 0),
    )
    tk.Label(caja, text=str(valor), bg="#fffdf7", fg=COLOR_TEXTO, font=("Segoe UI", 15, "bold")).pack(
        anchor="w",
        padx=10,
    )
    if detalle:
        tk.Label(caja, text=detalle, bg="#fffdf7", fg="#6f665d", font=("Segoe UI", 9)).pack(
            anchor="w",
            padx=10,
            pady=(0, 8),
        )


def mostrar_resultados(panel, datos):
    for widget in panel.winfo_children():
        widget.destroy()

    banda = tk.Frame(panel, bg=datos["color_riesgo"], height=58)
    banda.pack(fill="x")
    tk.Label(
        banda,
        text=f"Riesgo operativo: {datos['nivel_riesgo'].upper()}",
        bg=datos["color_riesgo"],
        fg="white",
        font=("Segoe UI", 17, "bold"),
    ).pack(anchor="w", padx=16, pady=12)

    tarjeta_resultado(panel, "Caudal real de salida", f"{datos['salida_t_h']} t/h", f"Eficiencia por humedad: {datos['eficiencia']}")
    tarjeta_resultado(panel, "Acumulacion en bota", f"{datos['volumen_acumulado_m3']} m3", f"Exceso: {datos['exceso_t_h']} t/h")
    tarjeta_resultado(panel, "Centro de masa", f"x={datos['x_cm_m']} m | y={datos['y_cm_m']} m", f"Masa total: {datos['masa_total_kg']} kg")
    tarjeta_resultado(panel, "Momento de inercia", f"{datos['momento_inercia_kg_m2']} kg.m2")
    tarjeta_resultado(panel, "Estabilidad", datos["estado_estabilidad"], f"Margen: {datos['margen_Nm']} N.m")
    tarjeta_resultado(panel, "Probabilidad de atasco", f"{datos['prob_atasco'] * 100:.1f}%")
    tarjeta_resultado(panel, "Probabilidad de rotura", f"{datos['prob_rotura'] * 100:.1f}%")


def construir_tab_calculos(tab, historial):
    tab.configure(bg=COLOR_FONDO)

    izquierda = tk.Frame(tab, bg=COLOR_PANEL)
    izquierda.pack(side="left", fill="y", padx=18, pady=18)

    derecha = tk.Frame(tab, bg=COLOR_PANEL)
    derecha.pack(side="left", fill="both", expand=True, padx=(0, 18), pady=18)

    tk.Label(
        izquierda,
        text="Elevador de cangilones",
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO,
        font=("Segoe UI", 18, "bold"),
    ).grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(12, 2))
    tk.Label(
        izquierda,
        text="Datos de operacion y maqueta",
        bg=COLOR_PANEL,
        fg="#6f665d",
        font=("Segoe UI", 10),
    ).grid(row=1, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 10))

    entradas = {
        "flujo": campo(izquierda, "Flujo de entrada (t/h)", 2, "18"),
        "humedad": campo(izquierda, "Humedad del grano (%)", 3, "16"),
        "velocidad": campo(izquierda, "Velocidad correa (m/s)", 4, "1.25"),
        "capacidad": campo(izquierda, "Capacidad cangilon (L)", 5, "3.5"),
        "cangilones": campo(izquierda, "Cangilones por metro", 6, "2.4"),
        "densidad": campo(izquierda, "Densidad grano (t/m3)", 7, "0.72"),
        "tiempo": campo(izquierda, "Tiempo observado (min)", 8, "12"),
        "altura": campo(izquierda, "Altura elevador (m)", 9, "8"),
        "estructura": campo(izquierda, "Masa estructura (kg)", 10, "1150"),
        "grano": campo(izquierda, "Masa grano en banda (kg)", 11, "280"),
        "desplazamiento": campo(izquierda, "Desplazamiento carga (m)", 12, "0.32"),
        "base": campo(izquierda, "Ancho de base (m)", 13, "1.35"),
        "viento": campo(izquierda, "Empuje lateral (N)", 14, "90"),
        "altura_viento": campo(izquierda, "Altura del empuje (m)", 15, "5.5"),
        "horas": campo(izquierda, "Horas sin mantenimiento", 16, "950"),
        "impurezas": campo(izquierda, "Impurezas (g/kg)", 17, "3"),
        "tension": campo(izquierda, "Tension correa (kN)", 18, "8.5"),
    }

    def leer(nombre):
        return float(entradas[nombre].get())

    def calcular():
        try:
            datos = resumen_calculo(
                leer("flujo"),
                leer("humedad"),
                leer("velocidad"),
                leer("capacidad"),
                leer("cangilones"),
                leer("densidad"),
                leer("tiempo"),
                leer("altura"),
                leer("estructura"),
                leer("grano"),
                leer("desplazamiento"),
                leer("base"),
                leer("viento"),
                leer("altura_viento"),
                leer("horas"),
                leer("impurezas"),
                leer("tension"),
            )
            historial.append(datos)
            mostrar_resultados(derecha, datos)
        except ValueError as error:
            messagebox.showerror("Dato por revisar", str(error))

    tk.Button(
        izquierda,
        text="Analizar turno",
        command=calcular,
        bg=COLOR_VERDE,
        fg="white",
        relief="flat",
        font=("Segoe UI", 11, "bold"),
    ).grid(row=19, column=0, columnspan=2, sticky="we", padx=12, pady=14)

    calcular()
