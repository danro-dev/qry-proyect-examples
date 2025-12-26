# Tipos y Enums

Tipos auxiliares utilizados en qry-doc.

## SectionType <span class="version-badge new">v0.1.3</span>

Enum que define los tipos de secciones disponibles en un reporte.

### Importación

```python
from qry_doc import SectionType
```

### Valores

| Valor | Descripción |
|-------|-------------|
| `COVER` | Portada con imagen a página completa |
| `SUMMARY` | Resumen ejecutivo con título |
| `DATA` | DataFrame renderizado como tabla |
| `CHART` | Gráfico o visualización |
| `CUSTOM` | Contenido personalizado arbitrario |

### Ejemplo

```python
from qry_doc import SectionType, SectionConfig

sections = [
    SectionConfig(SectionType.COVER),
    SectionConfig(SectionType.SUMMARY),
    SectionConfig(SectionType.DATA),
]
```

---

## SectionConfig <span class="version-badge new">v0.1.3</span>

Dataclass para configurar una sección del reporte.

### Importación

```python
from qry_doc import SectionConfig
```

### Definición

```python
@dataclass
class SectionConfig:
    section_type: SectionType
    enabled: bool = True
    custom_content: str | None = None
```

### Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `section_type` | `SectionType` | - | Tipo de sección |
| `enabled` | `bool` | `True` | Si la sección está activa |
| `custom_content` | `str \| None` | `None` | Contenido para CUSTOM |

### Ejemplos

```python
# Sección básica
section = SectionConfig(SectionType.SUMMARY)

# Sección deshabilitada
section = SectionConfig(SectionType.DATA, enabled=False)

# Sección personalizada
section = SectionConfig(
    SectionType.CUSTOM,
    custom_content="Mi contenido personalizado..."
)
```

---

## LogoPosition <span class="version-badge new">v0.1.3</span>

Enum para posiciones del logo en el pie de página.

### Importación

```python
from qry_doc import LogoPosition
```

### Valores

| Valor | Descripción |
|-------|-------------|
| `BOTTOM_RIGHT` | Esquina inferior derecha (default) |
| `BOTTOM_LEFT` | Esquina inferior izquierda |
| `BOTTOM_CENTER` | Centro inferior |

### Ejemplo

```python
from qry_doc import ReportTemplate, LogoPosition

template = ReportTemplate(
    footer_logo_position=LogoPosition.BOTTOM_LEFT,
)
```

---

## AssetManager <span class="version-badge new">v0.1.3</span>

Clase para gestión de assets del paquete.

### Importación

```python
from qry_doc import AssetManager
```

### Métodos estáticos

#### get_default_logo_path()

```python
@staticmethod
def get_default_logo_path() -> Path | None
```

Retorna la ruta al logo por defecto del paquete.

```python
logo = AssetManager.get_default_logo_path()
print(logo)  # /path/to/qry_doc/assets/default_logo.png
```

#### validate_image_path()

```python
@staticmethod
def validate_image_path(path: Path) -> tuple[bool, str | None]
```

Valida que una ruta de imagen sea válida.

```python
is_valid, error = AssetManager.validate_image_path(Path("imagen.png"))
if not is_valid:
    print(f"Error: {error}")
```

#### validate_font_path()

```python
@staticmethod
def validate_font_path(path: Path) -> tuple[bool, str | None]
```

Valida que una ruta de fuente sea válida.

```python
is_valid, error = AssetManager.validate_font_path(Path("fuente.ttf"))
if not is_valid:
    print(f"Error: {error}")
```

---

## Excepciones

### QryDocError

Excepción base para todos los errores de qry-doc.

```python
from qry_doc import QryDocError
```

### QueryError

Error al interpretar o ejecutar una consulta.

```python
from qry_doc import QueryError
```

### ExportError

Error al exportar datos.

```python
from qry_doc import ExportError
```

### ReportError

Error al generar un reporte PDF.

```python
from qry_doc import ReportError
```

### DataSourceError

Error al cargar la fuente de datos.

```python
from qry_doc import DataSourceError
```

### ValidationError

Error de validación de entradas o recursos.

```python
from qry_doc import ValidationError
```

### Atributos comunes

Todas las excepciones incluyen:

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `user_message` | `str` | Mensaje amigable para el usuario |
| `internal_error` | `Exception \| None` | Excepción original |

```python
try:
    qry.ask("consulta")
except QueryError as e:
    print(f"Usuario: {e.user_message}")
    if e.internal_error:
        print(f"Debug: {e.internal_error}")
```

---

## PageSize

Alias de tipo para tamaños de página.

```python
PageSize = tuple[float, float]
```

### Tamaños predefinidos

```python
from reportlab.lib.pagesizes import letter, A4, legal

# Letter (8.5" x 11")
template = ReportTemplate(page_size=letter)

# A4 (210mm x 297mm)
template = ReportTemplate(page_size=A4)
```

## Ver también

- [ReportTemplate](report-template.md)
- [QryDoc](qrydoc.md)
