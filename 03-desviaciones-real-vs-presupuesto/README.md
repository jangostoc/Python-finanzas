# 03 · Análisis de desviaciones: Real vs Presupuesto

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jangostoc/finanzas-con-ia/blob/main/03-desviaciones-real-vs-presupuesto/desviaciones_real_vs_ppto.ipynb)

Cierre a septiembre de 2026 de **Distribuidora Atlántica, S.L.**, una distribuidora de alimentación con tres líneas de producto (aceites, conservas y bebidas) y cuatro departamentos. *Empresa y datos ficticios, generados para este ejercicio.*

![Puente de EBITDA](cascada_ebitda.png)

## Qué hace el análisis

| Paso | Técnica de control de gestión |
|---|---|
| 1 · Validación | Comprobación de nulos, duplicados, meses y escenarios antes de analizar |
| 2 · PyG acumulada | Real vs presupuesto hasta EBITDA, con desviación en € y %, y convención de signos homogénea (positivo = favorable) |
| 3 · Precio / volumen / mix | Descomposición de la desviación de ventas y de margen bruto por línea, con comprobación de que los efectos explican el 100 % |
| 4 · Gastos de estructura | Ranking de desviaciones, **alertas por materialidad** (≥ 10.000 € y ≥ 5 %) y mapa de calor mensual por departamento |
| 5 · Puente de EBITDA | Cascada del EBITDA presupuestado al real |
| 6 · Reporting | Evolución mensual y **Excel de 5 pestañas** con formato (desviaciones en verde y rojo) |
| 7 · Conclusiones | Lectura de negocio, separación entre causas controlables y no controlables, y acciones propuestas |

## Resultado principal

Las ventas superan el presupuesto en un **+2,0 %**, pero el **EBITDA queda un 5,6 % por debajo (−208 k€)**. La causa principal es la subida del coste de la materia prima en aceites, que solo se repercute parcialmente en precio. El detalle está en la sección 7 del notebook.

## Ficheros

| Fichero | Contenido |
|---|---|
| `desviaciones_real_vs_ppto.ipynb` | Notebook de análisis, ya ejecutado (se ve con todos los resultados en GitHub) |
| `ventas.csv` | Cajas, ventas y coste de ventas por mes, línea y escenario |
| `gastos.csv` | Gastos de estructura por mes, departamento, concepto y escenario |
| `generar_datos.py` | Script que genera los datos ficticios, con las "historias" de negocio documentadas |

## Cómo ejecutarlo

Pulsa **Abrir en Colab** y ejecuta las celdas en orden. Los datos se cargan solos desde este repositorio. Al final se genera `informe_desviaciones_sep2026.xlsx`, que puedes descargar desde el panel de archivos 📁.

Para usarlo con datos de tu empresa, basta con exportar del ERP dos ficheros con las mismas columnas que `ventas.csv` y `gastos.csv`.
