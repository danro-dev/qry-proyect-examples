# Changelog

Todos los cambios notables de qry-doc serán documentados en esta página.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [0.1.5] - 2025-12-26

### Añadido

#### 🤖 AIBuilder con LangChain

Nuevo agente inteligente para preparación de datos y sugerencias de visualizaciones.

```python
from qry_doc import QryDoc

qry = QryDoc("datos.csv", llm=llm)
ai = qry.ai_builder

# Obtener resumen estructurado
summary = ai.get_data_summary()

# Sugerencias de gráficas
suggestions = ai.suggest_charts("análisis de ventas")

# Preparar datos para reporte
report_data = ai.prepare_report_data("reporte trimestral")
```

- Integración con LangChain para análisis inteligente
- Método `get_data_summary()` para resumen estructurado de datos
- Método `suggest_charts()` para sugerencias de visualizaciones
- Método `prepare_report_data()` para preparación de reportes
- Método `validate_query()` para validar consultas
- Contexto de conversación mantenido
- [Ver guía completa](guides/ai-builder.md)

#### 🎯 CoverBuilder para portadas dinámicas

API fluida para crear portadas personalizadas con posicionamiento preciso.

```python
cover = (
    qry.create_cover()
    .set_title("Reporte Anual 2024", font_size=48, color="#003366")
    .set_subtitle("Análisis de Ventas")
    .set_date(datetime.now())
    .set_author("Equipo de Datos")
    .set_background_color("#F5F5F5")
)
```

- Métodos fluidos: `set_title()`, `set_subtitle()`, `set_date()`, `set_author()`
- Posicionamiento exacto en puntos
- Soporte para imágenes de fondo con opacidad
- Textos personalizados con `add_custom_text()`
- [Ver guía completa](guides/cover-builder.md)

#### 🏗️ TemplateBuilder para templates personalizados

Constructor fluido para configurar templates de reportes.

```python
template = (
    qry.create_template()
    .with_colors(primary="#003366", secondary="#0066CC")
    .with_fonts(title_font="Helvetica-Bold", body_font="Helvetica")
    .with_margins(top=72, bottom=72)
    .with_charts(charts)
)
```

- API fluida encadenable
- Método `from_preset()` para iniciar desde un preset
- Soporte para múltiples gráficas con `with_charts()`
- [Ver guía completa](guides/template-builder.md)

#### 📊 Soporte para múltiples gráficas

Incluye hasta 10 gráficas en un solo reporte con ChartConfig.

```python
from qry_doc import ChartConfig

charts = [
    ChartConfig(chart_type='bar', title='Ventas por Región', group_by='region', value_column='total'),
    ChartConfig(chart_type='pie', title='Distribución', group_by='categoria', value_column='cantidad'),
    ChartConfig(chart_type='line', title='Tendencia', group_by='fecha', value_column='ventas'),
]

template = qry.create_template().with_charts(charts)
```

- Tipos soportados: `bar`, `barh`, `line`, `pie`, `scatter`, `area`
- Máximo 10 gráficas por reporte
- Validación automática de configuraciones
- [Ver guía completa](guides/chart-config.md)

#### 🏭 ReportPresets por industria

Presets predefinidos optimizados para diferentes industrias.

```python
from qry_doc import TemplateBuilder, ReportPresetType

template = TemplateBuilder.from_preset(ReportPresetType.FINANCIAL).build()
```

