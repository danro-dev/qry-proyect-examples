"""
04 - Generar Reportes PDF
=========================

Este ejemplo muestra cómo generar reportes PDF profesionales
con qry-doc.

Los reportes incluyen:
- Título y resumen ejecutivo
- Gráficos y visualizaciones (cuando aplica)
- Tablas de datos
- Encabezado y pie de página
"""

from qry_doc import QryDoc, ReportTemplate, ReportError
import pandasai as pai
from pandasai_openai import OpenAI
import os

# Configuración
llm = OpenAI()
pai.config.set({"llm": llm})
qry = QryDoc("data/ventas.csv", llm=llm)

# Crear carpeta de salida
os.makedirs("output/reportes", exist_ok=True)


# =============================================================================
# REPORTE BÁSICO
# =============================================================================

print("=" * 60)
print("REPORTE BÁSICO")
print("=" * 60)

# Generar un reporte simple
resultado = qry.generate_report(
    "Analiza las ventas por categoría de producto",
    "output/reportes/analisis_categorias.pdf"
)
print(resultado)
# Output: "Reporte generado exitosamente en output/reportes/analisis_categorias.pdf"


# =============================================================================
# REPORTE CON TÍTULO PERSONALIZADO
# =============================================================================

print("\n" + "=" * 60)
print("REPORTE CON TÍTULO PERSONALIZADO")
print("=" * 60)

resultado = qry.generate_report(
    "Muestra el rendimiento de cada vendedor",
    "output/reportes/rendimiento_vendedores.pdf",
    title="Informe de Rendimiento del Equipo de Ventas Q1 2024"
)
print(resultado)


# =============================================================================
# DIFERENTES TIPOS DE ANÁLISIS
# =============================================================================

print("\n" + "=" * 60)
print("DIFERENTES TIPOS DE ANÁLISIS")
print("=" * 60)

# Análisis temporal
resultado = qry.generate_report(
    "Analiza la evolución de las ventas mes a mes",
    "output/reportes/tendencia_mensual.pdf",
    title="Análisis de Tendencias Mensuales"
)
print(resultado)

# Análisis por región
resultado = qry.generate_report(
    "Compara el desempeño de ventas por región geográfica",
    "output/reportes/analisis_regional.pdf",
    title="Análisis de Ventas por Región"
)
print(resultado)

# Análisis de productos
resultado = qry.generate_report(
    "Identifica los productos más y menos vendidos",
    "output/reportes/analisis_productos.pdf",
    title="Análisis de Portafolio de Productos"
)
print(resultado)


# =============================================================================
# REPORTE CON TEMPLATE PERSONALIZADO
# =============================================================================

print("\n" + "=" * 60)
print("REPORTE CON TEMPLATE PERSONALIZADO")
print("=" * 60)

# Crear un template con colores corporativos
template_corporativo = ReportTemplate(
    primary_color="#003366",      # Azul corporativo
    title_font="Helvetica-Bold",
    body_font="Helvetica",
)

resultado = qry.generate_report(
    "Resumen ejecutivo de ventas del primer trimestre",
    "output/reportes/resumen_ejecutivo.pdf",
    title="Resumen Ejecutivo Q1 2024",
    template=template_corporativo
)
print(resultado)


# =============================================================================
# USANDO TEMPLATES PREDEFINIDOS
# =============================================================================

print("\n" + "=" * 60)
print("USANDO TEMPLATES PREDEFINIDOS")
print("=" * 60)

from qry_doc import (
    DEFAULT_TEMPLATE,
    CORPORATE_TEMPLATE,
    MINIMAL_TEMPLATE,
    A4_TEMPLATE,
)

# Template corporativo predefinido
resultado = qry.generate_report(
    "Análisis de márgenes por producto",
    "output/reportes/margenes_corporativo.pdf",
    title="Análisis de Rentabilidad",
    template=CORPORATE_TEMPLATE
)
print(f"Con CORPORATE_TEMPLATE: {resultado}")

# Template minimalista
resultado = qry.generate_report(
    "Resumen de ventas del mes",
    "output/reportes/resumen_minimal.pdf",
    title="Resumen Mensual",
    template=MINIMAL_TEMPLATE
)
print(f"Con MINIMAL_TEMPLATE: {resultado}")

# Template A4 (tamaño europeo)
resultado = qry.generate_report(
    "Informe detallado de operaciones",
    "output/reportes/informe_a4.pdf",
    title="Informe de Operaciones",
    template=A4_TEMPLATE
)
print(f"Con A4_TEMPLATE: {resultado}")


# =============================================================================
# MANEJO DE ERRORES
# =============================================================================

print("\n" + "=" * 60)
print("MANEJO DE ERRORES")
print("=" * 60)

try:
    # Si algo falla en la generación, se lanza ReportError
    qry.generate_report(
        "Genera un análisis",
        "output/reportes/test.pdf"
    )
except ReportError as e:
    print(f"Error: {e.user_message}")


# =============================================================================
# TIPS PARA MEJORES REPORTES
# =============================================================================

print("\n" + "=" * 60)
print("TIPS PARA MEJORES REPORTES")
print("=" * 60)

print("""
💡 Tips para generar mejores reportes:

1. Sé específico en el análisis que quieres:
   ❌ "Analiza los datos"
   ✅ "Analiza las ventas por categoría comparando Q1 vs Q2"

2. Usa consultas que generen visualizaciones:
   - "Muestra la tendencia de..." (genera gráfico de líneas)
   - "Compara las ventas de..." (genera gráfico de barras)
   - "Distribución de..." (genera gráfico circular)

3. Personaliza el título para que sea descriptivo:
   ❌ title="Reporte"
   ✅ title="Análisis de Ventas Q1 2024 - Región Norte"

4. Usa templates que coincidan con tu marca:
   - CORPORATE_TEMPLATE para informes formales
   - MINIMAL_TEMPLATE para presentaciones limpias
   - Crea tu propio ReportTemplate con tus colores

5. El reporte incluye automáticamente:
   - Resumen ejecutivo generado por IA
   - Gráficos relevantes (si aplica)
   - Tablas de datos de soporte
   - Numeración de páginas
""")


print("\n✅ Ejemplos de reportes completados")
print(f"📁 Reportes generados en 'output/reportes/'")
