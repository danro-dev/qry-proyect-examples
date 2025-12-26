# Ejemplos Avanzados

Esta guía presenta ejemplos completos que combinan múltiples características de qry-doc.

## Ejemplo 1: Análisis de Aerolíneas con MySQL

Este ejemplo conecta a una base de datos MySQL real, ejecuta consultas, genera gráficas y crea un reporte PDF completo.

### Requisitos

```bash
# Instalar driver MySQL
uv pip install pymysql
```

### Código Completo

```python
"""
Análisis de Puntualidad de Aerolíneas
=====================================
Conecta a MySQL, analiza datos y genera reporte PDF con múltiples gráficas.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd

load_dotenv()

from qry_doc import QryDoc, ReportTemplate
from qry_doc.data_source import DataSourceLoader
from qry_doc.report_template import LogoPosition
from qry_doc.report_generator import ReportGenerator
from reportlab.platypus import Paragraph, Spacer, Image, PageBreak

import pandasai as pai
from pandasai_openai import OpenAI

# Configurar LLM
llm = OpenAI()
pai.config.set({"llm": llm})

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

MYSQL_URL = "mysql+pymysql://guest:ctu-relational@relational.fel.cvut.cz:3306/Airline"
OUTPUT_DIR = Path("output/reporte_aerolineas")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# 1. CARGAR DATOS
# =============================================================================

print("🔗 Cargando datos de MySQL...")

query = """
SELECT 
    UniqueCarrier as Aerolinea,
    Origin as Origen,
    Dest as Destino,
    FlightDate as Fecha,
    DayOfWeek as DiaSemana,
    DepDelay as RetrasoSalida,
    ArrDelay as RetrasoLlegada,
    Distance as Distancia,
    Cancelled as Cancelado
FROM On_Time_On_Time_Performance_2016_1
WHERE DepDelay IS NOT NULL AND ArrDelay IS NOT NULL
ORDER BY RAND()
LIMIT 30000
"""

df = DataSourceLoader.load_sql_query(MYSQL_URL, query)
print(f"✅ Cargados {len(df):,} vuelos")

# =============================================================================
# 2. GENERAR GRÁFICAS
# =============================================================================

print("📈 Generando gráficas...")

plt.style.use('seaborn-v0_8-whitegrid')

# Gráfica 1: Vuelos por Aerolínea
fig, ax = plt.subplots(figsize=(12, 6))
vuelos = df['Aerolinea'].value_counts().head(12)
ax.bar(vuelos.index, vuelos.values, color=plt.cm.Blues(range(50, 250, 17)))
ax.set_title('Top 12 Aerolíneas por Número de Vuelos', fontsize=14, fontweight='bold')
ax.set_xlabel('Aerolínea')
ax.set_ylabel('Número de Vuelos')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_01.png', dpi=150, bbox_inches='tight')
plt.close()

# Gráfica 2: Retraso Promedio por Aerolínea
fig, ax = plt.subplots(figsize=(12, 6))
retraso = df.groupby('Aerolinea')['RetrasoLlegada'].mean().sort_values()
colors = ['#2ecc71' if x < 0 else '#e74c3c' for x in retraso.values]
ax.barh(retraso.index, retraso.values, color=colors)
ax.axvline(x=0, color='black', linewidth=0.8)
ax.set_title('Retraso Promedio de Llegada por Aerolínea', fontsize=14, fontweight='bold')
ax.set_xlabel('Retraso Promedio (minutos)')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_02.png', dpi=150, bbox_inches='tight')
plt.close()

# Gráfica 3: Distribución de Retrasos
fig, ax = plt.subplots(figsize=(10, 6))
retrasos = df[(df['RetrasoLlegada'] >= -30) & (df['RetrasoLlegada'] <= 60)]['RetrasoLlegada']
ax.hist(retrasos, bins=50, color='#3498db', edgecolor='white', alpha=0.8)
ax.axvline(x=0, color='#e74c3c', linewidth=2, linestyle='--', label='A tiempo')
ax.axvline(x=retrasos.mean(), color='#f39c12', linewidth=2, label=f'Promedio: {retrasos.mean():.1f} min')
ax.set_title('Distribución de Retrasos de Llegada', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_03.png', dpi=150, bbox_inches='tight')
plt.close()

# Gráfica 4: Estado de Vuelos (Pie)
fig, ax = plt.subplots(figsize=(8, 8))
estados = {
    'A tiempo (≤15 min)': len(df[df['RetrasoLlegada'] <= 15]),
    'Retrasado (>15 min)': len(df[df['RetrasoLlegada'] > 15]),
    'Cancelado': df['Cancelado'].sum(),
}
colors = ['#2ecc71', '#e74c3c', '#95a5a6']
ax.pie(estados.values(), labels=estados.keys(), autopct='%1.1f%%', colors=colors)
ax.set_title('Estado de los Vuelos', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_04.png', dpi=150, bbox_inches='tight')
plt.close()

print("✅ Gráficas generadas")

# =============================================================================
# 3. CALCULAR ESTADÍSTICAS
# =============================================================================

stats = {
    'total_vuelos': len(df),
    'aerolineas': df['Aerolinea'].nunique(),
    'puntualidad': len(df[df['RetrasoLlegada'] <= 15]) / len(df) * 100,
    'retraso_promedio': df['RetrasoLlegada'].mean(),
}

# Resumen por aerolínea
resumen = df.groupby('Aerolinea').agg({
    'Fecha': 'count',
    'RetrasoLlegada': 'mean',
    'Distancia': 'mean'
}).round(2)
resumen.columns = ['Vuelos', 'Retraso Prom.', 'Distancia Prom.']
resumen = resumen.sort_values('Vuelos', ascending=False).head(10).reset_index()

# =============================================================================
# 4. GENERAR REPORTE PDF
# =============================================================================

print("📄 Generando reporte PDF...")

# Template sin portada, con logo en footer
template = ReportTemplate(
    primary_color="#1a365d",
    footer_logo_enabled=True,
    footer_logo_path=Path("public/logo.png") if Path("public/logo.png").exists() else None,
)

generator = ReportGenerator(OUTPUT_DIR / "reporte_aerolineas.pdf", template=template)

story = generator.story
styles = generator.styles

# Página 1: Título y Resumen
story.append(Paragraph("Análisis de Puntualidad de Aerolíneas", styles['Title']))
story.append(Spacer(1, 20))

story.append(Paragraph("Resumen Ejecutivo", styles['Heading']))
story.append(Paragraph(
    f"Análisis de {stats['total_vuelos']:,} vuelos de {stats['aerolineas']} aerolíneas.",
    styles['Body']
))

metricas = f"""
• Total de vuelos: {stats['total_vuelos']:,}<br/>
• Aerolíneas: {stats['aerolineas']}<br/>
• Tasa de puntualidad: {stats['puntualidad']:.1f}%<br/>
• Retraso promedio: {stats['retraso_promedio']:.1f} minutos
"""
story.append(Paragraph(metricas, styles['Body']))

story.append(Paragraph("Top 10 Aerolíneas", styles['Heading']))
generator._add_table(resumen)

# Página 2: Gráficas
story.append(PageBreak())

def add_chart(path, title):
    story.append(Paragraph(title, styles['Heading']))
    img = Image(str(path))
    scale = min(template.content_width / img.imageWidth, 280 / img.imageHeight, 1.0)
    img.drawWidth = img.imageWidth * scale
    img.drawHeight = img.imageHeight * scale
    story.append(img)
    story.append(Spacer(1, 15))

add_chart(OUTPUT_DIR / 'grafica_01.png', "Vuelos por Aerolínea")
add_chart(OUTPUT_DIR / 'grafica_02.png', "Retraso Promedio")

story.append(PageBreak())
add_chart(OUTPUT_DIR / 'grafica_03.png', "Distribución de Retrasos")
add_chart(OUTPUT_DIR / 'grafica_04.png', "Estado de Vuelos")

# Construir documento
generator._build_document()

print(f"✅ Reporte generado: {OUTPUT_DIR / 'reporte_aerolineas.pdf'}")
```

