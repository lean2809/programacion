# Proyecto: Elevador de Cangilones para Granos

Aplicacion en Python basada en el avance del proyecto de Mecanica. El programa analiza
un elevador de cangilones considerando caudal de entrada, capacidad de evacuacion,
humedad del grano, estabilidad, centro de masa, momento de inercia y riesgo operativo.

## Estructura

- `Calculos.py`: formulas mecanicas y probabilisticas.
- `interfaz.py`: pantalla principal de entrada y resultados.
- `historial.py`: tabla de turnos analizados.
- `graficas.py`: graficas del comportamiento del elevador.
- `exportar.py`: exportacion CSV/TXT.
- `main.py`: aplicacion de escritorio con Tkinter.
- `app.py`: version web con Streamlit.
- `logo_unica.png`: logo de la universidad usado en escritorio y web.
- `requirements.txt`: librerias necesarias.

## Instalar librerias

```powershell
python -m pip install -r requirements.txt
```

## Ejecutar la version de escritorio

```powershell
python main.py
```

## Enlace web de la app

```text
Enlace de streamlit
```

https://elevadordecangilonesparagranos.streamlit.app

## Que calcula

- Capacidad real de salida del elevador en toneladas por hora.
- Acumulacion posible de grano en la bota.
- Centro de masa aproximado de estructura y carga.
- Momento de inercia estimado del sistema.
- Margen de estabilidad frente a volcamiento.
- Probabilidad de atasco por sobrealimentacion, humedad y baja velocidad.
- Probabilidad de rotura de cangilones por fatiga, impurezas y tension.

## Uso sugerido

1. Ingresar datos del turno en `Analisis`.
2. Presionar `Analizar turno`.
3. Revisar el nivel de riesgo y los momentos calculados.
4. Consultar `Historial` y `Graficas` para comparar registros.
5. Exportar el reporte en `CSV` o `TXT`.
