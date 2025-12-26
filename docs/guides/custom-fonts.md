# Fuentes Personalizadas

<span class="version-badge new">v0.1.3</span>

qry-doc soporta fuentes TrueType (.ttf) y OpenType (.otf) para personalizar la tipografía de tus reportes.

## Uso básico

```python
from pathlib import Path
from qry_doc import ReportTemplate

template = ReportTemplate(
    custom_title_font_path=Path("fonts/Montserrat-Bold.ttf"),
    custom_body_font_path=Path("fonts/OpenSans-Regular.ttf"),
)
```

## Fuentes por defecto

Sin configuración personalizada, qry-doc usa:

| Elemento | Fuente |
|----------|--------|
| Títulos | Helvetica-Bold |
| Cuerpo | Helvetica |

## Obtener fuentes

Puedes descargar fuentes gratuitas de:

- [Google Fonts](https://fonts.google.com/) - Gran colección gratuita
- [Font Squirrel](https://www.fontsquirrel.com/) - Fuentes libres de licencia
- [DaFont](https://www.dafont.com/) - Fuentes decorativas

!!! tip "Google Fonts"
    Google Fonts ofrece fuentes de alta calidad y licencia libre.
    Descarga los archivos TTF y colócalos en una carpeta `fonts/`.

## Formatos soportados

| Formato | Extensión | Soporte |
|---------|-----------|---------|
| TrueType | `.ttf` | ✅ Completo |
| OpenType | `.otf` | ✅ Completo |
| Web Open Font | `.woff` | ❌ No soportado |

## Fallback automático

Si una fuente no existe o es inválida, qry-doc usa Helvetica automáticamente:

```python
# Si la fuente no existe, usa Helvetica sin errores
template = ReportTemplate(
    custom_title_font_path=Path("fuente_inexistente.ttf"),
)
```

Se registra una advertencia en el log:

```
WARNING: Font not found: fuente_inexistente.ttf. Using default font.
```

## Ejemplo completo

```python
from pathlib import Path
import pandas as pd
from qry_doc import ReportTemplate, ReportGenerator

# Verificar que las fuentes existen
fonts_dir = Path("fonts")
title_font = fonts_dir / "Montserrat-Bold.ttf"
body_font = fonts_dir / "OpenSans-Regular.ttf"

# Crear template
template = ReportTemplate(
    custom_title_font_path=title_font if title_font.exists() else None,
    custom_body_font_path=body_font if body_font.exists() else None,
    primary_color="#2c3e50",
)

# Datos
df = pd.DataFrame({
    'producto': ['A', 'B', 'C'],
    'ventas': [100, 200, 150]
})

# Generar reporte
generator = ReportGenerator("reporte_fuentes.pdf", template=template)
generator.build(
    title="Reporte con Fuentes Personalizadas",
    summary="Este reporte usa tipografía personalizada.",
    dataframe=df
)
```

## Estructura de carpetas recomendada

```
mi_proyecto/
├── fonts/
│   ├── Montserrat-Bold.ttf
│   ├── Montserrat-Regular.ttf
│   ├── OpenSans-Bold.ttf
│   └── OpenSans-Regular.ttf
├── output/
└── main.py
```

## Solo fuente de títulos

Puedes personalizar solo los títulos:

```python
template = ReportTemplate(
    custom_title_font_path=Path("fonts/Montserrat-Bold.ttf"),
    # body_font usa Helvetica por defecto
)
```

## Solo fuente de cuerpo

O solo el cuerpo del texto:

```python
template = ReportTemplate(
    # title_font usa Helvetica-Bold por defecto
    custom_body_font_path=Path("fonts/OpenSans-Regular.ttf"),
)
```

## Validación de fuentes

qry-doc valida las fuentes antes de usarlas:

1. Verifica que el archivo existe
2. Verifica que la extensión es `.ttf` o `.otf`
3. Intenta registrar la fuente con ReportLab
4. Si falla, usa Helvetica como fallback

## Referencia de parámetros

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `custom_title_font_path` | `Path \| None` | `None` | Fuente para títulos |
| `custom_body_font_path` | `Path \| None` | `None` | Fuente para cuerpo |
| `title_font` | `str` | `"Helvetica-Bold"` | Nombre de fuente de títulos |
| `body_font` | `str` | `"Helvetica"` | Nombre de fuente de cuerpo |

## Ver también

- [ReportTemplate API](../api/report-template.md)
- [AssetManager API](../api/types.md#assetmanager)
