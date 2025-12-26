"""
Ejemplo 07: Reporte Completo de Aerolíneas con Gráficas
=======================================================

Este ejemplo genera un reporte PDF profesional con múltiples gráficas
y análisis detallado de datos de aerolíneas.

Características:
- Sin portada (directo al contenido)
- Logo en pie de página
- Múltiples gráficas (barras, pie, líneas)
- Análisis estadístico completo
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

import pandasai as pai
from pandasai_openai import OpenAI

llm = OpenAI()
pai.config.set({"llm": llm})

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

MYSQL_URL = "mysql+pymysql://guest:ctu-relational@relational.fel.cvut.cz:3306/Airline"
OUTPUT_DIR = Path("output/reporte_completo")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Logo personalizado (si existe)
LOGO_PATH = Path("public/logo_op.png")

print("=" * 70)
print("📊 REPORTE COMPLETO DE AEROLÍNEAS")
print("=" * 70)

# =============================================================================
# 1. CARGAR DATOS
# =============================================================================

print("\n🔗 Cargando datos de MySQL...")

query = """
SELECT 
    UniqueCarrier as Aerolinea,
    Origin as Origen,
    OriginCityName as CiudadOrigen,
    Dest as Destino,
    DestCityName as CiudadDestino,
    FlightDate as Fecha,
    DayOfWeek as DiaSemana,
    DepDelay as RetrasoSalida,
    ArrDelay as RetrasoLlegada,
    Distance as Distancia,
    Cancelled as Cancelado,
    Diverted as Desviado,
    AirTime as TiempoVuelo
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

print("\n📈 Generando gráficas...")

# Configurar estilo de matplotlib
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10

# --- Gráfica 1: Vuelos por Aerolínea ---
print("   📊 Gráfica 1: Vuelos por aerolínea...")
fig, ax = plt.subplots(figsize=(12, 6))
vuelos_aerolinea = df['Aerolinea'].value_counts().head(12)
colors = plt.cm.Blues(range(50, 250, 17))
bars = ax.bar(vuelos_aerolinea.index, vuelos_aerolinea.values, color=colors)
ax.set_xlabel('Aerolínea', fontsize=12)
ax.set_ylabel('Número de Vuelos', fontsize=12)
ax.set_title('Top 12 Aerolíneas por Número de Vuelos', fontsize=14, fontweight='bold')
ax.tick_params(axis='x', rotation=45)
for bar, val in zip(bars, vuelos_aerolinea.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
            f'{val:,}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_01_vuelos_aerolinea.png', dpi=150, bbox_inches='tight')
plt.close()

