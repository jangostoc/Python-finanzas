"""
generar_datos.py
-------------------------------------------------------------
Genera los datos FICTICIOS del proyecto 03: una distribuidora
de alimentación ("Distribuidora Atlántica, S.L.", empresa
inventada) con presupuesto y real de enero a septiembre de 2026.

Salida (formato "export de ERP", una fila por mes/escenario):
  - ventas.csv : mes, linea, escenario, cajas, importe_ventas, coste_ventas
  - gastos.csv : mes, departamento, concepto, escenario, importe

Los datos reales incluyen "historias" de negocio reconocibles
para que el análisis tenga algo que descubrir (ver README).
Ejecutar:  python generar_datos.py
-------------------------------------------------------------
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)          # semilla fija: siempre los mismos datos
MESES = pd.period_range("2026-01", "2026-09", freq="M")

# ============================================================
# 1. VENTAS: presupuesto por línea (cajas/mes, €/caja, coste €/caja)
# ============================================================
LINEAS = {
    #             cajas  precio  coste   estacionalidad (ene..sep)
    "Aceites":   (22000, 48.0, 33.0, [1.00, .95, 1.00, 1.00, 1.02, 1.00, .95, .90, 1.05]),
    "Conservas": (35000, 26.0, 16.5, [.95, .95, 1.00, 1.00, 1.00, 1.02, 1.00, .95, 1.05]),
    "Bebidas":   (28000, 19.0, 11.0, [.75, .80, .90, 1.00, 1.15, 1.35, 1.45, 1.40, 1.10]),
}

filas = []
for linea, (cajas, precio, coste, estac) in LINEAS.items():
    for i, mes in enumerate(MESES):
        m = mes.month
        u_ppto = round(cajas * estac[i])
        # --- Historias de negocio en el REAL ---
        f_vol, f_pre, f_cos = 1.0, 1.0, 1.0
        if linea == "Aceites":
            if m >= 2: f_cos *= 1.10          # sube la materia prima (+10 %)
            if m >= 3: f_pre *= 1.07          # se repercute parcialmente en precio
            if m >= 4: f_vol *= 0.95          # y los clientes compran algo menos
        if linea == "Conservas" and m >= 5:
            f_vol *= 1.09                      # nuevo cliente de gran distribución
            f_pre *= 0.98                      # ...a cambio de un descuento del 2 %
        if linea == "Bebidas" and m in (7, 8):
            f_vol *= 0.85                      # verano lluvioso: caen las bebidas
        u_real = round(u_ppto * f_vol * rng.normal(1, 0.025))
        p_real = precio * f_pre * rng.normal(1, 0.01)
        c_real = coste * f_cos * rng.normal(1, 0.01)

        filas += [
            dict(mes=str(mes), linea=linea, escenario="Presupuesto", cajas=u_ppto,
                 importe_ventas=round(u_ppto * precio, 2), coste_ventas=round(u_ppto * coste, 2)),
            dict(mes=str(mes), linea=linea, escenario="Real", cajas=u_real,
                 importe_ventas=round(u_real * p_real, 2), coste_ventas=round(u_real * c_real, 2)),
        ]
ventas = pd.DataFrame(filas)

# ============================================================
# 2. GASTOS DE ESTRUCTURA (opex) por departamento y concepto
# ============================================================
cajas_mes = ventas.groupby(["mes", "escenario"])["cajas"].sum()

GASTOS = {  # presupuesto mensual en €
    ("Comercial", "Personal"): 85000,
    ("Comercial", "Marketing"): 30000,
    ("Comercial", "Viajes y dietas"): 8000,
    ("Logística", "Personal"): 110000,
    ("Logística", "Transporte"): None,          # variable: 0,90 €/caja
    ("Logística", "Alquiler almacén"): 40000,
    ("Logística", "Energía"): 14000,
    ("Administración", "Personal"): 60000,
    ("Administración", "Servicios profesionales"): 12000,
    ("Administración", "Alquiler oficinas"): 9000,
    ("IT", "Personal"): 25000,
    ("IT", "Licencias y servicios"): 15000,
}
FIJOS = {"Alquiler almacén", "Alquiler oficinas"}   # no tienen ruido

filas = []
for (dep, concepto), base in GASTOS.items():
    for mes in MESES:
        m, k = mes.month, str(mes)
        if concepto == "Transporte":
            ppto = cajas_mes[(k, "Presupuesto")] * 0.90
            real = cajas_mes[(k, "Real")] * 0.90 * (1.055 if m >= 4 else 1.0)  # gasóleo +5,5 % desde abril
        else:
            ppto = base
            real = base if concepto in FIJOS else base * rng.normal(1, 0.02)
            if dep == "Comercial" and concepto == "Marketing" and m == 5:
                real += 45000                              # campaña de primavera no presupuestada
            if dep == "Comercial" and concepto == "Viajes y dietas":
                real *= 0.80                               # política de ahorro en viajes
            if concepto == "Energía" and m in (6, 7, 8):
                real *= 1.18                               # pico de precio eléctrico + frío en verano
            if dep == "IT" and concepto == "Licencias y servicios" and m == 3:
                real += 22000                              # renovación anual de licencias no prevista
            if dep == "Logística" and concepto == "Personal" and m in (7, 8):
                real *= 1.12                               # horas extra en verano
            if concepto == "Servicios profesionales" and m == 6:
                real *= 0.60                               # auditoría aplazada
        filas += [
            dict(mes=k, departamento=dep, concepto=concepto, escenario="Presupuesto", importe=round(ppto, 2)),
            dict(mes=k, departamento=dep, concepto=concepto, escenario="Real", importe=round(real, 2)),
        ]
gastos = pd.DataFrame(filas)

ventas.to_csv("ventas.csv", index=False)
gastos.to_csv("gastos.csv", index=False)
print(f"ventas.csv: {len(ventas)} filas  |  gastos.csv: {len(gastos)} filas")
