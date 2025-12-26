# Ejemplos qry-doc v0.1.3

Esta carpeta contiene ejemplos que demuestran las nuevas características de **qry-doc v0.1.3**.

## 🆕 Nuevas Características

| Característica | Descripción |
|----------------|-------------|
| **Portada** | Imagen de portada a página completa |
| **Footer Logo** | Logo en pie de página (default o personalizado) |
| **Fuentes Custom** | Soporte para fuentes TTF/OTF |
| **Secciones** | Sistema de secciones personalizables |

## 📁 Lista de Ejemplos

### 01_portada_basica.py
Demuestra cómo agregar una imagen de portada a los reportes PDF.

```python
template = ReportTemplate(
    cover_image_path=Path("public/portada.png"),
)
```

### 02_footer_logo.py
Muestra todas las opciones de configuración del logo en el pie de página:
- Logo por defecto del paquete
- Logo personalizado
- Diferentes posiciones (derecha, izquierda, centro)
- Dimensiones personalizables
- Desactivación del logo

```python
template = ReportTemplate(
    footer_logo_path=Path("mi_logo.png"),
    footer_logo_position=LogoPosition.BOTTOM_RIGHT,
    footer_logo_width=50.0,
    footer_logo_height=25.0,
)
```

### 03_fuentes_custom.py
Demuestra el uso de fuentes personalizadas TTF/OTF:
- Fuentes para títulos
- Fuentes para cuerpo
- Fallback automático a Helvetica

```python
template = ReportTemplate(
    custom_title_font_path=Path("fonts/Montserrat-Bold.ttf"),
    custom_body_font_path=Path("fonts/OpenSans-Regular.ttf"),
)
```

### 04_secciones.py
Muestra el sistema de secciones personalizables:
- Orden personalizado de secciones
- Secciones habilitadas/deshabilitadas
- Contenido CUSTOM arbitrario

```python
sections = [
    SectionConfig(SectionType.COVER),
    SectionConfig(SectionType.SUMMARY),
    SectionConfig(SectionType.CUSTOM, custom_content="Mi contenido"),
    SectionConfig(SectionType.DATA),
]

template = ReportTemplate(sections=sections)
```

### 05_reporte_completo.py
**Ejemplo completo** que combina todas las características:
- ✅ Portada personalizada
- ✅ Logo en footer
- ✅ Sistema de secciones
- ✅ Múltiples secciones CUSTOM
- ✅ Colores corporativos

## 🚀 Cómo Ejecutar

```bash
# Desde la raíz del proyecto qry-proyect
cd qry-proyect

# Ejecutar un ejemplo específico
.venv/bin/python examples/v0.1.3/01_portada_basica.py

# Ejecutar todos los ejemplos
for f in examples/v0.1.3/*.py; do .venv/bin/python "$f"; done
```

## 📂 Archivos Necesarios

Asegúrate de tener estos archivos:

```
qry-proyect/
├── public/
│   ├── portada.png      # Imagen de portada
│   └── logo_op.png      # Logo personalizado
├── examples/
│   └── data/
│       └── ventas.csv   # Datos de ejemplo
└── fonts/               # (Opcional) Fuentes TTF/OTF
    ├── Montserrat-Bold.ttf
    └── OpenSans-Regular.ttf
```

## 📤 Salida

Los PDFs generados se guardan en:

```
output/
├── 01_reporte_con_portada.pdf
├── footer_logos/
│   ├── 02a_logo_default.pdf
│   ├── 02b_logo_custom.pdf
│   └── ...
├── fuentes/
│   ├── 03a_fuentes_default.pdf
│   └── ...
├── secciones/
│   ├── 04a_orden_default.pdf
│   └── ...
└── 05_reporte_profesional.pdf
```

## 📚 Documentación

Para más información, consulta:
- [README principal](../../README.md)
- [Documentación de qry-doc](https://github.com/danro-dev/qry-doc)
- [Ejemplos legacy v0.1.0](../legacy/v0.1.0/)