# --- Gráfica 2: Retraso Promedio por Aerolínea ---
print("   📊 Gráfica 2: Retraso promedio por aerolínea...")
fig, ax = plt.subplots(figsize=(12, 6))
retraso_aerolinea = df.groupby('Aerolinea')['RetrasoLlegada'].mean().sort_values(ascending=True)
colors = ['#2ecc71' if x < 0 else '#e74c3c' for x in retraso_aerolinea.values]
bars = ax.barh(retraso_aerolinea.index, retraso_aerolinea.values, color=colors)
ax.axvline(x=0, color='black', linewidth=0.8)
ax.set_xlabel('Retraso Promedio (minutos)', fontsize=12)
ax.set_ylabel('Aerolínea', fontsize=12)
ax.set_title('Retraso Promedio de Llegada por Aerolínea', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_02_retraso_aerolinea.png', dpi=150, bbox_inches='tight')
plt.close()

# --- Gráfica 3: Distribución de Retrasos ---
print("   📊 Gráfica 3: Distribución de retrasos...")
fig, ax = plt.subplots(figsize=(10, 6))
retrasos_filtrados = df[(df['RetrasoLlegada'] >= -30) & (df['RetrasoLlegada'] <= 60)]['RetrasoLlegada']
ax.hist(retrasos_filtrados, bins=50, color='#3498db', edgecolor='white', alpha=0.8)
ax.axvline(x=0, color='#e74c3c', linewidth=2, linestyle='--', label='A tiempo')
ax.axvline(x=retrasos_filtrados.mean(), color='#f39c12', linewidth=2, label=f'Promedio: {retrasos_filtrados.mean():.1f} min')
ax.set_xlabel('Retraso de Llegada (minutos)', fontsize=12)
ax.set_ylabel('Frecuencia', fontsize=12)
ax.set_title('Distribución de Retrasos de Llegada', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_03_distribucion_retrasos.png', dpi=150, bbox_inches='tight')
plt.close()

# --- Gráfica 4: Retrasos por Día de la Semana ---
print("   📊 Gráfica 4: Retrasos por día de la semana...")
dias = {1: 'Lunes', 2: 'Martes', 3: 'Miércoles', 4: 'Jueves', 5: 'Viernes', 6: 'Sábado', 7: 'Domingo'}
df['NombreDia'] = df['DiaSemana'].map(dias)
retraso_dia = df.groupby('DiaSemana').agg({
    'RetrasoSalida': 'mean',
    'RetrasoLlegada': 'mean'
}).round(2)
retraso_dia.index = [dias[i] for i in retraso_dia.index]

fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(retraso_dia))
width = 0.35
bars1 = ax.bar([i - width/2 for i in x], retraso_dia['RetrasoSalida'], width, label='Retraso Salida', color='#e74c3c')
bars2 = ax.bar([i + width/2 for i in x], retraso_dia['RetrasoLlegada'], width, label='Retraso Llegada', color='#3498db')
ax.set_xlabel('Día de la Semana', fontsize=12)
ax.set_ylabel('Retraso Promedio (minutos)', fontsize=12)
ax.set_title('Retraso Promedio por Día de la Semana', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(retraso_dia.index, rotation=45)
ax.legend()
ax.axhline(y=0, color='black', linewidth=0.5)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_04_retraso_dia.png', dpi=150, bbox_inches='tight')
plt.close()

# --- Gráfica 5: Top 10 Rutas más Frecuentes ---
print("   📊 Gráfica 5: Top 10 rutas...")
df['Ruta'] = df['Origen'] + ' → ' + df['Destino']
rutas = df['Ruta'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.Oranges(range(50, 250, 20))
bars = ax.barh(rutas.index[::-1], rutas.values[::-1], color=colors)
ax.set_xlabel('Número de Vuelos', fontsize=12)
ax.set_ylabel('Ruta', fontsize=12)
ax.set_title('Top 10 Rutas más Frecuentes', fontsize=14, fontweight='bold')
for bar, val in zip(bars, rutas.values[::-1]):
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, 
            f'{val:,}', ha='left', va='center', fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_05_rutas.png', dpi=150, bbox_inches='tight')
plt.close()

# --- Gráfica 6: Distribución de Distancias ---
print("   📊 Gráfica 6: Distribución de distancias...")
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df['Distancia'], bins=40, color='#9b59b6', edgecolor='white', alpha=0.8)
ax.axvline(x=df['Distancia'].mean(), color='#e74c3c', linewidth=2, 
           label=f'Promedio: {df["Distancia"].mean():.0f} millas')
ax.axvline(x=df['Distancia'].median(), color='#f39c12', linewidth=2, linestyle='--',
           label=f'Mediana: {df["Distancia"].median():.0f} millas')
ax.set_xlabel('Distancia (millas)', fontsize=12)
ax.set_ylabel('Frecuencia', fontsize=12)
ax.set_title('Distribución de Distancias de Vuelo', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_06_distancias.png', dpi=150, bbox_inches='tight')
plt.close()

# --- Gráfica 7: Pie de Estado de Vuelos ---
print("   📊 Gráfica 7: Estado de vuelos...")
fig, ax = plt.subplots(figsize=(8, 8))
estados = {
    'A tiempo (≤15 min)': len(df[df['RetrasoLlegada'] <= 15]),
    'Retrasado (>15 min)': len(df[df['RetrasoLlegada'] > 15]),
    'Cancelado': df['Cancelado'].sum(),
    'Desviado': df['Desviado'].sum()
}
colors = ['#2ecc71', '#e74c3c', '#95a5a6', '#f39c12']
explode = (0.02, 0.02, 0.05, 0.05)
wedges, texts, autotexts = ax.pie(estados.values(), labels=estados.keys(), autopct='%1.1f%%',
                                   colors=colors, explode=explode, startangle=90)
ax.set_title('Estado de los Vuelos', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_07_estado_vuelos.png', dpi=150, bbox_inches='tight')
plt.close()

print("✅ Todas las gráficas generadas")

# =============================================================================
# 3. CALCULAR ESTADÍSTICAS
# =============================================================================

print("\n📊 Calculando estadísticas...")

stats = {
    'total_vuelos': len(df),
    'aerolineas': df['Aerolinea'].nunique(),
    'aeropuertos_origen': df['Origen'].nunique(),
    'aeropuertos_destino': df['Destino'].nunique(),
    'retraso_salida_promedio': df['RetrasoSalida'].mean(),
    'retraso_llegada_promedio': df['RetrasoLlegada'].mean(),
    'distancia_promedio': df['Distancia'].mean(),
    'distancia_total': df['Distancia'].sum(),
    'vuelos_a_tiempo': len(df[df['RetrasoLlegada'] <= 15]),
    'vuelos_retrasados': len(df[df['RetrasoLlegada'] > 15]),
    'cancelados': df['Cancelado'].sum(),
    'desviados': df['Desviado'].sum(),
    'puntualidad': len(df[df['RetrasoLlegada'] <= 15]) / len(df) * 100,
}

# =============================================================================
# 4. GENERAR REPORTE PDF
# =============================================================================

print("\n📄 Generando reporte PDF...")

# Template SIN portada, CON logo en footer
template = ReportTemplate(
    primary_color="#1a365d",
    # Sin cover_image_path = sin portada
    footer_logo_enabled=True,
    footer_logo_path=LOGO_PATH if LOGO_PATH.exists() else None,
    footer_logo_position=LogoPosition.BOTTOM_RIGHT,
    footer_logo_width=100.0,
    footer_logo_height=50.0,
)

# Crear resumen para el reporte
resumen_aerolineas = df.groupby('Aerolinea').agg({
    'Fecha': 'count',
    'RetrasoSalida': 'mean',
    'RetrasoLlegada': 'mean',
    'Distancia': 'mean'
}).round(2)
resumen_aerolineas.columns = ['Vuelos', 'Retraso Salida', 'Retraso Llegada', 'Distancia Prom.']
resumen_aerolineas = resumen_aerolineas.sort_values('Vuelos', ascending=False).head(12).reset_index()

# Generar reporte con TODAS las gráficas
from reportlab.platypus import Paragraph, Spacer, Image, PageBreak

generator = ReportGenerator(OUTPUT_DIR / "reporte_aerolineas_completo.pdf", template=template)

# Construir el contenido manualmente para incluir todas las gráficas
story = generator.story
styles = generator.styles

# Título
story.append(Paragraph("Análisis de Puntualidad de Aerolíneas", styles['Title']))
story.append(Spacer(1, 20))

# Resumen ejecutivo
story.append(Paragraph("Resumen Ejecutivo", styles['Heading']))
summary_text = f"""
Este informe presenta un análisis detallado de {stats['total_vuelos']:,} vuelos operados por 
{stats['aerolineas']} aerolíneas estadounidenses durante enero de 2016.
"""
story.append(Paragraph(summary_text.strip(), styles['Body']))
story.append(Spacer(1, 10))

# Métricas principales
story.append(Paragraph("Métricas Principales", styles['Heading']))
metricas = f"""
• Total de vuelos analizados: {stats['total_vuelos']:,}<br/>
• Aerolíneas incluidas: {stats['aerolineas']}<br/>
• Aeropuertos de origen: {stats['aeropuertos_origen']}<br/>
• Aeropuertos de destino: {stats['aeropuertos_destino']}<br/>
• Tasa de puntualidad (≤15 min): {stats['puntualidad']:.1f}%<br/>
• Retraso promedio de llegada: {stats['retraso_llegada_promedio']:.1f} minutos
"""
story.append(Paragraph(metricas.strip(), styles['Body']))
story.append(Spacer(1, 15))

# Tabla de resumen
story.append(Paragraph("Resumen por Aerolínea", styles['Heading']))
generator._add_table(resumen_aerolineas)

# Nueva página para gráficas
story.append(PageBreak())

# Función helper para agregar gráficas
def add_chart(path, title):
    story.append(Paragraph(title, styles['Heading']))
    try:
        img = Image(str(path))
        max_width = template.content_width
        max_height = 280
        scale = min(max_width / img.imageWidth, max_height / img.imageHeight, 1.0)
        img.drawWidth = img.imageWidth * scale
        img.drawHeight = img.imageHeight * scale
        story.append(img)
        story.append(Spacer(1, 15))
    except Exception as e:
        print(f"   ⚠️ Error cargando {path}: {e}")

# Gráfica 1: Vuelos por aerolínea
add_chart(OUTPUT_DIR / 'grafica_01_vuelos_aerolinea.png', "1. Vuelos por Aerolínea")

# Gráfica 2: Retraso promedio
add_chart(OUTPUT_DIR / 'grafica_02_retraso_aerolinea.png', "2. Retraso Promedio por Aerolínea")

story.append(PageBreak())

# Gráfica 3: Distribución de retrasos
add_chart(OUTPUT_DIR / 'grafica_03_distribucion_retrasos.png', "3. Distribución de Retrasos")

# Gráfica 4: Retrasos por día
add_chart(OUTPUT_DIR / 'grafica_04_retraso_dia.png', "4. Retrasos por Día de la Semana")

story.append(PageBreak())

# Gráfica 5: Top rutas
add_chart(OUTPUT_DIR / 'grafica_05_rutas.png', "5. Top 10 Rutas más Frecuentes")

# Gráfica 6: Distribución de distancias
add_chart(OUTPUT_DIR / 'grafica_06_distancias.png', "6. Distribución de Distancias")

story.append(PageBreak())

# Gráfica 7: Estado de vuelos
add_chart(OUTPUT_DIR / 'grafica_07_estado_vuelos.png', "7. Estado de los Vuelos")

# Conclusiones
story.append(Paragraph("Conclusiones", styles['Heading']))
conclusiones = f"""
La industria aérea estadounidense mantiene una tasa de puntualidad del {stats['puntualidad']:.1f}%, 
con un retraso promedio de llegada de {stats['retraso_llegada_promedio']:.1f} minutos. 
Las aerolíneas con mayor volumen de operaciones tienden a mantener mejores índices de puntualidad 
debido a sus sistemas de gestión más robustos.
"""
story.append(Paragraph(conclusiones.strip(), styles['Body']))

# Construir el documento
generator._build_document()

print(f"✅ Reporte generado: {OUTPUT_DIR / 'reporte_aerolineas_completo.pdf'}")

# =============================================================================
# 5. RESUMEN FINAL
# =============================================================================

print("\n" + "=" * 70)
print("✅ PROCESO COMPLETADO")
print("=" * 70)

print(f"""
📁 Archivos generados en: {OUTPUT_DIR}

📊 Gráficas:
   - grafica_01_vuelos_aerolinea.png
   - grafica_02_retraso_aerolinea.png
   - grafica_03_distribucion_retrasos.png
   - grafica_04_retraso_dia.png
   - grafica_05_rutas.png
   - grafica_06_distancias.png
   - grafica_07_estado_vuelos.png

📄 Reporte PDF:
   - reporte_aerolineas_completo.pdf

📈 Estadísticas clave:
   - {stats['total_vuelos']:,} vuelos analizados
   - {stats['puntualidad']:.1f}% de puntualidad
   - {stats['retraso_llegada_promedio']:.1f} min retraso promedio
""")

print("=" * 70)
