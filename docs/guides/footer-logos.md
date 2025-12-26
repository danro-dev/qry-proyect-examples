# Logo en Pie de Página

<span class="version-badge new">v0.1.3</span>

qry-doc incluye un sistema flexible de logos en el pie de página que permite usar el logo por defecto del paquete o uno personalizado.

## Logo por defecto

Por defecto, qry-doc muestra su logo en la esquina inferior derecha de cada página:

```python
from qry_doc import ReportTemplate

# El logo por defecto está habilitado automáticamente
template = ReportTemplate()
```

## Logo personalizado

Puedes usar tu propio logo:

```python
from pathlib import Path
from qry_doc import ReportTemplate

template = ReportTemplate(
    footer_logo_path=Path("mi_logo.png"),
)
```

## Posiciones disponibles

Usa `LogoPosition` para controlar la ubicación:

```python
from qry_doc import ReportTemplate, LogoPosition

# Esquina inferior derecha (default)
template = ReportTemplate(
    footer_logo_position=LogoPosition.BOTTOM_RIGHT,
)

# Esquina inferior izquierda
template = ReportTemplate(
    footer_logo_position=LogoPosition.BOTTOM_LEFT,
)

# Centro inferior
template = ReportTemplate(
    footer_logo_position=LogoPosition.BOTTOM_CENTER,
)
```

## Dimensiones personalizadas

Ajusta el tamaño del logo:

```python
template = ReportTemplate(
    footer_logo_width=60.0,   # Ancho en puntos
    footer_logo_height=30.0,  # Alto en puntos
)
```

!!! info "Unidades"
    Las dimensiones están en puntos (1 punto = 1/72 pulgadas).
    
    - 72 puntos = 1 pulgada
    - 28.35 puntos ≈ 1 cm

## Desactivar el logo

Si no quieres mostrar ningún logo:

```python
template = ReportTemplate(
    footer_logo_enabled=False,
)
```

## Referencia de parámetros

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `footer_logo_path` | `Path \| None` | `None` | Ruta al logo personalizado |
| `footer_logo_enabled` | `bool` | `True` | Activar/desactivar logo |
| `footer_logo_position` | `LogoPosition` | `BOTTOM_RIGHT` | Posición del logo |
| `footer_logo_width` | `float` | `40.0` | Ancho en puntos |
| `footer_logo_height` | `float` | `20.0` | Alto en puntos |

## Ejemplo completo

```python
from pathlib import Path
import pandas as pd
from qry_doc import ReportTemplate, ReportGenerator, LogoPosition

# Datos
df = pd.DataFrame({'col': [1, 2, 3]})

# Template con logo personalizado
template = ReportTemplate(
    footer_logo_path=Path("public/mi_marca.png"),
    footer_logo_position=LogoPosition.BOTTOM_LEFT,
    footer_logo_width=50.0,
    footer_logo_height=25.0,
    primary_color="#e74c3c",
)

# Generar
generator = ReportGenerator("reporte.pdf", template=template)
generator.build(
    title="Mi Reporte",
    summary="Contenido...",
    dataframe=df
)
```

## Manejo de errores

Si el logo personalizado no existe, qry-doc muestra una advertencia en el log y continúa sin el logo:

```
WARNING: Footer logo not found: mi_logo.png. Skipping logo.
```

!!! tip "Graceful degradation"
    El reporte se genera correctamente aunque el logo no exista.
    Solo se omite el logo del pie de página.

## Formatos soportados

- PNG (recomendado, soporta transparencia)
- JPEG
- GIF

## Ver también

- [LogoPosition API](../api/types.md#logoposition)
- [ReportTemplate API](../api/report-template.md)
