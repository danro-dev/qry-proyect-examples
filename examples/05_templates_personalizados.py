"""
05 - Templates Personalizados
=============================

Este ejemplo muestra cómo personalizar completamente el estilo
de los reportes PDF usando ReportTemplate.

Opciones de personalización:
- Logo de empresa
- Colores corporativos
- Fuentes
- Tamaño de página
- Márgenes
- Encabezados y pies de página personalizados
"""

from qry_doc import QryDoc, ReportTemplate
import pandasai as pai
from pandasai_openai import OpenAI
from reportlab.lib.pagesizes import letter, A4, legal
from pathlib import Path
import os

# Configuración
llm = OpenAI()
pai.config.set({"llm": llm})
qry = QryDoc("data/ventas.csv", llm=llm)

# Crear carpeta de salida
os.makedirs("output/reportes_custom", exist_ok=True)


# =============================================================================
# TEMPLATE CON COLORES PERSONALIZADOS
# =============================================================================

print("=" * 60)
print("TEMPLATE CON COLORES PERSONALIZADOS")
print("=" * 60)

# Template con color verde corporativo
template_verde = ReportTemplate(
    primary_color="#2E7D32",  # Verde
)

qry.generate_report(
    "Análisis de ventas por región",
    "output/reportes_custom/reporte_verde.pdf",
    title="Informe de Ventas Regional",
    template=template_verde
)
print("✅ Reporte con color verde generado")

# Template con color rojo
template_rojo = ReportTemplate(
    primary_color="#C62828",  # Rojo
)

qry.generate_report(
    "Análisis de productos con bajo rendimiento",
    "output/reportes_custom/reporte_rojo.pdf",
    title="Alerta: Productos con Bajo Rendimiento",
    template=template_rojo
)
print("✅ Reporte con color rojo generado")


# =============================================================================
# TEMPLATE CON FUENTES PERSONALIZADAS
# =============================================================================

print("\n" + "=" * 60)
print("TEMPLATE CON FUENTES PERSONALIZADAS")
print("=" * 60)

# Fuentes disponibles en ReportLab (sin instalar adicionales):
# - Helvetica, Helvetica-Bold, Helvetica-Oblique
# - Times-Roman, Times-Bold, Times-Italic
# - Courier, Courier-Bold, Courier-Oblique

template_times = ReportTemplate(
    primary_color="#1565C0",
    title_font="Times-Bold",
    body_font="Times-Roman",
)

qry.generate_report(
    "Resumen ejecutivo trimestral",
    "output/reportes_custom/reporte_times.pdf",
    title="Resumen Ejecutivo Q1 2024",
    template=template_times
)
print("✅ Reporte con fuente Times generado")


# =============================================================================
# TEMPLATE CON TAMAÑO DE PÁGINA PERSONALIZADO
# =============================================================================

print("\n" + "=" * 60)
print("TEMPLATE CON TAMAÑO DE PÁGINA")
print("=" * 60)

# Tamaño A4 (estándar europeo)
template_a4 = ReportTemplate(
    primary_color="#6A1B9A",  # Púrpura
    page_size=A4,
)

qry.generate_report(
    "Informe para oficina europea",
    "output/reportes_custom/reporte_a4.pdf",
    title="Informe de Ventas - Europa",
    template=template_a4
)
print("✅ Reporte tamaño A4 generado")

# Tamaño Legal (más largo)
template_legal = ReportTemplate(
    primary_color="#00695C",  # Teal
    page_size=legal,
)

qry.generate_report(
    "Informe legal detallado",
    "output/reportes_custom/reporte_legal.pdf",
    title="Informe Detallado de Operaciones",
    template=template_legal
)
print("✅ Reporte tamaño Legal generado")


# =============================================================================
# TEMPLATE CON MÁRGENES PERSONALIZADOS
# =============================================================================

print("\n" + "=" * 60)
print("TEMPLATE CON MÁRGENES PERSONALIZADOS")
print("=" * 60)

# Márgenes amplios (más espacio en blanco)
template_margenes_amplios = ReportTemplate(
    primary_color="#37474F",
    margin_top=100.0,      # ~1.4 pulgadas
    margin_bottom=100.0,
    margin_left=90.0,      # ~1.25 pulgadas
    margin_right=90.0,
)

qry.generate_report(
    "Informe con márgenes amplios para encuadernación",
    "output/reportes_custom/reporte_margenes_amplios.pdf",
    title="Informe para Encuadernación",
    template=template_margenes_amplios
)
print("✅ Reporte con márgenes amplios generado")

# Márgenes reducidos (más contenido por página)
template_margenes_reducidos = ReportTemplate(
    primary_color="#455A64",
    margin_top=50.0,       # ~0.7 pulgadas
    margin_bottom=50.0,
    margin_left=50.0,
    margin_right=50.0,
)

