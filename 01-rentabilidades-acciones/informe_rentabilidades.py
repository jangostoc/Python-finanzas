"""
informe_rentabilidades.py
-------------------------------------------------------------
Descarga cotizaciones de Yahoo Finance, calcula rentabilidades
y GUARDA los resultados (gráfico PNG + informe Excel) en una
carpeta con la fecha de hoy. Todo se ejecuta de golpe.

Cómo ejecutarlo:
  - En Google Colab:  !python informe_rentabilidades.py
  - En tu ordenador:  python informe_rentabilidades.py
-------------------------------------------------------------
"""
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Sin ventanas: el gráfico se guarda, no se muestra
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

# ============================================================
# 1. PARÁMETROS  (lo único que normalmente tocarás)
# ============================================================
TICKERS = ["ITX.MC", "SAN.MC", "IBE.MC"]   # Inditex, Santander, Iberdrola
INICIO = "2025-01-01"
FIN = date.today().isoformat()
CARPETA = Path(f"informe_{date.today():%Y-%m-%d}")
CARPETA.mkdir(exist_ok=True)

# ============================================================
# 2. DESCARGA DE DATOS
# ============================================================
print("1/4 Descargando cotizaciones...")
precios = yf.download(TICKERS, start=INICIO, end=FIN,
                      auto_adjust=True, progress=False)["Close"].dropna()

if precios.empty:
    raise SystemExit("ERROR: no se han descargado datos. Revisa tickers, fechas o conexión.")

if precios.index.tz is not None:          # Excel no admite fechas con zona horaria
    precios.index = precios.index.tz_localize(None)

# ============================================================
# 3. CÁLCULO DE RENTABILIDADES
# ============================================================
print("2/4 Calculando rentabilidades...")
rent_diaria = precios.pct_change().dropna()

resumen = pd.DataFrame({
    "Precio inicial": precios.iloc[0],
    "Precio final": precios.iloc[-1],
    "Rentabilidad acumulada %": (precios.iloc[-1] / precios.iloc[0] - 1) * 100,
    "Volatilidad anualizada %": rent_diaria.std() * (252 ** 0.5) * 100,
}).round(2).sort_values("Rentabilidad acumulada %", ascending=False)

# ============================================================
# 4. GRÁFICO  (se guarda como imagen)
# ============================================================
print("3/4 Generando gráfico...")
base100 = precios / precios.iloc[0] * 100
ax = base100.plot(figsize=(10, 5), title=f"Evolución base 100 desde {INICIO}")
ax.axhline(100, color="grey", linestyle="--", linewidth=0.8)
ax.set_xlabel("")
ax.set_ylabel("Base 100")
ruta_grafico = CARPETA / "evolucion_base100.png"
plt.savefig(ruta_grafico, dpi=150, bbox_inches="tight")
plt.close()

# ============================================================
# 5. INFORME EXCEL  (3 pestañas)
# ============================================================
print("4/4 Guardando Excel...")
ruta_excel = CARPETA / "informe_rentabilidades.xlsx"
with pd.ExcelWriter(ruta_excel) as writer:
    resumen.to_excel(writer, sheet_name="Resumen")
    precios.round(2).to_excel(writer, sheet_name="Precios")
    (rent_diaria * 100).round(3).to_excel(writer, sheet_name="Rent diaria %")

print("\nHecho. Resultados guardados en:")
print(f"  - {ruta_grafico}")
print(f"  - {ruta_excel}")
print("\nResumen:")
print(resumen.to_string())
