# 01 · Rentabilidad y volatilidad de acciones

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jangostoc/finanzas-con-ia/blob/main/01-rentabilidades-acciones/rentabilidades_notebook.ipynb)

Análisis de **Inditex, Santander e Iberdrola** desde enero de 2025: rentabilidad acumulada, volatilidad anualizada y evolución en base 100.

El mismo proceso está resuelto de dos formas, para ilustrar cuándo conviene cada una:

| Fichero | Formato | Uso |
|---|---|---|
| `rentabilidades_notebook.ipynb` | Jupyter Notebook (3 celdas) | **Exploración:** se ejecuta paso a paso y se revisa cada resultado (descarga → cálculo → gráfico). |
| `informe_rentabilidades.py` | Script de Python | **Automatización:** se ejecuta de una vez y guarda un Excel (3 pestañas) y un gráfico PNG en una carpeta con la fecha del día. |

## Cómo ejecutarlo

- **Notebook:** ábrelo en Google Colab y ejecuta las celdas con `Shift + Enter`.
- **Script:** súbelo a Colab y ejecuta en una celda `!python informe_rentabilidades.py`.

Para analizar otras acciones, basta con cambiar la lista `TICKERS`.

## Métricas

- **Rentabilidad acumulada** = precio final / precio inicial − 1
- **Volatilidad anualizada** = desviación típica de la rentabilidad diaria × √252
- **Base 100** = precio / precio inicial × 100 (permite comparar valores con precios distintos)
