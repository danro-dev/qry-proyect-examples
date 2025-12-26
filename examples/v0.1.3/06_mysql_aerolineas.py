"""
Ejemplo 06: Análisis de Aerolíneas con MySQL
============================================

Este ejemplo demuestra cómo conectar qry-doc a una base de datos MySQL
real con datos de puntualidad de aerolíneas estadounidenses.

Base de datos: Airline (CTU Relational)
- 445,827 vuelos de enero 2016
- 16 aerolíneas principales de EE.UU.
- Datos del Departamento de Transporte (DOT)

Características demostradas:
- Conexión a MySQL remoto
- Exploración automática de estructura
- Consultas en lenguaje natural
- Generación de reportes PDF
- Exportación de datos filtrados
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importaciones de qry-doc
from qry_doc import QryDoc, ReportTemplate
from qry_doc.data_source import DataSourceLoader
from qry_doc.report_template import LogoPosition

# Configurar LLM (necesario para consultas en lenguaje natural)
import pandasai as pai
from pandasai_openai import OpenAI

llm = OpenAI()
pai.config.set({"llm": llm})

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

# Conexión MySQL - Base de datos de aerolíneas
MYSQL_URL = "mysql+pymysql://guest:ctu-relational@relational.fel.cvut.cz:3306/Airline"

# Directorio de salida
OUTPUT_DIR = Path("output/aerolineas")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Portada (opcional)
PORTADA_PATH = Path("public/portada.png")


# =============================================================================
# 1. EXPLORAR BASE DE DATOS
# =============================================================================

print("=" * 70)
print("🛫 ANÁLISIS DE PUNTUALIDAD DE AEROLÍNEAS - MySQL")
print("=" * 70)

print("\n📊 Explorando base de datos...")
try:
    db_info = DataSourceLoader.explore_database(MYSQL_URL)
    
    print(f"\nTablas encontradas: {len(db_info['tables'])}")
    for tabla, info in db_info['tables'].items():
        print(f"  📋 {tabla}: {info['row_count']:,} filas")
        
except Exception as e:
    print(f"❌ Error al explorar: {e}")
    exit(1)


# =============================================================================
# 2. CARGAR DATOS CON QUERY PERSONALIZADO
# =============================================================================

print("\n🔗 Cargando datos de vuelos...")

# Query para obtener un resumen manejable (los datos completos son 445k filas)
# Tomamos una muestra de todas las aerolíneas
query = """
SELECT 
    UniqueCarrier as Aerolinea,
    Carrier as Codigo,
    Origin as Origen,
    OriginCityName as CiudadOrigen,
    OriginState as EstadoOrigen,
    Dest as Destino,
    DestCityName as CiudadDestino,
    DestState as EstadoDestino,
    FlightDate as Fecha,
    DayOfWeek as DiaSemana,
    DepDelay as RetrasoSalida,
    ArrDelay as RetrasoLlegada,
    Distance as Distancia,
    Cancelled as Cancelado,
    Diverted as Desviado,
    CarrierDelay as RetrasoAerolinea,
    WeatherDelay as RetrasoClima,
    NASDelay as RetrasoNAS,
    AirTime as TiempoVuelo