qry.generate_report(
    "Informe compacto con más contenido",
    "output/reportes_custom/reporte_compacto.pdf",
    title="Informe Compacto",
    template=template_margenes_reducidos
)
print("✅ Reporte compacto generado")


# =============================================================================
# TEMPLATE CON LOGO (si tienes un archivo de imagen)
# =============================================================================

print("\n" + "=" * 60)
print("TEMPLATE CON LOGO")
print("=" * 60)

# Nota: Necesitas tener un archivo de logo (PNG, JPG)
# Si no existe, el reporte se genera sin logo

logo_path = Path("assets/mi_logo.png")

if logo_path.exists():
    template_con_logo = ReportTemplate(
        logo_path=logo_path,
        primary_color="#1976D2",
    )
    
    qry.generate_report(
        "Informe con logo corporativo",
        "output/reportes_custom/reporte_con_logo.pdf",
        title="Informe Corporativo",
        template=template_con_logo
    )
    print("✅ Reporte con logo generado")
else:
    print("ℹ️  No se encontró logo en 'assets/mi_logo.png'")
    print("   Crea esa carpeta y archivo para probar esta funcionalidad")


# =============================================================================
# TEMPLATE COMPLETO PERSONALIZADO
# =============================================================================

print("\n" + "=" * 60)
print("TEMPLATE COMPLETO PERSONALIZADO")
print("=" * 60)

# Combinando todas las opciones
template_completo = ReportTemplate(
    # Logo (opcional)
    logo_path=None,  # Cambiar por tu logo
    
    # Colores
    primary_color="#0D47A1",  # Azul oscuro
    
    # Fuentes
    title_font="Helvetica-Bold",
    body_font="Helvetica",
    
    # Tamaño de página
    page_size=letter,
    
    # Márgenes (en puntos, 72 puntos = 1 pulgada)
    margin_top=72.0,
    margin_bottom=72.0,
    margin_left=72.0,
    margin_right=72.0,
    
    # Altura de encabezado y pie
    header_height=50.0,
    footer_height=30.0,
)

qry.generate_report(
    "Análisis completo de ventas del trimestre",
    "output/reportes_custom/reporte_completo.pdf",
    title="Análisis Integral de Ventas Q1 2024",
    template=template_completo
)
print("✅ Reporte con template completo generado")


# =============================================================================
# ENCABEZADO Y PIE DE PÁGINA PERSONALIZADOS
# =============================================================================

print("\n" + "=" * 60)
print("ENCABEZADO Y PIE PERSONALIZADOS")
print("=" * 60)

# Puedes definir funciones personalizadas para header/footer
def mi_header(canvas, doc):
    """Encabezado personalizado."""
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(72, 750, "MI EMPRESA S.A.")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(540, 750, "Confidencial")
    canvas.line(72, 745, 540, 745)
    canvas.restoreState()

def mi_footer(canvas, doc):
    """Pie de página personalizado."""
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.line(72, 50, 540, 50)
    canvas.drawString(72, 35, "© 2024 Mi Empresa S.A. - Todos los derechos reservados")
    canvas.drawRightString(540, 35, f"Página {doc.page}")
    canvas.restoreState()

# Crear template y asignar callbacks
template_custom_header = ReportTemplate(
    primary_color="#263238",
)
template_custom_header.set_header_callback(mi_header)
template_custom_header.set_footer_callback(mi_footer)

qry.generate_report(
    "Informe con encabezado y pie personalizados",
    "output/reportes_custom/reporte_header_custom.pdf",
    title="Informe Confidencial",
    template=template_custom_header
)
print("✅ Reporte con header/footer personalizado generado")


# =============================================================================
# REFERENCIA DE COLORES SUGERIDOS
# =============================================================================

print("\n" + "=" * 60)
print("REFERENCIA DE COLORES")
print("=" * 60)

print("""
🎨 Colores sugeridos para reportes profesionales:

Azules (confianza, profesionalismo):
  - #0D47A1 (azul oscuro)
  - #1565C0 (azul medio)
  - #1976D2 (azul claro)
  - #003366 (azul corporativo)

Verdes (crecimiento, éxito):
  - #1B5E20 (verde oscuro)
  - #2E7D32 (verde medio)
  - #388E3C (verde claro)

Grises (neutralidad, elegancia):
  - #263238 (gris muy oscuro)
  - #37474F (gris oscuro)
  - #455A64 (gris medio)

Rojos (alertas, urgencia):
  - #B71C1C (rojo oscuro)
  - #C62828 (rojo medio)
  - #D32F2F (rojo claro)

Púrpuras (creatividad, lujo):
  - #4A148C (púrpura oscuro)
  - #6A1B9A (púrpura medio)
  - #7B1FA2 (púrpura claro)
""")


print("\n✅ Ejemplos de templates completados")
print(f"📁 Reportes generados en 'output/reportes_custom/'")
