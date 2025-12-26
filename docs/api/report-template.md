# ReportTemplate

Configuración para personalizar el estilo de reportes PDF.

## Importación

```python
from qry_doc import ReportTemplate
```

## Constructor

```python
@dataclass
class ReportTemplate:
    # Configuración básica
    logo_path: Path | None = None
    primary_color: str = "#1a1a2e"
    title_font: str = "Helvetica-Bold"
    body_font: str = "Helvetica"
    
    # Layout de página
    page_size: tuple[float, float] = letter
    margin_top: float = 72.0
    margin_bottom: float = 72.0
    margin_left: float = 72.0
    margin_right: float = 72.0
    header_height: float = 50.0
    footer_height: float = 30.0
    
    # Portada (v0.1.3+)
    cover_image_path: Path | None = None
    
    # Footer logo (v0.1.3+)
    footer_logo_path: Path | None = None
    footer_logo_enabled: bool = True
    footer_logo_position: LogoPosition = LogoPosition.BOTTOM_RIGHT
    footer_logo_width: float = 40.0
    footer_logo_height: float = 20.0
    
    # Fuentes personalizadas (v0.1.3+)
    custom_title_font_path: Path | None = None
    custom_body_font_path: Path | None = None
    
    # Secciones (v0.1.3+)
    sections: list[SectionConfig] = field(default_factory=list)
```

## Parámetros

### Configuración básica

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `logo_path` | `Path \| None` | `None` | Logo para el header |
| `primary_color` | `str` | `"#1a1a2e"` | Color principal (hex) |
| `title_font` | `str` | `"Helvetica-Bold"` | Fuente de títulos |
| `body_font` | `str` | `"Helvetica"` | Fuente de cuerpo |

### Layout de página

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `page_size` | `tuple` | `letter` | Tamaño de página |
| `margin_top` | `float` | `72.0` | Margen superior (puntos) |
| `margin_bottom` | `float` | `72.0` | Margen inferior |
| `margin_left` | `float` | `72.0` | Margen izquierdo |
| `margin_right` | `float` | `72.0` | Margen derecho |
| `header_height` | `float` | `50.0` | Altura del header |
| `footer_height` | `float` | `30.0` | Altura del footer |

### Portada <span class="version-badge new">v0.1.3</span>

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `cover_image_path` | `Path \| None` | `None` | Imagen de portada |

### Footer logo <span class="version-badge new">v0.1.3</span>

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `footer_logo_path` | `Path \| None` | `None` | Logo personalizado |
| `footer_logo_enabled` | `bool` | `True` | Activar logo |
| `footer_logo_position` | `LogoPosition` | `BOTTOM_RIGHT` | Posición |
| `footer_logo_width` | `float` | `40.0` | Ancho (puntos) |
| `footer_logo_height` | `float` | `20.0` | Alto (puntos) |

### Fuentes personalizadas <span class="version-badge new">v0.1.3</span>

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `custom_title_font_path` | `Path \| None` | `None` | Fuente TTF/OTF títulos |
| `custom_body_font_path` | `Path \| None` | `None` | Fuente TTF/OTF cuerpo |

### Secciones <span class="version-badge new">v0.1.3</span>

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `sections` | `list[SectionConfig]` | `[]` | Lista de secciones |

## Propiedades

### primary_color_obj

```python
@property
def primary_color_obj(self) -> Color
```

Retorna el color primario como objeto ReportLab Color.

### page_width / page_height

```python
@property
def page_width(self) -> float

@property
def page_height(self) -> float
```

Dimensiones de la página en puntos.

### content_width / content_height

```python
@property
def content_width(self) -> float

@property
def content_height(self) -> float
```

Área disponible para contenido (página menos márgenes).

## Métodos

### get_footer_logo_path() <span class="version-badge new">v0.1.3</span>

```python
def get_footer_logo_path(self) -> Path | None
```

Retorna la ruta al logo del footer (personalizado o default).

### register_custom_fonts() <span class="version-badge new">v0.1.3</span>

```python
def register_custom_fonts(self) -> tuple[str, str]
```

Registra fuentes personalizadas y retorna los nombres a usar.

### draw_header() / draw_footer()

```python
def draw_header(self, canvas: Any, doc: Any) -> None
def draw_footer(self, canvas: Any, doc: Any) -> None
```

Dibuja header/footer en el canvas. Puede sobrescribirse.

### set_header_callback() / set_footer_callback()

```python
def set_header_callback(self, callback: Callable) -> None
def set_footer_callback(self, callback: Callable) -> None
```

Establece callbacks personalizados para header/footer.

## Templates predefinidos

```python
from qry_doc import (
    DEFAULT_TEMPLATE,    # Estilo profesional estándar
    CORPORATE_TEMPLATE,  # Azul corporativo
    MINIMAL_TEMPLATE,    # Minimalista
    A4_TEMPLATE,         # Tamaño A4
)
```

## Ejemplos

### Template básico

```python
template = ReportTemplate(
    primary_color="#003366",
)
```

### Template completo v0.1.3

```python
from pathlib import Path
from qry_doc import (
    ReportTemplate,
    LogoPosition,
    SectionType,
    SectionConfig,
)

template = ReportTemplate(
    # Portada
    cover_image_path=Path("portada.png"),
    
    # Footer logo
    footer_logo_path=Path("mi_logo.png"),
    footer_logo_position=LogoPosition.BOTTOM_RIGHT,
    footer_logo_width=50.0,
    
    # Fuentes
    custom_title_font_path=Path("fonts/Montserrat-Bold.ttf"),
    custom_body_font_path=Path("fonts/OpenSans-Regular.ttf"),
    
    # Secciones
    sections=[
        SectionConfig(SectionType.COVER),
        SectionConfig(SectionType.SUMMARY),
        SectionConfig(SectionType.DATA),
    ],
    
    # Colores
    primary_color="#1a1a2e",
)
```

## Ver también

- [Guía de Portadas](../guides/cover-pages.md)
- [Guía de Footer Logos](../guides/footer-logos.md)
- [Guía de Fuentes](../guides/custom-fonts.md)
- [Guía de Secciones](../guides/sections.md)
- [Tipos y Enums](types.md)