### Resultado

El script genera:

- 4 gráficas PNG
- 1 reporte PDF de 3 páginas con:
    - Resumen ejecutivo y tabla
    - Gráficas de barras
    - Histograma y pie chart

---

## Ejemplo 2: Consultas en Lenguaje Natural

Usa QryDoc para hacer preguntas sobre los datos:

```python
from qry_doc import QryDoc
from qry_doc.data_source import DataSourceLoader

# Cargar datos
df = DataSourceLoader.load_sql_query(MYSQL_URL, "SELECT * FROM vuelos LIMIT 20000")

# Crear QryDoc
qry = QryDoc(df, llm=llm)

# Hacer preguntas en español
respuesta = qry.ask("¿Cuáles son las 5 aerolíneas con más vuelos?")
print(respuesta)

respuesta = qry.ask("¿Cuál es el retraso promedio por día de la semana?")
print(respuesta)

respuesta = qry.ask("¿Qué porcentaje de vuelos llegan a tiempo?")
print(respuesta)
```

---

## Ejemplo 3: Exportar Datos Filtrados

```python
from qry_doc import QryDoc
from qry_doc.data_source import DataSourceLoader

# Cargar y filtrar datos
df = DataSourceLoader.load_sql_query(MYSQL_URL, query)

# Filtrar vuelos retrasados
retrasados = df[df['RetrasoLlegada'] > 30]

# Exportar a CSV
qry = QryDoc(retrasados, llm=llm)
qry.export_csv("output/vuelos_retrasados.csv")

print(f"Exportados {len(retrasados):,} vuelos retrasados")
```

