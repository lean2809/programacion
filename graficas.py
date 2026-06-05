import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


COLOR_FONDO = "#18211f"
COLOR_PANEL = "#f7f1e5"
COLOR_VERDE = "#6f8f3f"
COLOR_TIERRA = "#b06f37"


def construir_tab_graficas(tab, historial):
    tab.configure(bg=COLOR_FONDO)
    barra = tk.Frame(tab, bg=COLOR_PANEL)
    barra.pack(fill="x", padx=18, pady=(18, 0))

    lienzo = tk.Frame(tab, bg=COLOR_PANEL)
    lienzo.pack(fill="both", expand=True, padx=18, pady=18)

    seleccion = tk.StringVar(value="Riesgo por turno")
    opciones = ["Riesgo por turno", "Entrada vs salida", "Centro de masa", "Atasco vs rotura"]
    ttk.Combobox(barra, textvariable=seleccion, values=opciones, state="readonly", width=24).pack(
        side="left",
        padx=12,
        pady=12,
    )

    estado = {"canvas": None}

    def limpiar():
        for widget in lienzo.winfo_children():
            widget.destroy()
        if estado["canvas"] is not None:
            estado["canvas"] = None

    def dibujar():
        limpiar()
        if not historial:
            tk.Label(
                lienzo,
                text="Primero registra un analisis en la pestana de calculos.",
                bg=COLOR_PANEL,
                fg="#5a4630",
                font=("Segoe UI", 12),
            ).pack(pady=30)
            return

        df = pd.DataFrame(historial)
        x = list(range(1, len(df) + 1))
        fig, ax = plt.subplots(figsize=(8.5, 4.5))
        fig.patch.set_facecolor(COLOR_PANEL)
        ax.set_facecolor("#fffdf7")

        if seleccion.get() == "Riesgo por turno":
            ax.plot(x, df["riesgo_general"] * 100, marker="o", color=COLOR_TIERRA)
            ax.set_ylabel("Riesgo (%)")
            ax.set_title("Riesgo operativo general")
        elif seleccion.get() == "Entrada vs salida":
            ax.bar(x, df["flujo_entrada_t_h"], label="Entrada", color=COLOR_TIERRA)
            ax.bar(x, df["salida_t_h"], label="Salida", color=COLOR_VERDE, alpha=0.85)
            ax.set_ylabel("t/h")
            ax.set_title("Capacidad de evacuacion del elevador")
            ax.legend()
        elif seleccion.get() == "Centro de masa":
            ax.scatter(df["x_cm_m"], df["y_cm_m"], s=90, color=COLOR_TIERRA)
            ax.axvline(0, color="#888", linestyle="--")
            ax.set_xlabel("x del centro de masa (m)")
            ax.set_ylabel("altura del centro de masa (m)")
            ax.set_title("Ubicacion estimada del centro de masa")
        else:
            ax.plot(x, df["prob_atasco"] * 100, marker="o", label="Atasco", color=COLOR_TIERRA)
            ax.plot(x, df["prob_rotura"] * 100, marker="o", label="Rotura", color=COLOR_VERDE)
            ax.set_ylabel("Probabilidad (%)")
            ax.set_title("Comparacion de sucesos de riesgo")
            ax.legend()

        ax.grid(True, alpha=0.25)
        canvas = FigureCanvasTkAgg(fig, master=lienzo)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)
        estado["canvas"] = canvas

    tk.Button(
        barra,
        text="Ver grafica",
        command=dibujar,
        bg=COLOR_VERDE,
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
    ).pack(side="left", pady=12)
