import math


GRAVEDAD = 9.81


def limitar(valor, minimo=0.0, maximo=1.0):
    return max(minimo, min(maximo, valor))


def validar_positivo(valor, nombre):
    if valor <= 0:
        raise ValueError(f"{nombre} debe ser mayor que cero")


def eficiencia_por_humedad(humedad_pct):
    """La humedad alta vuelve el grano mas pesado y menos fluido."""
    if humedad_pct <= 14:
        return 0.92
    castigo = (humedad_pct - 14) * 0.025
    return round(limitar(0.92 - castigo, 0.50, 0.92), 3)


def calcular_salida_t_h(capacidad_cangilon_l, cangilones_por_m, velocidad_m_s, densidad_t_m3, humedad_pct):
    validar_positivo(capacidad_cangilon_l, "La capacidad del cangilon")
    validar_positivo(cangilones_por_m, "La cantidad de cangilones por metro")
    validar_positivo(velocidad_m_s, "La velocidad de la correa")
    validar_positivo(densidad_t_m3, "La densidad del grano")

    eficiencia = eficiencia_por_humedad(humedad_pct)
    volumen_m3_s = (capacidad_cangilon_l / 1000) * cangilones_por_m * velocidad_m_s * eficiencia
    salida_t_h = volumen_m3_s * densidad_t_m3 * 3600
    return round(salida_t_h, 2), eficiencia


def calcular_acumulacion(flujo_entrada_t_h, salida_t_h, densidad_t_m3, tiempo_min):
    validar_positivo(densidad_t_m3, "La densidad del grano")
    validar_positivo(tiempo_min, "El tiempo observado")

    exceso_t_h = max(0, flujo_entrada_t_h - salida_t_h)
    masa_exceso_t = exceso_t_h * (tiempo_min / 60)
    volumen_m3 = masa_exceso_t / densidad_t_m3
    return {
        "exceso_t_h": round(exceso_t_h, 2),
        "masa_acumulada_t": round(masa_exceso_t, 3),
        "volumen_acumulado_m3": round(volumen_m3, 3),
    }


def calcular_centro_masa(altura_m, masa_estructura_kg, masa_grano_kg, desplazamiento_carga_m):
    validar_positivo(altura_m, "La altura del elevador")
    validar_positivo(masa_estructura_kg, "La masa de la estructura")

    # Separamos la torre y la carga porque en la maqueta se comportan distinto.
    x_estructura = 0.0
    y_estructura = altura_m / 2
    x_grano = desplazamiento_carga_m
    y_grano = altura_m * 0.58

    masa_total = masa_estructura_kg + masa_grano_kg
    validar_positivo(masa_total, "La masa total")

    x_cm = ((masa_estructura_kg * x_estructura) + (masa_grano_kg * x_grano)) / masa_total
    y_cm = ((masa_estructura_kg * y_estructura) + (masa_grano_kg * y_grano)) / masa_total
    return {
        "masa_total_kg": round(masa_total, 2),
        "x_cm_m": round(x_cm, 3),
        "y_cm_m": round(y_cm, 3),
    }


def calcular_momento_inercia(altura_m, masa_estructura_kg, masa_grano_kg, x_cm_m):
    # Aproximacion sencilla: torre como barra vertical y grano como carga puntual.
    inercia_torre = (masa_estructura_kg * altura_m**2) / 12
    inercia_grano = masa_grano_kg * x_cm_m**2
    return round(inercia_torre + inercia_grano, 2)


def evaluar_estabilidad(masa_total_kg, ancho_base_m, x_cm_m, viento_n=0, altura_viento_m=1):
    validar_positivo(ancho_base_m, "El ancho de base")

    peso_n = masa_total_kg * GRAVEDAD
    brazo_seguro = ancho_base_m / 2
    momento_estable = peso_n * brazo_seguro
    momento_volcador = peso_n * abs(x_cm_m) + (viento_n * altura_viento_m)
    margen = momento_estable - momento_volcador

    if margen > momento_estable * 0.35:
        estado = "estable"
    elif margen > 0:
        estado = "vigilar"
    else:
        estado = "riesgo de volcamiento"

    return {
        "peso_total_N": round(peso_n, 2),
        "momento_estable_Nm": round(momento_estable, 2),
        "momento_volcador_Nm": round(momento_volcador, 2),
        "margen_Nm": round(margen, 2),
        "estado_estabilidad": estado,
    }