| Preset | Descripción | Color |
|--------|-------------|-------|
| `FINANCIAL` | Banca e inversiones | Azul (#003366) |
| `HEALTHCARE` | Salud y farmacéutica | Verde (#006666) |
| `TECHNOLOGY` | Software y TI | Púrpura (#5C2D91) |
| `RETAIL` | Comercio y ventas | Naranja (#E65100) |
| `MANUFACTURING` | Producción industrial | Gris (#455A64) |
| `CONSULTING` | Consultoría | Azul marino (#1A237E) |

- [Ver guía completa](guides/report-presets.md)

#### 🔧 Nuevos métodos en QryDoc

```python
# Nuevos métodos factory
cover = qry.create_cover()      # Retorna CoverBuilder
template = qry.create_template() # Retorna TemplateBuilder

# Nueva propiedad
ai = qry.ai_builder  # Retorna AIBuilder configurado

# Nuevo método de generación
qry.generate_report_with_builder(
    "reporte.pdf",
    cover=cover,
    template=template
)
```

#### 📦 Nuevos exports públicos

- `AIBuilder`, `DataSummary`, `ChartSuggestion`
- `CoverBuilder`, `CoverConfig`
- `TemplateBuilder`
- `ChartConfig`, `ChartTypeEnum`, `VALID_CHART_TYPES`
- `ReportPreset`, `ReportPresetType`
- `TextElement`, `TextAlignment`

#### 🔗 Dependencia opcional LangChain

```bash
# Instalar con soporte para AIBuilder
pip install "qry-doc[langchain]"
```

---

## [0.1.4] - 2025-12-26

### Mejorado

#### 🖼️ Portada a página completa

La imagen de portada ahora cubre toda la página sin márgenes.

- Usa el método Canvas de ReportLab para mayor flexibilidad
- La portada no muestra header ni footer
- Solucionado error "Flowable too large" con imágenes grandes

#### 🏷️ Logo del footer más grande

Tamaño por defecto aumentado significativamente para mejor visibilidad.

```python
# Nuevos valores por defecto
footer_logo_width: 120.0   # antes: 40.0
footer_logo_height: 60.0   # antes: 20.0
```

---

## [0.1.3] - 2025-12-25

### Añadido

#### 🖼️ Portada personalizada

Soporte para agregar una imagen de portada a página completa en los reportes PDF.

```python
template = ReportTemplate(
    cover_image_path=Path("mi_portada.png"),
)
```

- La imagen se escala automáticamente manteniendo la relación de aspecto
- Validación de rutas con mensajes de error descriptivos
- [Ver guía completa](guides/cover-pages.md)

#### 🏷️ Logo en pie de página

Sistema completo de logo en el footer con múltiples opciones.

```python
template = ReportTemplate(
    footer_logo_path=Path("mi_logo.png"),
    footer_logo_position=LogoPosition.BOTTOM_RIGHT,
    footer_logo_width=50.0,
    footer_logo_height=25.0,
)
```

- Logo por defecto incluido en el paquete
- Soporte para logo personalizado
- Posición configurable: `BOTTOM_RIGHT`, `BOTTOM_LEFT`, `BOTTOM_CENTER`
- Dimensiones personalizables
- Opción para desactivar completamente
- [Ver guía completa](guides/footer-logos.md)

#### ✏️ Fuentes personalizadas

Soporte para fuentes TrueType (.ttf) y OpenType (.otf).

```python
template = ReportTemplate(
    custom_title_font_path=Path("fonts/Montserrat-Bold.ttf"),
    custom_body_font_path=Path("fonts/OpenSans-Regular.ttf"),
)
```

- Fuentes separadas para títulos y cuerpo
- Fallback automático a Helvetica si la fuente es inválida
- Validación de extensiones
- [Ver guía completa](guides/custom-fonts.md)

#### 📑 Sistema de secciones

Control granular sobre la estructura del reporte.

```python
sections = [
    SectionConfig(SectionType.COVER),
    SectionConfig(SectionType.SUMMARY),
    SectionConfig(SectionType.CUSTOM, custom_content="..."),
    SectionConfig(SectionType.DATA),
]

template = ReportTemplate(sections=sections)
```

- Tipos: `COVER`, `SUMMARY`, `DATA`, `CHART`, `CUSTOM`
- Orden personalizable
- Secciones desactivables individualmente
- Contenido personalizado con `CUSTOM`
- Nuevo método `build_with_sections()`
- [Ver guía completa](guides/sections.md)

#### 🔧 AssetManager

Nueva clase para gestión de assets del paquete.

```python
from qry_doc import AssetManager

logo = AssetManager.get_default_logo_path()
is_valid, error = AssetManager.validate_image_path(path)
is_valid, error = AssetManager.validate_font_path(path)
```

#### 📦 Nuevos exports públicos

- `SectionType`
- `SectionConfig`
- `LogoPosition`
- `AssetManager`

### Mejorado

- Documentación completa de todas las nuevas funcionalidades
- 126 tests incluyendo property-based tests
- Mejor manejo de errores con mensajes descriptivos

---

## [0.1.0] - 2025-12-XX

### Añadido

- **QryDoc**: Clase principal (Facade) para interacción con datos
- **Consultas en lenguaje natural**: Integración con PandasAI
- **Exportación CSV**: Con encoding UTF-8 BOM para Excel
- **Generación de reportes PDF**: Con ReportLab/Platypus
- **ReportTemplate**: Configuración de estilos
- **Templates predefinidos**: DEFAULT, CORPORATE, MINIMAL, A4
- **Sanitización de errores**: Protección de información sensible
- **Soporte multi-LLM**: OpenAI, Anthropic, Google, etc.

### Características

- Consultas en español e inglés
- Visualizaciones automáticas con Matplotlib
- Tablas con ajuste automático de columnas
- Headers y footers personalizables
- Context manager para limpieza automática

---

## Próximas versiones

### Planificado

- [ ] Soporte para conexiones SQL (PostgreSQL, MySQL, SQLite)
- [ ] Caché de consultas para mejorar rendimiento
- [ ] Exportación a Excel (.xlsx)
- [ ] Más templates predefinidos
- [ ] CLI para uso desde terminal
- [ ] Integración con Jupyter notebooks

---

## Enlaces

- [Repositorio GitHub](https://github.com/danro-dev/qry-doc)
- [Reportar un bug](https://github.com/danro-dev/qry-doc/issues)
- [Solicitar feature](https://github.com/danro-dev/qry-doc/issues)
