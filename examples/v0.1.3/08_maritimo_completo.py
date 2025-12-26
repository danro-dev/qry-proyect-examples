"""
Ejemplo 08: Análisis Completo de Datos Marítimos
================================================

Este ejemplo demuestra el flujo completo de qry-doc:
1. Cargar datos desde CSV
2. Consultas en lenguaje natural
3. Análisis estadístico
4. Generación de múltiples gráficas
5. Exportación a CSV
6. Generación de reporte PDF con múltiples páginas

Dataset: Registros históricos de navegación marítima (1851-1852)
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

load_dotenv()

from qry_doc import QryDoc, ReportTemplate
from qry_doc.data_source import DataSourceLoader
from qry_doc.report_template import LogoPosition
from qry_doc.report_generator import ReportGenerator
from reportlab.platypus import Paragraph, Spacer, Image, PageBreak

import pandasai as pai
from pandasai_openai import OpenAI

llm = OpenAI()
pai.config.set({"llm": llm})

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

CSV_PATH = Path("examples/data/maritimal_data/DataLimpia.csv")
OUTPUT_DIR = Path("output/maritimo")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LOGO_PATH = Path("public/logo_op.png")

print("=" * 70)
print("🚢 ANÁLISIS COMPLETO DE DATOS MARÍTIMOS")
print("=" * 70)

# =============================================================================
# 1. CARGAR DATOS
# =============================================================================

print("\n📂 Cargando datos desde CSV...")

df = DataSourceLoader.load(CSV_PATH)
print(f"✅ Cargados {len(df):,} registros de navegación")

# Mostrar columnas disponibles
print(f"\n📋 Columnas disponibles:")
for col in df.columns:
    print(f"   - {col}")

# Limpiar y preparar datos
print("\n🔧 Preparando datos...")

# Convertir fechas
df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
df['travel_departure_date'] = pd.to_datetime(df['travel_departure_date'], errors='coerce')
df['travel_arrival_date'] = pd.to_datetime(df['travel_arrival_date'], errors='coerce')

# Extraer año y mes
df['year'] = df['publication_date'].dt.year
df['month'] = df['publication_date'].dt.month
df['month_name'] = df['publication_date'].dt.month_name()

# Limpiar duración del viaje (extraer número de días)
def extract_days(duration):
    if pd.isna(duration):
        return np.nan
    try:
        # Extraer números de strings como "4dias", "18dias"
        import re
        match = re.search(r'(\d+)', str(duration))
        if match:
            return int(match.group(1))
    except:
        pass
    return np.nan

df['travel_days'] = df['travel_duration'].apply(extract_days)

print(f"✅ Datos preparados")

# =============================================================================
# 2. CONSULTAS EN LENGUAJE NATURAL
# =============================================================================

print("\n🤖 Realizando consultas en lenguaje natural...")

qry = QryDoc(df, llm=llm)

# Consulta 1: Puertos más frecuentes
print("\n   📍 Consultando puertos de salida más frecuentes...")
try:
    respuesta1 = qry.ask("¿Cuáles son los 5 puertos de salida (travel_departure_port) más frecuentes?")
    print(f"   Respuesta: {respuesta1}")
except Exception as e:
    print(f"   ⚠️ Error en consulta: {e}")

# Consulta 2: Tipos de barcos
print("\n   🚢 Consultando tipos de barcos...")
try:
    respuesta2 = qry.ask("¿Cuántos tipos diferentes de barcos (ship_type) hay y cuáles son los más comunes?")
    print(f"   Respuesta: {respuesta2}")
except Exception as e:
    print(f"   ⚠️ Error en consulta: {e}")

# Consulta 3: Duración promedio
print("\n   ⏱️ Consultando duración promedio de viajes...")
try:
    respuesta3 = qry.ask("¿Cuál es la duración promedio de los viajes en días?")
    print(f"   Respuesta: {respuesta3}")
except Exception as e:
    print(f"   ⚠️ Error en consulta: {e}")

# =============================================================================
# 3. ANÁLISIS ESTADÍSTICO
# =============================================================================

print("\n📊 Calculando estadísticas...")

stats = {
    'total_registros': len(df),
    'puertos_salida': df['travel_departure_port'].nunique(),
    'puertos_llegada': df['travel_arrival_port'].nunique(),
    'tipos_barcos': df['ship_type'].nunique(),
    'barcos_unicos': df['ship_name'].nunique(),
    'duracion_promedio': df['travel_days'].mean(),
    'duracion_max': df['travel_days'].max(),
    'duracion_min': df['travel_days'].min(),
    'fecha_min': df['publication_date'].min(),
    'fecha_max': df['publication_date'].max(),
}

print(f"""
   📈 Estadísticas generales:
   - Total de registros: {stats['total_registros']:,}
   - Puertos de salida únicos: {stats['puertos_salida']}
   - Puertos de llegada únicos: {stats['puertos_llegada']}
   - Tipos de barcos: {stats['tipos_barcos']}
   - Barcos únicos: {stats['barcos_unicos']}
   - Duración promedio: {stats['duracion_promedio']:.1f} días
   - Período: {stats['fecha_min']} a {stats['fecha_max']}
