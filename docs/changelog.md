# Changelog

Todos los cambios notables de qry-doc serán documentados en esta página.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

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