---

## Ejemplo 4: Reporte con Portada

```python
from qry_doc import ReportTemplate
from qry_doc.report_generator import ReportGenerator

# Template CON portada
template = ReportTemplate(
    primary_color="#1a365d",
    cover_image_path=Path("public/portada.png"),  # Imagen de portada
    footer_logo_enabled=True,
    footer_logo_path=Path("public/logo.png"),
)

generator = ReportGenerator("reporte_con_portada.pdf", template=template)
generator.build(
    title="Mi Reporte",
    summary="Resumen ejecutivo...",
    chart_path=Path("grafica.png"),
    dataframe=df
)
```

---

## Base de Datos de Ejemplo

Los ejemplos usan la base de datos CTU Relational:

| Campo | Valor |
|-------|-------|
| Host | `relational.fel.cvut.cz` |
| Puerto | `3306` |
| Usuario | `guest` |
| Contraseña | `ctu-relational` |
| Base de datos | `Airline` |

**Tabla principal:** `On_Time_On_Time_Performance_2016_1`

- 445,827 vuelos de enero 2016
- Datos de puntualidad de aerolíneas estadounidenses

### Columnas Útiles

| Columna | Descripción |
|---------|-------------|
| `UniqueCarrier` | Código de aerolínea |
| `Origin` / `Dest` | Aeropuertos origen/destino |
| `FlightDate` | Fecha del vuelo |
| `DepDelay` | Retraso de salida (minutos) |
| `ArrDelay` | Retraso de llegada (minutos) |
| `Distance` | Distancia (millas) |
| `Cancelled` | Si fue cancelado (0/1) |

---

## Ver También

- [Bases de Datos](databases.md) - Conexión a diferentes bases de datos
- [Múltiples Gráficas](multiple-charts.md) - Detalles sobre agregar gráficas
- [Portadas](cover-pages.md) - Configurar portadas
