# Design Document

## Overview

Este diseño describe la arquitectura para reorganizar los ejemplos del proyecto y crear una documentación web profesional usando MkDocs Material. El objetivo es proporcionar una experiencia de documentación moderna y ejemplos claros para todas las funcionalidades de qry-doc v0.1.3.

## Architecture

```
qry-proyect/
├── docs/                          # Fuente de documentación MkDocs
│   ├── index.md                   # Página principal
│   ├── getting-started/
│   │   ├── installation.md
│   │   └── quickstart.md
│   ├── guides/
│   │   ├── cover-pages.md
│   │   ├── footer-logos.md
│   │   ├── custom-fonts.md
│   │   └── sections.md
│   ├── api/
│   │   ├── qrydoc.md
│   │   ├── report-template.md
│   │   └── types.md
│   ├── changelog.md
│   └── assets/
│       └── logo.png
├── examples/
│   ├── legacy/
│   │   └── v0.1.0/               # Ejemplos antiguos
│   ├── v0.1.3/                   # Nuevos ejemplos
│   │   ├── 01_portada_basica.py
│   │   ├── 02_footer_logo.py
│   │   ├── 03_fuentes_custom.py
│   │   ├── 04_secciones.py
│   │   ├── 05_reporte_completo.py
│   │   └── README.md
│   └── data/                     # Datos compartidos
├── mkdocs.yml                    # Configuración MkDocs
└── site/                         # Sitio generado (gitignore)
```

## Components and Interfaces

### MkDocs Configuration

```yaml
site_name: qry-doc Documentation
theme:
  name: material
  logo: assets/logo.png
  palette:
    primary: indigo
nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quickstart.md
  - Guides:
    - Cover Pages: guides/cover-pages.md
    - Footer Logos: guides/footer-logos.md
    - Custom Fonts: guides/custom-fonts.md
    - Sections: guides/sections.md
  - API Reference:
    - QryDoc: api/qrydoc.md
    - ReportTemplate: api/report-template.md
    - Types: api/types.md
  - Changelog: changelog.md
```

### Example Structure

Cada ejemplo seguirá esta estructura:
1. Docstring explicativo
2. Imports necesarios
3. Configuración de datos de prueba
4. Demostración de la funcionalidad
5. Generación de output en `output/`

## Data Models

No aplica - este spec es principalmente sobre organización de archivos y documentación.

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system.*

No hay propiedades formales para este spec ya que es principalmente documentación y ejemplos.

## Error Handling

- Si MkDocs no está instalado, mostrar instrucciones de instalación
- Si los ejemplos fallan, mostrar mensajes de error descriptivos
- Si faltan archivos de assets, usar placeholders o mostrar advertencias

## Testing Strategy

### Unit Tests
- Verificar que los ejemplos se ejecutan sin errores
- Verificar que los PDFs se generan correctamente

### Manual Testing
- Revisar que la documentación se renderiza correctamente
- Verificar navegación y enlaces
- Comprobar que los ejemplos de código funcionan
