"""
03 - Exportar Resultados a CSV
==============================

Este ejemplo muestra cómo exportar los resultados de tus consultas
a archivos CSV compatibles con Excel.

Características:
- Encoding UTF-8 con BOM (compatible con Excel)
- Opción de incluir o excluir índice
- Métodos confiables de exportación
- Mensajes de error amigables
"""

from qry_doc import QryDoc, ExportError
import pandasai as pai
from pandasai_openai import OpenAI
import os

# Configuración
llm = OpenAI()
pai.config.set({"llm": llm})

# Inicializar QryDoc
qry = QryDoc("data/ventas.csv", llm=llm)

# Crear carpeta de salida
os.makedirs("output", exist_ok=True)


# =============================================================================
# EXPORTACIÓN DIRECTA (MÁS CONFIABLE)
# =============================================================================

print("=" * 60)
print("EXPORTACIÓN DIRECTA DEL DATAFRAME")
print("=" * 60)

# Exportar todos los datos
resultado = qry.export_dataframe("output/todos_los_datos.csv")
print(resultado)

# Ver las columnas disponibles
print(f"\nColumnas disponibles: {qry.columns}")


# =============================================================================
# EXPORTAR CON FILTROS (SIN LLM - MUY CONFIABLE)
# =============================================================================

print("\n" + "=" * 60)
print("EXPORTAR CON FILTROS")
print("=" * 60)

# Filtrar por región
resultado = qry.filter_and_export(
    "output/ventas_centro.csv",
    filters={"region": "Centro"}
)
print(resultado)

# Filtrar por categoría
resultado = qry.filter_and_export(
    "output/ventas_accesorios.csv",
    filters={"categoria": "Accesorios"}
)
print(resultado)

# Seleccionar columnas específicas
resultado = qry.filter_and_export(
    "output/resumen_ventas.csv",
    columns=["fecha", "producto", "cantidad", "precio_unitario"]
)
print(resultado)

# Combinar filtros y columnas
resultado = qry.filter_and_export(
    "output/ventas_sur_resumen.csv",
    columns=["producto", "cantidad", "vendedor"],
    filters={"region": "Sur"}
)
print(resultado)


# =============================================================================
# EXPORTACIÓN CON CONSULTA LLM (PUEDE VARIAR)
# =============================================================================

print("\n" + "=" * 60)
print("EXPORTACIÓN CON CONSULTA LLM")
print("=" * 60)

def safe_extract(query: str, out_path: str):
    """Intentar exportar con manejo de errores."""
    try:
        result = qry.extract_to_csv(query, out_path)
        print(f"✅ {result}")
        return result
    except Exception as e:
        msg = getattr(e, "user_message", str(e))
        print(f"⚠️ No se pudo exportar: {msg[:100]}")
        return None

# Intentar exportaciones con LLM
safe_extract(
    "Muestra todas las filas donde la cantidad sea mayor a 2",
    "output/ventas_grandes.csv"
)

safe_extract(
    "Agrupa por vendedor y suma las cantidades",
    "output/ventas_por_vendedor.csv"
)


# =============================================================================
# TRABAJAR CON EL DATAFRAME DIRECTAMENTE
# =============================================================================

print("\n" + "=" * 60)
print("TRABAJAR CON EL DATAFRAME")
print("=" * 60)

# Acceder al DataFrame subyacente
df = qry.dataframe

# Hacer operaciones de pandas
ventas_por_categoria = df.groupby("categoria")["cantidad"].sum().reset_index()
ventas_por_categoria.columns = ["categoria", "total_cantidad"]

# Exportar resultado de pandas
from qry_doc.csv_exporter import CSVExporter
resultado = CSVExporter.export(ventas_por_categoria, "output/ventas_por_categoria.csv")
print(resultado)

# Calcular ingresos
df["ingresos"] = df["cantidad"] * df["precio_unitario"]
ventas_por_vendedor = df.groupby("vendedor")["ingresos"].sum().reset_index()
ventas_por_vendedor.columns = ["vendedor", "total_ingresos"]
ventas_por_vendedor = ventas_por_vendedor.sort_values("total_ingresos", ascending=False)

resultado = CSVExporter.export(ventas_por_vendedor, "output/ranking_vendedores.csv")
print(resultado)


# =============================================================================
# TIPS PARA MEJORES RESULTADOS
# =============================================================================

print("\n" + "=" * 60)
print("TIPS PARA EXPORTAR DATOS")
print("=" * 60)

print("""
💡 Métodos de exportación disponibles:

1. export_dataframe() - Exporta todos los datos (más confiable)
   qry.export_dataframe("todos.csv")

2. filter_and_export() - Filtra y exporta sin LLM (muy confiable)
   qry.filter_and_export("filtrado.csv", 
       columns=["col1", "col2"],
       filters={"region": "Norte"})

3. extract_to_csv() - Usa LLM para interpretar consulta (puede variar)
   qry.extract_to_csv("Muestra ventas de enero", "enero.csv")

4. Acceso directo al DataFrame:
   df = qry.dataframe
   resultado = df.groupby("categoria").sum()
   CSVExporter.export(resultado, "agregado.csv")

📝 Recomendaciones:
- Use filter_and_export() para filtros simples
- Use el DataFrame directamente para agregaciones complejas
- Use extract_to_csv() solo cuando necesite interpretación de lenguaje natural
""")


print("\n✅ Ejemplos de exportación completados")
print(f"📁 Archivos generados en la carpeta 'output/'")
