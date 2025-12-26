"""
08 - Conexión a PostgreSQL
==========================

Este ejemplo muestra cómo conectar qry-doc a una base de datos PostgreSQL.
La librería explora automáticamente la base de datos y selecciona la mejor tabla.

Requisitos:
- PostgreSQL corriendo
- pip install psycopg2-binary sqlalchemy
"""

from qry_doc import QryDoc
from qry_doc.data_source import DataSourceLoader
import pandasai as pai
from pandasai_openai import OpenAI
import os

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

# Configurar LLM
llm = OpenAI()
pai.config.set({"llm": llm})

# Cadena de conexión PostgreSQL desde variable de entorno o valor por defecto
POSTGRES_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://postgres:danro@127.0.0.1:5432/ap"
)

# Crear carpeta de salida
os.makedirs("output/postgres", exist_ok=True)


# =============================================================================
# EXPLORAR BASE DE DATOS
# =============================================================================

print("=" * 60)
print("EXPLORAR BASE DE DATOS")
print("=" * 60)

try:
    db_info = DataSourceLoader.explore_database(POSTGRES_URL)
    
    print(f"\n📊 Estructura de la base de datos:")
    print(f"\nTablas ({len(db_info['tables'])}):")
    for table_name, info in db_info['tables'].items():
        print(f"  📋 {table_name}: {info['row_count']} filas, {len(info['columns'])} columnas")
        for col in info['columns'][:5]:
            print(f"      - {col['name']} ({col['type']})")
        if len(info['columns']) > 5:
            print(f"      ... y {len(info['columns']) - 5} columnas más")
            
except Exception as e:
    print(f"❌ Error al explorar: {e}")


# =============================================================================
# CONEXIÓN AUTOMÁTICA
# =============================================================================

print("\n" + "=" * 60)
print("CONEXIÓN AUTOMÁTICA")
print("=" * 60)

try:
    qry = QryDoc(POSTGRES_URL, llm=llm)
    
    print(f"\n✅ Conexión exitosa")
    print(f"Columnas: {qry.columns}")
    print(f"Dimensiones: {qry.shape[0]} filas x {qry.shape[1]} columnas")
    
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    exit(1)


# =============================================================================
# GENERAR GRÁFICAS
# =============================================================================

print("\n" + "=" * 60)
print("GENERAR GRÁFICAS")
print("=" * 60)

# Detectar columnas numéricas y categóricas
numeric_cols = qry.dataframe.select_dtypes(include=['number']).columns.tolist()
categorical_cols = qry.dataframe.select_dtypes(exclude=['number']).columns.tolist()

print(f"Columnas numéricas: {numeric_cols}")
print(f"Columnas categóricas: {categorical_cols}")

# Gráfica de barras
if categorical_cols and numeric_cols:
    chart = qry.generate_chart(
        "output/postgres/grafica_barras.png",
        chart_type='bar',
        group_by=categorical_cols[0],
        value_column=numeric_cols[0],
        title=f'{numeric_cols[0]} por {categorical_cols[0]}'
    )
    print(f"✅ Gráfica de barras: {chart}")

# Gráfica de barras horizontales
if len(categorical_cols) > 1 and numeric_cols:
    chart = qry.generate_chart(
        "output/postgres/grafica_barras_h.png",
        chart_type='barh',
        group_by=categorical_cols[1] if len(categorical_cols) > 1 else categorical_cols[0],
        value_column=numeric_cols[0],
        title=f'{numeric_cols[0]} por {categorical_cols[1] if len(categorical_cols) > 1 else categorical_cols[0]}'
    )
    print(f"✅ Gráfica horizontal: {chart}")

# Gráfica de pie
if categorical_cols and numeric_cols:
    chart = qry.generate_chart(
        "output/postgres/grafica_pie.png",
        chart_type='pie',
        group_by=categorical_cols[0],
        value_column=numeric_cols[0],
        title=f'Distribución de {numeric_cols[0]}'
    )
    print(f"✅ Gráfica pie: {chart}")


# =============================================================================
# GENERAR REPORTES PDF CON GRÁFICAS
# =============================================================================

print("\n" + "=" * 60)
print("GENERAR REPORTES PDF")
print("=" * 60)

# Reporte con gráfica de barras
if categorical_cols and numeric_cols:
    result = qry.generate_report(
        f"Analiza los datos agrupados por {categorical_cols[0]}",
        "output/postgres/reporte_barras.pdf",
        title=f"Análisis por {categorical_cols[0].title()}",
        include_chart=True,
        chart_type='bar',
        group_by=categorical_cols[0],
        value_column=numeric_cols[0]
    )
    print(result)

# Reporte con gráfica pie
if categorical_cols and numeric_cols:
    result = qry.generate_report(
        f"Muestra la distribución de {numeric_cols[0]} por {categorical_cols[0]}",
        "output/postgres/reporte_pie.pdf",
        title=f"Distribución de {numeric_cols[0].title()}",
        include_chart=True,
        chart_type='pie',
        group_by=categorical_cols[0],
        value_column=numeric_cols[0]
    )
    print(result)


# =============================================================================
# CONSULTAS CON LLM
# =============================================================================

print("\n" + "=" * 60)
print("CONSULTAS CON LLM")
print("=" * 60)

# Preguntas sobre los datos
try:
    respuesta = qry.ask("¿Cuántos registros hay en total?")
    print(f"Total registros: {respuesta}")
except Exception as e:
    print(f"Error: {e}")

try:
    respuesta = qry.ask("¿Cuál es el valor total de todas las ventas?")
    print(f"Total ventas: {respuesta}")
except Exception as e:
    print(f"Error: {e}")


# =============================================================================
# EXPORTAR DATOS
# =============================================================================

print("\n" + "=" * 60)
print("EXPORTAR DATOS")
print("=" * 60)

# Exportar todos los datos
resultado = qry.export_dataframe("output/postgres/todos_los_datos.csv")
print(resultado)

# Exportar con filtros si hay columnas conocidas
string_cols = [c for c in categorical_cols if qry.dataframe[c].dtype == 'object']
if string_cols:
    unique_values = qry.dataframe[string_cols[0]].unique()[:3]
    for val in unique_values:
        safe_name = str(val).lower().replace(' ', '_').replace('/', '_')
        resultado = qry.filter_and_export(
            f"output/postgres/filtrado_{safe_name}.csv",
            filters={string_cols[0]: val}
        )
        print(resultado)


print("\n" + "=" * 60)
print("✅ Ejemplos de PostgreSQL completados")
print("📁 Archivos generados en 'output/postgres/'")
print("=" * 60)
