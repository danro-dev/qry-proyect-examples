# Portadas Personalizadas

<span class="version-badge new">v0.1.3</span>

Las portadas permiten agregar una imagen a página completa como primera página de tus reportes PDF.

## Uso básico

```python
from pathlib import Path
from qry_doc import ReportTemplate, ReportGenerator

template = ReportTemplate(
    cover_image_path=Path("mi_portada.png"),
)

generator = ReportGenerator("reporte.pdf", template=template)
generator.build(
    title="Mi Reporte",
    summary="Contenido del reporte...",
    dataframe=df
)
```

## Cómo funciona

1. La imagen se escala automáticamente para ajustarse a la página
2. Se mantiene la relación de aspecto original
3. La imagen se centra en la página
4. Se añade un salto de página después de la portada

## Formatos soportados

| Formato | Extensión | Recomendado |
|---------|-----------|-------------|
| PNG | `.png` | ✅ Sí |
| JPEG | `.jpg`, `.jpeg` | ✅ Sí |
| GIF | `.gif` | ⚠️ Limitado |

!!! tip "Recomendación"
    Usa imágenes PNG de alta resolución (300 DPI) para mejores resultados de impresión.

## Dimensiones recomendadas

Para tamaño carta (Letter):

- **Ancho**: 2550 px (8.5" × 300 DPI)
- **Alto**: 3300 px (11" × 300 DPI)

Para tamaño A4:

- **Ancho**: 2480 px (210mm × 300 DPI)
- **Alto**: 3508 px (297mm × 300 DPI)

## Ejemplo completo

```python
from pathlib import Path
import pandas as pd
from qry_doc import ReportTemplate, ReportGenerator

# Datos de ejemplo
df = pd.DataFrame({
    'producto': ['Laptop', 'Mouse', 'Teclado'],
    'ventas': [1500, 800, 600]
})

# Template con portada
template = ReportTemplate(
    cover_image_path=Path("public/portada.png"),
    primary_color="#1a1a2e",
)

# Generar reporte
generator = ReportGenerator("reporte_con_portada.pdf", template=template)
generator.build(
    title="Informe de Ventas Q4 2024",
    summary="""
    Este informe presenta el análisis de ventas del cuarto trimestre.
    
    Puntos destacados:
    • Crecimiento del 15% vs Q3
    • Laptop Pro lidera las ventas
    """,
    dataframe=df
)

print("✅ Reporte generado con portada")
```

## Manejo de errores

Si la imagen de portada no existe o es inválida, se lanza un `ValidationError`:

```python
from qry_doc.exceptions import ValidationError

try:
    generator.build(...)
except ValidationError as e:
    print(f"Error: {e.user_message}")
```

!!! warning "Validación de rutas"
    qry-doc valida que la imagen exista antes de generar el PDF.
    Si la ruta es inválida, recibirás un error descriptivo.

## Combinación con secciones

Puedes usar portadas junto con el sistema de secciones:

```python
from qry_doc import SectionType, SectionConfig

sections = [
    SectionConfig(SectionType.COVER),    # Portada
    SectionConfig(SectionType.SUMMARY),  # Resumen
    SectionConfig(SectionType.DATA),     # Datos
]

template = ReportTemplate(
    cover_image_path=Path("portada.png"),
    sections=sections,
)
```

## Ver también

- [Sistema de Secciones](sections.md)
- [ReportTemplate API](../api/report-template.md)
