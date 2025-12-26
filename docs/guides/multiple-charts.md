# Reportes con Múltiples Gráficas

Esta guía muestra cómo crear reportes PDF profesionales con múltiples gráficas y análisis detallado.

## Caso de Uso

Cuando necesitas generar un reporte completo con:

- Múltiples visualizaciones (barras, histogramas, pie charts)
- Tablas de datos
- Análisis estadístico
- Varias páginas organizadas

## Método Básico vs Avanzado

### Método Básico: `build()`

El método `build()` acepta **una sola gráfica**:

```python
from qry_doc import ReportTemplate
from qry_doc.report_generator import ReportGenerator

generator = ReportGenerator("reporte.pdf", template=template)
generator.build(
    title="Mi Reporte",
    summary="Resumen ejecutivo...",
    chart_path=Path("grafica.png"),  # Solo una gráfica
    dataframe=df
)
```

### Método Avanzado: Acceso directo al `story`

Para múltiples gráficas, accede directamente al `story` de ReportLab:

```python
from reportlab.platypus import Paragraph, Spacer, Image, PageBreak
from qry_doc import ReportTemplate
from qry_doc.report_generator import ReportGenerator

# Crear generador
generator = ReportGenerator("reporte.pdf", template=template)

# Acceder al story y estilos
story = generator.story
styles = generator.styles
```

## Ejemplo Completo

### 1. Configurar Template (sin portada)

```python
from pathlib import Path
from qry_doc import ReportTemplate
from qry_doc.report_template import LogoPosition

template = ReportTemplate(
    primary_color="#1a365d",
    # Sin cover_image_path = sin portada
    footer_logo_enabled=True,
    footer_logo_path=Path("public/logo.png"),
    footer_logo_position=LogoPosition.BOTTOM_RIGHT,
)
```

### 2. Generar Gráficas con Matplotlib

```python
import matplotlib.pyplot as plt

# Configurar estilo
plt.style.use('seaborn-v0_8-whitegrid')

# Gráfica 1: Barras
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(categorias, valores, color=plt.cm.Blues(range(50, 250, 20)))
ax.set_title('Mi Gráfica de Barras', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('output/grafica_01.png', dpi=150, bbox_inches='tight')
plt.close()

# Gráfica 2: Histograma
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(datos, bins=50, color='#3498db', edgecolor='white')
ax.set_title('Distribución', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('output/grafica_02.png', dpi=150, bbox_inches='tight')
plt.close()

# Gráfica 3: Pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', colors=colores)
ax.set_title('Distribución por Categoría', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('output/grafica_03.png', dpi=150, bbox_inches='tight')
plt.close()
```

### 3. Construir el PDF con Múltiples Gráficas

```python
from reportlab.platypus import Paragraph, Spacer, Image, PageBreak
from qry_doc.report_generator import ReportGenerator

generator = ReportGenerator("output/reporte_completo.pdf", template=template)

story = generator.story
styles = generator.styles

# === PÁGINA 1: Título y Resumen ===
story.append(Paragraph("Análisis de Datos", styles['Title']))
story.append(Spacer(1, 20))

story.append(Paragraph("Resumen Ejecutivo", styles['Heading']))
story.append(Paragraph("Este informe presenta un análisis detallado...", styles['Body']))
story.append(Spacer(1, 15))

# Métricas con HTML
metricas = """
• Total de registros: 30,000<br/>
• Categorías: 12<br/>
• Tasa de éxito: 84.1%
"""
story.append(Paragraph(metricas, styles['Body']))

# Agregar tabla
story.append(Paragraph("Resumen de Datos", styles['Heading']))
generator._add_table(df_resumen)

# === PÁGINA 2: Gráficas 1 y 2 ===
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
        print(f"Error cargando {path}: {e}")

add_chart(Path("output/grafica_01.png"), "1. Gráfica de Barras")
add_chart(Path("output/grafica_02.png"), "2. Histograma")

# === PÁGINA 3: Gráfica 3 y Conclusiones ===
story.append(PageBreak())

add_chart(Path("output/grafica_03.png"), "3. Distribución")

story.append(Paragraph("Conclusiones", styles['Heading']))
story.append(Paragraph("Los datos muestran que...", styles['Body']))

# === CONSTRUIR DOCUMENTO ===
generator._build_document()

print("✅ Reporte generado con múltiples gráficas")
```

## Estilos Disponibles

El generador proporciona estos estilos predefinidos:

| Estilo | Uso |
|--------|-----|
| `styles['Title']` | Título principal del reporte |
| `styles['Heading']` | Encabezados de sección |
| `styles['Body']` | Texto de párrafo |
| `styles['Normal']` | Texto normal |

## Elementos de ReportLab

Puedes usar cualquier elemento de Platypus:

```python
from reportlab.platypus import (
    Paragraph,    # Texto con formato
    Spacer,       # Espacio vertical
    Image,        # Imágenes
    PageBreak,    # Salto de página
    Table,        # Tablas personalizadas
)
```

## Tips para Gráficas

### Tamaño Óptimo

```python
# Para gráficas que ocupen media página
plt.figure(figsize=(10, 6))

# Para gráficas más pequeñas (2 por página)
plt.figure(figsize=(10, 4))

# Para pie charts
plt.figure(figsize=(8, 8))
```

### DPI Recomendado

```python
# 150 DPI es un buen balance entre calidad y tamaño
plt.savefig('grafica.png', dpi=150, bbox_inches='tight')
```

### Escalar Imágenes en el PDF

```python
img = Image(str(path))
max_width = template.content_width  # Ancho disponible
max_height = 280  # Altura máxima

# Calcular escala manteniendo proporción
scale = min(
    max_width / img.imageWidth,
    max_height / img.imageHeight,
    1.0  # No agrandar
)

img.drawWidth = img.imageWidth * scale
img.drawHeight = img.imageHeight * scale
```

## Organización de Páginas

### Dos gráficas por página

```python
add_chart(path1, "Gráfica 1")
add_chart(path2, "Gráfica 2")
story.append(PageBreak())
```

### Una gráfica grande por página

```python
add_chart_large(path1, "Gráfica Grande")
story.append(PageBreak())
```

## Ejemplo de Salida

El reporte generado tendrá esta estructura:

```
📄 Página 1: Título, resumen, métricas, tabla
📄 Página 2: Gráficas 1 y 2
📄 Página 3: Gráficas 3 y 4
📄 Página 4: Gráfica 5 y conclusiones
```

## Ver También

- [Sistema de Secciones](sections.md) - Para reportes con estructura predefinida
- [Portadas](cover-pages.md) - Agregar portada al reporte
- [Logo en Footer](footer-logos.md) - Personalizar el pie de página
