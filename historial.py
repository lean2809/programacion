import tkinter as tk
from tkinter import ttk

import pandas as pd


COLOR_FONDO = "#18211f"
COLOR_PANEL = "#f7f1e5"
COLOR_TEXTO = "#18211f"
COLOR_VERDE = "#6f8f3f"


def construir_tab_historial(tab, historial):
    tab.configure(bg=COLOR_FONDO)
    panel = tk.Frame(tab, bg=COLOR_PANEL)
    panel.pack(fill="both", expand=True, padx=18, pady=18)

    resumen = tk.Label(panel, bg=COLOR_PANEL, fg=COLOR_TEXTO, font=("Segoe UI", 11, "bold"))
    resumen.pack(anchor="w", padx=12, pady=(12, 8))

    columnas = [
        "flujo_entrada_t_h",
        "salida_t_h",
        "volumen_acumulado_m3",
        "estado_estabilidad",
        "prob_atasco",
        "prob_rotura",
        "nivel_riesgo",
    ]

    tabla = ttk.Treeview(panel, columns=columnas, show="headings", height=15)
    for columna in columnas:
        tabla.heading(columna, text=columna)
        tabla.column(columna, anchor="center", width=145)
    tabla.pack(fill="both", expand=True, padx=12)

    def actualizar():
        for item in tabla.get_children():
            tabla.delete(item)

        if not historial:
            resumen.config(text="No hay turnos registrados todavia.")
            return

        df = pd.DataFrame(historial)
        for _, fila in df.iterrows():
            tabla.insert("", "end", values=[fila.get(columna, "") for columna in columnas])

        texto = (
            f"Registros: {len(df)}  |  "
            f"Riesgo max: {df['riesgo_general'].max() * 100:.1f}%  |  "
            f"Acumulacion promedio: {df['volumen_acumulado_m3'].mean():.2f} m3  |  "
            f"Salida promedio: {df['salida_t_h'].mean():.2f} t/h"
        )
        resumen.config(text=texto)

    tk.Button(
        panel,
        text="Actualizar historial",
        command=actualizar,
        bg=COLOR_VERDE,
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
    ).pack(anchor="e", padx=12, pady=12)
