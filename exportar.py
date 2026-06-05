from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

import pandas as pd


COLOR_FONDO = "#18211f"
COLOR_PANEL = "#f7f1e5"
COLOR_TEXTO = "#18211f"
COLOR_VERDE = "#6f8f3f"


def construir_tab_exportar(tab, historial):
    tab.configure(bg=COLOR_FONDO)
    panel = tk.Frame(tab, bg=COLOR_PANEL)
    panel.pack(fill="both", expand=True, padx=18, pady=18)

    tk.Label(
        panel,
        text="Bitacora del elevador",
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO,
        font=("Segoe UI", 18, "bold"),
    ).pack(anchor="w", padx=16, pady=(16, 4))
    tk.Label(
        panel,
        text="Exporta los turnos analizados para adjuntarlos al avance del proyecto.",
        bg=COLOR_PANEL,
        fg="#6f665d",
        font=("Segoe UI", 10),
    ).pack(anchor="w", padx=16, pady=(0, 18))

    def dataframe():
        if not historial:
            messagebox.showwarning("Sin registros", "Haz al menos un analisis antes de exportar.")
            return None
        return pd.DataFrame(historial)

    def exportar_csv():
        df = dataframe()
        if df is None:
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivo CSV", "*.csv")],
            initialfile="bitacora_elevador_cangilones.csv",
        )
        if ruta:
            df.to_csv(ruta, index=False, encoding="utf-8-sig")
            messagebox.showinfo("Listo", f"CSV guardado en:\n{ruta}")

    def exportar_txt():
        df = dataframe()
        if df is None:
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt")],
            initialfile="reporte_elevador_cangilones.txt",
        )
        if ruta:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("Reporte del elevador de cangilones para granos\n")
                archivo.write(f"Generado: {datetime.now():%Y-%m-%d %H:%M}\n\n")
                archivo.write(df.to_string(index=False))
            messagebox.showinfo("Listo", f"TXT guardado en:\n{ruta}")

    tk.Button(
        panel,
        text="Guardar CSV",
        command=exportar_csv,
        bg=COLOR_VERDE,
        fg="white",
        relief="flat",
        width=18,
        font=("Segoe UI", 11, "bold"),
    ).pack(anchor="w", padx=16, pady=7)
    tk.Button(
        panel,
        text="Guardar TXT",
        command=exportar_txt,
        bg=COLOR_VERDE,
        fg="white",
        relief="flat",
        width=18,
        font=("Segoe UI", 11, "bold"),
    ).pack(anchor="w", padx=16, pady=7)