def probabilidad_atasco(flujo_entrada_t_h, salida_t_h, humedad_pct, velocidad_m_s):
    relacion_carga = flujo_entrada_t_h / max(salida_t_h, 0.01)
    humedad_riesgo = limitar((humedad_pct - 13) / 12)
    velocidad_riesgo = limitar((1.1 - velocidad_m_s) / 1.1)
    puntaje = (relacion_carga - 0.85) * 1.8 + humedad_riesgo * 1.4 + velocidad_riesgo
    prob = 1 / (1 + math.exp(-puntaje))
    return round(limitar(prob), 3)


def probabilidad_rotura_cangilones(horas_operacion, impurezas_g_kg, tension_kn):
    validar_positivo(horas_operacion, "Las horas de operacion")
    validar_positivo(tension_kn, "La tension de correa")

    fatiga = limitar(horas_operacion / 2500)
    impacto = limitar(impurezas_g_kg / 9)
    tension = limitar((tension_kn - 7) / 9)
    prob = 0.10 + fatiga * 0.34 + impacto * 0.32 + tension * 0.24
    return round(limitar(prob), 3)


def clasificar_riesgo(probabilidad):
    if probabilidad < 0.35:
        return "bajo", "#2e9d59"
    if probabilidad < 0.65:
        return "medio", "#c7891b"
    return "alto", "#b23b3b"


def resumen_calculo(
    flujo_entrada_t_h,
    humedad_pct,
    velocidad_m_s,
    capacidad_cangilon_l,
    cangilones_por_m,
    densidad_t_m3,
    tiempo_min,
    altura_m,
    masa_estructura_kg,
    masa_grano_kg,
    desplazamiento_carga_m,
    ancho_base_m,
    viento_n,
    altura_viento_m,
    horas_operacion,
    impurezas_g_kg,
    tension_kn,
):
    salida_t_h, eficiencia = calcular_salida_t_h(
        capacidad_cangilon_l,
        cangilones_por_m,
        velocidad_m_s,
        densidad_t_m3,
        humedad_pct,
    )
    acumulacion = calcular_acumulacion(flujo_entrada_t_h, salida_t_h, densidad_t_m3, tiempo_min)
    centro = calcular_centro_masa(altura_m, masa_estructura_kg, masa_grano_kg, desplazamiento_carga_m)
    inercia = calcular_momento_inercia(altura_m, masa_estructura_kg, masa_grano_kg, centro["x_cm_m"])
    estabilidad = evaluar_estabilidad(
        centro["masa_total_kg"],
        ancho_base_m,
        centro["x_cm_m"],
        viento_n,
        altura_viento_m,
    )
    p_atasco = probabilidad_atasco(flujo_entrada_t_h, salida_t_h, humedad_pct, velocidad_m_s)
    p_rotura = probabilidad_rotura_cangilones(horas_operacion, impurezas_g_kg, tension_kn)
    riesgo_general = round(max(p_atasco, p_rotura), 3)
    nivel, color = clasificar_riesgo(riesgo_general)

    return {
        "flujo_entrada_t_h": flujo_entrada_t_h,
        "salida_t_h": salida_t_h,
        "eficiencia": eficiencia,
        "humedad_pct": humedad_pct,
        "velocidad_m_s": velocidad_m_s,
        "volumen_acumulado_m3": acumulacion["volumen_acumulado_m3"],
        "exceso_t_h": acumulacion["exceso_t_h"],
        "masa_total_kg": centro["masa_total_kg"],
        "x_cm_m": centro["x_cm_m"],
        "y_cm_m": centro["y_cm_m"],
        "momento_inercia_kg_m2": inercia,
        "momento_estable_Nm": estabilidad["momento_estable_Nm"],
        "momento_volcador_Nm": estabilidad["momento_volcador_Nm"],
        "margen_Nm": estabilidad["margen_Nm"],
        "estado_estabilidad": estabilidad["estado_estabilidad"],
        "prob_atasco": p_atasco,
        "prob_rotura": p_rotura,
        "riesgo_general": riesgo_general,
        "nivel_riesgo": nivel,
        "color_riesgo": color,
    }
