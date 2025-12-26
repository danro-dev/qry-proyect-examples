# TemplateBuilder

<span class="version-badge new">v0.1.5</span>

TemplateBuilder proporciona una API fluida para construir templates de reportes PDF con configuración completa de colores, fuentes, márgenes, secciones y gráficas.

## Uso básico

```python
from qry_doc import QryDoc

qry = QryDoc("datos.csv", llm=llm)

# Crear template con API fluida
template = (
    qry.create_template()
    .with_colors(primary="#003366")
    .with_fonts(title_font="Helvetica-Bold")
    .with_margins(top=72, bottom=72)
)

# Generar reporte
qry.generate_report_with_builder(
    "reporte.pdf",
    template=template,
    title="Mi Reporte"
)
```

## Desde un preset

Inicia desde un preset de industria y personaliza:

```python
from qry_doc import TemplateBuilder, ReportPresetType

template = (
    TemplateBuilder.from_preset(ReportPresetType.FINANCIAL)
    .with_margins(top=100)  # Override solo lo necesario
    .build()
)
```

## Métodos disponibles

### with_colors()

Configura los colores del template.

```python
template.with_colors(
    primary="#003366",    # Color principal (headings, acentos)
    secondary="#0066CC"   # Color secundario (opcional)
)
```

### with_fonts()

Configura las fuentes.

```python
template.with_fonts(
    title_font="Helvetica-Bold",  # Fuente para títulos
    body_font="Helvetica"         # Fuente para cuerpo (default: igual que title)
)
```

### with_margins()

Configura los márgenes de página en puntos.

```python
template.with_margins(
    top=72,      # 1 pulgada
    bottom=72,
    left=72,
    right=72
)
```

!!! info "Conversión de unidades"
    - 1 pulgada = 72 puntos
    - 1 cm ≈ 28.35 puntos

### with_page_size()

Configura el tamaño de página.

```python
from reportlab.lib.pagesizes import letter, A4

template.with_page_size(letter)  # Default
template.with_page_size(A4)      # Tamaño europeo
```

### with_header()

Configura el encabezado.

```python
template.with_header(
    logo_path="logo.png",  # Logo del header
    height=50.0            # Altura en puntos
)
```

### with_footer()

Configura el pie de página.

```python
from qry_doc import LogoPosition

template.with_footer(
    logo_path="logo_footer.png",
    logo_position=LogoPosition.BOTTOM_RIGHT,
    logo_enabled=True,
    logo_width=40.0,
    logo_height=20.0,
    height=30.0
)
```

### with_sections()

Configura las secciones del reporte.

```python
from qry_doc import SectionConfig, SectionType

template.with_sections([
    SectionConfig(SectionType.COVER),
    SectionConfig(SectionType.SUMMARY),
    SectionConfig(SectionType.CHART),
    SectionConfig(SectionType.DATA),
    SectionConfig(SectionType.CUSTOM, custom_content="Notas adicionales..."),
])
```

### with_cover()

Configura una imagen de portada.

```python
template.with_cover("portada.png")
```

### with_custom_fonts()

Configura fuentes TTF/OTF personalizadas.

```python
template.with_custom_fonts(
    title_font_path="fonts/Montserrat-Bold.ttf",
    body_font_path="fonts/OpenSans-Regular.ttf"
)
```

### with_charts()

Configura múltiples gráficas (máximo 10).

```python
from qry_doc import ChartConfig

charts = [
    ChartConfig(chart_type='bar', title='Ventas', group_by='region', value_column='total'),
    ChartConfig(chart_type='pie', title='Distribución', group_by='categoria', value_column='cantidad'),
]

template.with_charts(charts)
```

### build()

Construye y retorna el ReportTemplate final.

```python
report_template = template.build()
```

## Ejemplo completo

```python
from qry_doc import (
    QryDoc,
    TemplateBuilder,
    ChartConfig,
    SectionConfig,
    SectionType,
    LogoPosition,
)

qry = QryDoc("ventas.csv", llm=llm)

# Definir gráficas
charts = [
    ChartConfig(
        chart_type='bar',
        title='Ventas por Región',
        group_by='region',
        value_column='total',
        color='#003366'
    ),
    ChartConfig(
        chart_type='pie',
        title='Distribución por Categoría',
        group_by='categoria',
        value_column='cantidad'
    ),
]

# Construir template completo
template = (
    qry.create_template()
    .with_colors(primary="#003366", secondary="#0066CC")
    .with_fonts(title_font="Helvetica-Bold", body_font="Helvetica")
    .with_margins(top=72, bottom=72, left=72, right=72)
    .with_header(logo_path="logo.png", height=50)
    .with_footer(
        logo_position=LogoPosition.BOTTOM_RIGHT,
        logo_width=120,
        logo_height=60
    )
    .with_sections([
        SectionConfig(SectionType.SUMMARY),
        SectionConfig(SectionType.CHART),
        SectionConfig(SectionType.DATA),
    ])
    .with_charts(charts)
)

# Generar reporte
qry.generate_report_with_builder(
    "reporte_completo.pdf",
    template=template,
    title="Análisis de Ventas Q4 2024"
)
```

## Validación

TemplateBuilder valida automáticamente:

- Colores en formato hex válido
- Márgenes no negativos
- Alturas no negativas
- Máximo 10 gráficas

```python
from qry_doc.exceptions import ValidationError

try:
    template.with_margins(top=-10)  # Error
except ValidationError as e:
    print(f"Error: {e.user_message}")
```

## Propiedades

```python
# Obtener configuración actual
config = template.config

# Obtener gráficas configuradas
charts = template.charts
```

## Ver también

- [ReportPresets](report-presets.md)
- [ChartConfig](chart-config.md)
- [CoverBuilder](cover-builder.md)
- [Sistema de Secciones](sections.md)
