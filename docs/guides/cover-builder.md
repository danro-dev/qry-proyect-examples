# CoverBuilder

<span class="version-badge new">v0.1.5</span>

CoverBuilder proporciona una API fluida para crear portadas dinámicas con control preciso sobre posicionamiento, estilos y contenido.

## Uso básico

```python
from qry_doc import QryDoc
from datetime import datetime

qry = QryDoc("datos.csv", llm=llm)

# Crear portada con API fluida
cover = (
    qry.create_cover()
    .set_title("Reporte Anual 2024")
    .set_subtitle("Análisis de Ventas")
    .set_date(datetime.now())
    .set_author("Equipo de Datos")
)

# Generar reporte
qry.generate_report_with_builder(
    "reporte.pdf",
    cover=cover,
    title="Mi Reporte"
)
```

## Métodos disponibles

### set_title()

Configura el título principal de la portada.

```python
cover.set_title(
    text="Mi Título",
    font_size=48,           # Tamaño en puntos (default: 36)
    x=306.0,                # Posición X (default: centrado)
    y=500.0,                # Posición Y (default: tercio superior)
    color="#003366",        # Color hex (default: #000000)
    font_family="Helvetica-Bold",
    alignment=TextAlignment.CENTER
)
```

### set_subtitle()

Configura el subtítulo.

```python
cover.set_subtitle(
    text="Subtítulo del Reporte",
    font_size=24,           # Default: 24
    color="#666666",        # Default: #333333
)
```

### set_date()

Configura la fecha del reporte.

```python
from datetime import datetime

# Con datetime
cover.set_date(datetime.now(), format="%d de %B, %Y")

# Con string
cover.set_date("Diciembre 2024")
```

### set_author()

Configura el autor o equipo.

```python
cover.set_author("Departamento de Finanzas")
```

### add_custom_text()

Añade texto personalizado en cualquier posición.

```python
cover.add_custom_text(
    text="CONFIDENCIAL",
    x=306.0,
    y=750.0,
    font_size=12,
    color="#FF0000",
    alignment=TextAlignment.CENTER
)
```

### set_background_color()

Configura un color de fondo.

```python
cover.set_background_color("#F5F5F5")
```

### set_background_image()

Configura una imagen de fondo.

```python
cover.set_background_image(
    path="fondo.png",
    opacity=0.8  # 0.0 a 1.0
)
```

## Sistema de coordenadas

Las posiciones se especifican en puntos desde la esquina inferior izquierda:

```
┌─────────────────────────────┐
│                             │ y = 792 (top)
│                             │
│         (306, 500)          │ ← Título centrado
│            TÍTULO           │
│                             │
│         (306, 450)          │ ← Subtítulo
│          Subtítulo          │
│                             │
│                             │
│         (306, 150)          │ ← Fecha
│           Fecha             │
│         (306, 120)          │ ← Autor
│           Autor             │
│                             │
└─────────────────────────────┘
x = 0                    x = 612 (right)
```

!!! info "Tamaño de página Letter"
    - Ancho: 612 puntos (8.5 pulgadas)
    - Alto: 792 puntos (11 pulgadas)
    - Centro horizontal: 306 puntos

## Alineación de texto

```python
from qry_doc import TextAlignment

# Opciones disponibles
TextAlignment.LEFT    # Alineado a la izquierda
TextAlignment.CENTER  # Centrado
TextAlignment.RIGHT   # Alineado a la derecha
```

## Ejemplo completo

```python
from qry_doc import QryDoc, TextAlignment
from datetime import datetime

qry = QryDoc("ventas.csv", llm=llm)

cover = (
    qry.create_cover()
    # Título principal
    .set_title(
        "Informe Ejecutivo 2024",
        font_size=48,
        color="#1A237E",
        y=550.0
    )
    # Subtítulo
    .set_subtitle(
        "Análisis Integral de Resultados",
        font_size=28,
        color="#3949AB",
        y=490.0
    )
    # Marca de agua
    .add_custom_text(
        "CONFIDENCIAL",
        x=306.0,
        y=750.0,
        font_size=12,
        color="#FF0000",
        alignment=TextAlignment.CENTER
    )
    # Fecha y autor
    .set_date(datetime.now(), format="%B %Y")
    .set_author("División Corporativa")
    # Versión
    .add_custom_text(
        "Versión 1.0",
        x=540.0,
        y=50.0,
        font_size=10,
        color="#999999",
        alignment=TextAlignment.RIGHT
    )
    # Fondo
    .set_background_color("#FAFAFA")
)

qry.generate_report_with_builder(
    "informe_ejecutivo.pdf",
    cover=cover,
    title="Informe Ejecutivo"
)
```

## Validación

CoverBuilder valida automáticamente:

- `font_size` debe ser positivo
- `color` debe ser formato hex válido (#RRGGBB o #RGB)
- `opacity` debe estar entre 0.0 y 1.0

```python
from qry_doc.exceptions import ValidationError

try:
    cover.set_title("Test", font_size=-5)  # Error
except ValidationError as e:
    print(f"Error: {e.user_message}")
```

## Combinación con TemplateBuilder

```python
cover = qry.create_cover().set_title("Mi Reporte")

template = (
    qry.create_template()
    .with_colors("#003366")
    .with_charts(charts)
)

qry.generate_report_with_builder(
    "reporte.pdf",
    cover=cover,
    template=template
)
```

## Ver también

- [TemplateBuilder](template-builder.md)
- [Portadas con imagen](cover-pages.md)
- [TextElement API](../api/types.md#textelement)