FROM On_Time_On_Time_Performance_2016_1
WHERE DepDelay IS NOT NULL
ORDER BY RAND()
LIMIT 20000
"""

try:
    df = DataSourceLoader.load_sql_query(MYSQL_URL, query)
    print(f"✅ Datos cargados: {len(df):,} vuelos")
    print(f"   Columnas: {list(df.columns)}")
    print(f"\n   Muestra de datos:")
    print(df.head(3).to_string())
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)


# =============================================================================
# 3. CREAR INSTANCIA DE QryDoc
# =============================================================================

print("\n🤖 Inicializando QryDoc...")
qry = QryDoc(df, llm=llm)
print(f"✅ QryDoc listo - {qry.shape[0]:,} filas x {qry.shape[1]} columnas")


# =============================================================================
# 4. CONSULTAS EN LENGUAJE NATURAL
# =============================================================================

print("\n" + "=" * 70)
print("💬 CONSULTAS EN LENGUAJE NATURAL")
print("=" * 70)

consultas = [
    "¿Cuántos vuelos hay en total?",
    "¿Cuáles son las 5 aerolíneas con más vuelos?",
    "¿Cuál es el retraso promedio de salida en minutos?",
    "¿Qué porcentaje de vuelos fueron cancelados?",
    "¿Cuáles son los 5 aeropuertos de origen con más vuelos?",
    "¿Cuál es la distancia promedio de los vuelos?",
]

for pregunta in consultas:
    try:
        print(f"\n❓ {pregunta}")
        respuesta = qry.ask(pregunta)
        print(f"   ➡️  {respuesta}")
    except Exception as e:
        print(f"   ❌ Error: {e}")


# =============================================================================
# 5. ANÁLISIS AVANZADO
# =============================================================================

print("\n" + "=" * 70)
print("📈 ANÁLISIS AVANZADO")
print("=" * 70)

analisis_avanzados = [
    "¿Cuál es el día de la semana con más retrasos promedio?",
    "¿Qué aerolínea tiene el menor retraso promedio de llegada?",
    "¿Cuántos vuelos fueron desviados y cuál fue su retraso promedio?",
    "¿Cuál es la ruta (origen-destino) más frecuente?",
    "¿Qué porcentaje de retrasos se debe al clima?",
]

for pregunta in analisis_avanzados:
    try:
        print(f"\n❓ {pregunta}")
        respuesta = qry.ask(pregunta)
        print(f"   ➡️  {respuesta}")
    except Exception as e:
        print(f"   ❌ Error: {e}")


# =============================================================================
# 6. EXPORTAR DATOS
# =============================================================================

print("\n" + "=" * 70)
print("📁 EXPORTAR DATOS")
print("=" * 70)

# Exportar todos los datos
resultado = qry.export_dataframe(OUTPUT_DIR / "vuelos_completos.csv")
print(f"\n✅ {resultado}")

# Exportar vuelos cancelados
try:
    df_cancelados = df[df['Cancelado'] == 1]
    if len(df_cancelados) > 0:
        df_cancelados.to_csv(OUTPUT_DIR / "vuelos_cancelados.csv", index=False)
        print(f"✅ Exportados {len(df_cancelados)} vuelos cancelados")
except Exception as e:
    print(f"⚠️  No se pudieron exportar cancelados: {e}")

# Exportar resumen por aerolínea
try:
    resumen = df.groupby('Aerolinea').agg({
        'Fecha': 'count',
        'RetrasoSalida': 'mean',
        'RetrasoLlegada': 'mean',
        'Distancia': 'mean',
        'Cancelado': 'sum'
    }).round(2)
    resumen.columns = ['TotalVuelos', 'RetrasoSalidaPromedio', 'RetrasoLlegadaPromedio', 'DistanciaPromedio', 'Cancelados']
    resumen = resumen.sort_values('TotalVuelos', ascending=False)
    resumen.to_csv(OUTPUT_DIR / "resumen_aerolineas.csv")
    print(f"✅ Exportado resumen de {len(resumen)} aerolíneas")
except Exception as e:
    print(f"⚠️  Error en resumen: {e}")


# =============================================================================
# 7. GENERAR REPORTES PDF
# =============================================================================

print("\n" + "=" * 70)
print("📄 GENERAR REPORTES PDF")
print("=" * 70)

# Template personalizado
template = ReportTemplate(
    primary_color="#1a365d",  # Azul oscuro
    cover_image_path=PORTADA_PATH if PORTADA_PATH.exists() else None,
    footer_logo_enabled=True,
    footer_logo_position=LogoPosition.BOTTOM_RIGHT,
)

# Reporte 1: Análisis general
print("\n📄 Generando reporte de análisis general...")
try:
    qry.generate_report(
        "Genera un análisis ejecutivo de los datos de vuelos, incluyendo estadísticas de retrasos, aerolíneas principales y tendencias",
        OUTPUT_DIR / "reporte_analisis_general.pdf",
        title="Análisis de Puntualidad de Aerolíneas",
        template=template,
        include_chart=True,
        chart_type='bar',
        group_by='Aerolinea',
        value_column='RetrasoSalida'
    )
    print("✅ Reporte de análisis general generado")
except Exception as e:
    print(f"❌ Error: {e}")

# Reporte 2: Top aerolíneas
print("\n📄 Generando reporte de aerolíneas...")
try:
    # Crear DataFrame resumido para el reporte
    df_top = df.groupby('Aerolinea').agg({
        'Fecha': 'count',
        'RetrasoSalida': 'mean',
        'Cancelado': 'sum'
    }).round(2).reset_index()
    df_top.columns = ['Aerolínea', 'Total Vuelos', 'Retraso Promedio (min)', 'Cancelados']
    df_top = df_top.sort_values('Total Vuelos', ascending=False).head(10)
    
    qry_top = QryDoc(df_top, llm=llm)
    qry_top.generate_report(
        "Analiza el rendimiento de las principales aerolíneas",
        OUTPUT_DIR / "reporte_top_aerolineas.pdf",
        title="Top 10 Aerolíneas por Volumen",
        template=template
    )
    print("✅ Reporte de top aerolíneas generado")
except Exception as e:
    print(f"❌ Error: {e}")

# Reporte 3: Análisis de retrasos
print("\n📄 Generando reporte de retrasos...")
try:
    qry.generate_report(
        "Analiza los patrones de retrasos: causas principales, aerolíneas más afectadas y días con más retrasos",
        OUTPUT_DIR / "reporte_retrasos.pdf",
        title="Análisis de Retrasos en Vuelos",
        template=template,
        include_chart=True,
        chart_type='pie',
        group_by='DiaSemana',
        value_column='RetrasoSalida'
    )
    print("✅ Reporte de retrasos generado")
except Exception as e:
    print(f"❌ Error: {e}")


# =============================================================================
# 8. RESUMEN FINAL
# =============================================================================

print("\n" + "=" * 70)
print("✅ ANÁLISIS COMPLETADO")
print("=" * 70)

print(f"""
📊 Datos analizados:
   - {len(df):,} vuelos
   - {df['Aerolinea'].nunique()} aerolíneas
   - {df['Origen'].nunique()} aeropuertos de origen
   - {df['Destino'].nunique()} aeropuertos de destino

📁 Archivos generados en: {OUTPUT_DIR}
   - vuelos_completos.csv
   - vuelos_cancelados.csv
   - resumen_aerolineas.csv
   - reporte_analisis_general.pdf
   - reporte_top_aerolineas.pdf
   - reporte_retrasos.pdf

🔗 Base de datos: MySQL (CTU Relational)
   - Host: relational.fel.cvut.cz
   - Database: Airline
""")

print("=" * 70)