""")

# =============================================================================
# 4. GENERAR GRÁFICAS
# =============================================================================

print("📈 Generando gráficas...")

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10

# --- Gráfica 1: Top 10 Puertos de Salida ---
print("   📊 Gráfica 1: Puertos de salida...")
fig, ax = plt.subplots(figsize=(12, 6))
puertos_salida = df['travel_departure_port'].value_counts().head(10)
colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(puertos_salida)))
bars = ax.barh(puertos_salida.index[::-1], puertos_salida.values[::-1], color=colors)
ax.set_xlabel('Número de Viajes', fontsize=12)
ax.set_ylabel('Puerto de Salida', fontsize=12)
ax.set_title('Top 10 Puertos de Salida más Frecuentes', fontsize=14, fontweight='bold')
for bar, val in zip(bars, puertos_salida.values[::-1]):
    ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, 
            f'{val:,}', ha='left', va='center', fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_01_puertos_salida.png', dpi=150, bbox_inches='tight')
plt.close()

# --- Gráfica 2: Top 10 Tipos de Barcos ---
print("   📊 Gráfica 2: Tipos de barcos...")
fig, ax = plt.subplots(figsize=(12, 6))
tipos_barcos = df['ship_type'].value_counts().head(10)
colors = plt.cm.Oranges(np.linspace(0.3, 0.9, len(tipos_barcos)))
bars = ax.bar(tipos_barcos.index, tipos_barcos.values, color=colors)
ax.set_xlabel('Tipo de Barco', fontsize=12)
ax.set_ylabel('Número de Viajes', fontsize=12)
ax.set_title('Top 10 Tipos de Barcos más Comunes', fontsize=14, fontweight='bold')
ax.tick_params(axis='x', rotation=45)
for bar, val in zip(bars, tipos_barcos.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
            f'{val:,}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_02_tipos_barcos.png', dpi=150, bbox_inches='tight')
plt.close()

# --- Gráfica 3: Distribución de Duración de Viajes ---
print("   📊 Gráfica 3: Duración de viajes...")
fig, ax = plt.subplots(figsize=(10, 6))
duraciones = df['travel_days'].dropna()
duraciones_filtradas = duraciones[duraciones <= 60]  # Filtrar outliers
ax.hist(duraciones_filtradas, bins=30, color='#3498db', edgecolor='white', alpha=0.8)
ax.axvline(x=duraciones_filtradas.mean(), color='#e74c3c', linewidth=2, 
           label=f'Promedio: {duraciones_filtradas.mean():.1f} días')
ax.axvline(x=duraciones_filtradas.median(), color='#f39c12', linewidth=2, linestyle='--',
           label=f'Mediana: {duraciones_filtradas.median():.1f} días')
ax.set_xlabel('Duración del Viaje (días)', fontsize=12)
ax.set_ylabel('Frecuencia', fontsize=12)
ax.set_title('Distribución de Duración de Viajes', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_03_duracion_viajes.png', dpi=150, bbox_inches='tight')
plt.close()

# --- Gráfica 4: Viajes por Mes ---
print("   📊 Gráfica 4: Viajes por mes...")
fig, ax = plt.subplots(figsize=(10, 6))
viajes_mes = df.groupby('month').size()
meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
viajes_mes.index = [meses[i-1] for i in viajes_mes.index]
colors = plt.cm.Greens(np.linspace(0.3, 0.9, len(viajes_mes)))
bars = ax.bar(viajes_mes.index, viajes_mes.values, color=colors)
ax.set_xlabel('Mes', fontsize=12)
ax.set_ylabel('Número de Viajes', fontsize=12)
ax.set_title('Distribución de Viajes por Mes', fontsize=14, fontweight='bold')
for bar, val in zip(bars, viajes_mes.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
            f'{val:,}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_04_viajes_mes.png', dpi=150, bbox_inches='tight')
plt.close()

# --- Gráfica 5: Top 10 Puertos de Llegada ---
print("   📊 Gráfica 5: Puertos de llegada...")
fig, ax = plt.subplots(figsize=(12, 6))
puertos_llegada = df['travel_arrival_port'].value_counts().head(10)
colors = plt.cm.Purples(np.linspace(0.3, 0.9, len(puertos_llegada)))
bars = ax.barh(puertos_llegada.index[::-1], puertos_llegada.values[::-1], color=colors)
ax.set_xlabel('Número de Viajes', fontsize=12)
ax.set_ylabel('Puerto de Llegada', fontsize=12)
ax.set_title('Top 10 Puertos de Llegada más Frecuentes', fontsize=14, fontweight='bold')
for bar, val in zip(bars, puertos_llegada.values[::-1]):
    ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, 
            f'{val:,}', ha='left', va='center', fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_05_puertos_llegada.png', dpi=150, bbox_inches='tight')
plt.close()

# --- Gráfica 6: Sección de Noticias ---
print("   📊 Gráfica 6: Secciones de noticias...")
fig, ax = plt.subplots(figsize=(8, 8))
secciones = df['news_section'].value_counts()
colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'][:len(secciones)]
wedges, texts, autotexts = ax.pie(secciones.values, labels=secciones.index, autopct='%1.1f%%',
                                   colors=colors, startangle=90)
ax.set_title('Distribución por Sección de Noticias', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'grafica_06_secciones.png', dpi=150, bbox_inches='tight')
plt.close()

print("✅ Todas las gráficas generadas")

# =============================================================================
# 5. EXPORTAR DATOS A CSV
# =============================================================================

print("\n💾 Exportando datos a CSV...")

# Resumen por puerto de salida
resumen_puertos = df.groupby('travel_departure_port').agg({
    'ship_name': 'count',
    'travel_days': 'mean'
}).round(2)
resumen_puertos.columns = ['Total_Viajes', 'Duracion_Promedio']
resumen_puertos = resumen_puertos.sort_values('Total_Viajes', ascending=False)
resumen_puertos.to_csv(OUTPUT_DIR / 'resumen_puertos.csv')
print(f"   ✅ Exportado: resumen_puertos.csv ({len(resumen_puertos)} puertos)")

# Resumen por tipo de barco
resumen_barcos = df.groupby('ship_type').agg({
    'ship_name': 'count',
    'travel_days': 'mean'
}).round(2)
resumen_barcos.columns = ['Total_Viajes', 'Duracion_Promedio']
resumen_barcos = resumen_barcos.sort_values('Total_Viajes', ascending=False)
resumen_barcos.to_csv(OUTPUT_DIR / 'resumen_barcos.csv')
print(f"   ✅ Exportado: resumen_barcos.csv ({len(resumen_barcos)} tipos)")

# Datos filtrados (viajes largos > 30 días)
viajes_largos = df[df['travel_days'] > 30][['publication_date', 'travel_departure_port', 
                                             'travel_arrival_port', 'ship_type', 'ship_name', 
                                             'travel_days']].copy()
viajes_largos.to_csv(OUTPUT_DIR / 'viajes_largos.csv', index=False)
print(f"   ✅ Exportado: viajes_largos.csv ({len(viajes_largos)} viajes > 30 días)")

# =============================================================================
# 6. GENERAR REPORTE PDF
# =============================================================================

print("\n📄 Generando reporte PDF con múltiples gráficas...")

# Template sin portada, con logo en footer
template = ReportTemplate(
    primary_color="#1a365d",
    footer_logo_enabled=True,
    footer_logo_path=LOGO_PATH if LOGO_PATH.exists() else None,
    footer_logo_position=LogoPosition.BOTTOM_RIGHT,
    footer_logo_width=100.0,
    footer_logo_height=50.0,
)

generator = ReportGenerator(OUTPUT_DIR / "reporte_maritimo_completo.pdf", template=template)

story = generator.story
styles = generator.styles

# === PÁGINA 1: Título y Resumen Ejecutivo ===
story.append(Paragraph("Análisis de Datos Marítimos Históricos", styles['Title']))
story.append(Spacer(1, 20))

story.append(Paragraph("Resumen Ejecutivo", styles['Heading']))
resumen_texto = f"""
Este informe presenta un análisis detallado de {stats['total_registros']:,} registros de navegación 
marítima histórica del período {stats['fecha_min'].strftime('%Y') if pd.notna(stats['fecha_min']) else 'N/A'} - 
{stats['fecha_max'].strftime('%Y') if pd.notna(stats['fecha_max']) else 'N/A'}. Los datos incluyen información 
sobre puertos de salida y llegada, tipos de embarcaciones, duración de viajes y carga transportada.
"""
story.append(Paragraph(resumen_texto.strip(), styles['Body']))
story.append(Spacer(1, 15))

# Métricas principales
story.append(Paragraph("Métricas Principales", styles['Heading']))
metricas = f"""
• Total de registros analizados: {stats['total_registros']:,}<br/>
• Puertos de salida únicos: {stats['puertos_salida']}<br/>
• Puertos de llegada únicos: {stats['puertos_llegada']}<br/>
• Tipos de embarcaciones: {stats['tipos_barcos']}<br/>
• Embarcaciones únicas: {stats['barcos_unicos']}<br/>
• Duración promedio de viaje: {stats['duracion_promedio']:.1f} días<br/>
• Viaje más largo: {stats['duracion_max']:.0f} días<br/>
• Viaje más corto: {stats['duracion_min']:.0f} días
"""
story.append(Paragraph(metricas.strip(), styles['Body']))
story.append(Spacer(1, 15))

# Tabla de resumen por tipo de barco
story.append(Paragraph("Top 10 Tipos de Embarcaciones", styles['Heading']))
tabla_barcos = resumen_barcos.head(10).reset_index()
tabla_barcos.columns = ['Tipo', 'Viajes', 'Duración Prom.']
generator._add_table(tabla_barcos)

# === PÁGINA 2: Gráficas de Puertos ===
story.append(PageBreak())

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

add_chart(OUTPUT_DIR / 'grafica_01_puertos_salida.png', "1. Puertos de Salida más Frecuentes")
add_chart(OUTPUT_DIR / 'grafica_05_puertos_llegada.png', "2. Puertos de Llegada más Frecuentes")

# === PÁGINA 3: Gráficas de Embarcaciones ===
story.append(PageBreak())

add_chart(OUTPUT_DIR / 'grafica_02_tipos_barcos.png', "3. Tipos de Embarcaciones más Comunes")
add_chart(OUTPUT_DIR / 'grafica_03_duracion_viajes.png', "4. Distribución de Duración de Viajes")

# === PÁGINA 4: Gráficas Temporales ===
story.append(PageBreak())

add_chart(OUTPUT_DIR / 'grafica_04_viajes_mes.png', "5. Distribución de Viajes por Mes")
add_chart(OUTPUT_DIR / 'grafica_06_secciones.png', "6. Distribución por Sección de Noticias")

# === PÁGINA 5: Conclusiones ===
story.append(PageBreak())

story.append(Paragraph("Conclusiones", styles['Heading']))
conclusiones = f"""
El análisis de los {stats['total_registros']:,} registros marítimos históricos revela patrones 
interesantes sobre el comercio y la navegación de la época:

