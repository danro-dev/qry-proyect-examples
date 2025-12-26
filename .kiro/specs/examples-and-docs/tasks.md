# Implementation Plan: Examples and Documentation

## Overview

Este plan implementa la reorganización de ejemplos y la creación de documentación web profesional para qry-doc usando MkDocs Material.

## Tasks

- [x] 1. Reorganizar ejemplos existentes
  - [x] 1.1 Crear estructura de directorios para ejemplos versionados
    - Crear `examples/legacy/v0.1.0/`
    - Crear `examples/v0.1.3/`
    - _Requirements: 1.1, 1.2_
  - [x] 1.2 Mover ejemplos antiguos a legacy
    - Mover todos los archivos .py actuales a `legacy/v0.1.0/`
    - Mantener `data/` en ubicación compartida
    - _Requirements: 1.1, 1.3_

- [-] 2. Crear nuevos ejemplos de PDF v0.1.3
  - [x] 2.1 Crear ejemplo de portada básica
    - Usar `portada.png` de public/
    - Demostrar `cover_image_path`
    - _Requirements: 2.1_
  - [x] 2.2 Crear ejemplo de footer logo
    - Demostrar logo por defecto, personalizado y desactivado
    - Demostrar `LogoPosition`
    - _Requirements: 2.2_
  - [x] 2.3 Crear ejemplo de fuentes personalizadas
    - Demostrar `custom_title_font_path` y `custom_body_font_path`
    - _Requirements: 2.3_
  - [-] 2.4 Crear ejemplo de secciones
    - Demostrar `SectionType` y `SectionConfig`
    - Mostrar orden personalizado de secciones
    - _Requirements: 2.4_
  - [ ] 2.5 Crear ejemplo completo combinando todas las features
    - Portada + logo + fuentes + secciones
    - _Requirements: 2.5_
  - [ ] 2.6 Crear README para los nuevos ejemplos
    - Documentar cada ejemplo
    - _Requirements: 2.6_

- [ ] 3. Configurar MkDocs
  - [ ] 3.1 Agregar dependencias de MkDocs al proyecto
    - Agregar mkdocs y mkdocs-material a pyproject.toml
    - _Requirements: 5.2_
  - [ ] 3.2 Crear mkdocs.yml con configuración completa
    - Configurar tema Material
    - Configurar navegación
    - Configurar logo y colores
    - _Requirements: 3.1, 3.2, 5.1_

- [ ] 4. Crear documentación - Páginas principales
  - [ ] 4.1 Crear página de inicio (index.md)
    - Overview del proyecto
    - Features principales
    - _Requirements: 4.1_
  - [ ] 4.2 Crear guía de instalación
    - Instalación con pip y uv
    - Configuración de LLM
    - _Requirements: 4.2_
  - [ ] 4.3 Crear tutorial de inicio rápido
    - Ejemplo básico completo
    - _Requirements: 4.3_

- [ ] 5. Crear documentación - Guías de features
  - [ ] 5.1 Crear guía de portadas
    - Documentar cover_image_path
    - Ejemplos de código
    - _Requirements: 4.4_
  - [ ] 5.2 Crear guía de footer logos
    - Documentar todas las opciones de logo
    - Ejemplos de posiciones
    - _Requirements: 4.4_
  - [ ] 5.3 Crear guía de fuentes personalizadas
    - Documentar soporte TTF/OTF
    - Ejemplos de uso
    - _Requirements: 4.4_
  - [ ] 5.4 Crear guía de secciones
    - Documentar SectionType y SectionConfig
    - Ejemplos de personalización
    - _Requirements: 4.4_

- [ ] 6. Crear documentación - API Reference
  - [ ] 6.1 Documentar clase QryDoc
    - Métodos y propiedades
    - _Requirements: 4.5_
  - [ ] 6.2 Documentar ReportTemplate
    - Todos los parámetros
    - _Requirements: 4.5_
  - [ ] 6.3 Documentar tipos (SectionType, LogoPosition, etc.)
    - Enums y dataclasses
    - _Requirements: 4.5_

- [ ] 7. Crear changelog y assets
  - [ ] 7.1 Crear página de changelog
    - Historial de versiones
    - _Requirements: 4.6_
  - [ ] 7.2 Copiar assets (logo) a docs
    - _Requirements: 3.2_

- [ ] 8. Verificar y construir
  - [ ] 8.1 Ejecutar ejemplos para verificar que funcionan
    - _Requirements: 2.6_
  - [ ] 8.2 Construir sitio de documentación
    - Ejecutar mkdocs build
    - _Requirements: 5.3, 5.4_

## Notes

- MkDocs Material proporciona un tema profesional con búsqueda, navegación y responsive design
- Los ejemplos deben ser ejecutables de forma independiente
- La documentación debe ser clara y con ejemplos de código funcionales