<b>Principales hallazgos:</b><br/>
• La Habana aparece como el puerto de llegada predominante, reflejando su importancia como 
  centro comercial del Caribe.<br/>
• Los tipos de embarcaciones más comunes incluyen bergantines, goletas y vapores, 
  representando la transición tecnológica de la época.<br/>
• La duración promedio de los viajes de {stats['duracion_promedio']:.1f} días indica rutas 
  principalmente regionales y transatlánticas.<br/>
• La distribución mensual muestra patrones estacionales en la actividad marítima.

<b>Archivos exportados:</b><br/>
• resumen_puertos.csv - Estadísticas por puerto de salida<br/>
• resumen_barcos.csv - Estadísticas por tipo de embarcación<br/>
• viajes_largos.csv - Viajes con duración superior a 30 días
"""
story.append(Paragraph(conclusiones.strip(), styles['Body']))

# Construir documento
generator._build_document()

print(f"✅ Reporte generado: {OUTPUT_DIR / 'reporte_maritimo_completo.pdf'}")

# =============================================================================
# 7. RESUMEN FINAL
# =============================================================================

print("\n" + "=" * 70)
print("✅ PROCESO COMPLETADO")
print("=" * 70)

print(f"""
📁 Archivos generados en: {OUTPUT_DIR}

📊 Gráficas PNG:
   - grafica_01_puertos_salida.png
   - grafica_02_tipos_barcos.png
   - grafica_03_duracion_viajes.png
   - grafica_04_viajes_mes.png
   - grafica_05_puertos_llegada.png
   - grafica_06_secciones.png

💾 Archivos CSV:
   - resumen_puertos.csv
   - resumen_barcos.csv
   - viajes_largos.csv

📄 Reporte PDF:
   - reporte_maritimo_completo.pdf (5 páginas)

📈 Estadísticas clave:
   - {stats['total_registros']:,} registros analizados
   - {stats['puertos_salida']} puertos de salida
   - {stats['tipos_barcos']} tipos de embarcaciones
   - {stats['duracion_promedio']:.1f} días duración promedio
""")

print("=" * 70)
