# Sistema de Secciones

<span class="version-badge new">v0.1.3</span>

El sistema de secciones permite controlar el orden y contenido de las diferentes partes de un reporte PDF.

## Tipos de secciones

| Tipo | Descripción |
|------|-------------|
| `COVER` | Portada con imagen a página completa |
| `SUMMARY` | Resumen ejecutivo con título |
| `DATA` | Tabla de datos (DataFrame) |
| `CHART` | Gráfico o visualización |
| `CUSTOM` | Contenido personalizado arbitrario |

## Uso básico

```python
from qry_doc import ReportTemplate, SectionType, SectionConfig

sections = [
    SectionConfig(SectionType.SUMMARY),
    SectionConfig(SectionType.DATA),
]

template = ReportTemplate(sections=sections)
```

## Orden por defecto

Sin configuración de secciones, qry-doc usa:

1. SUMMARY (Resumen)
2. CHART (Gráfico)
3. DATA (Datos)

## Personalizar el orden

```python
# Datos primero, luego resumen
sections = [
    SectionConfig(SectionType.DATA),
    SectionConfig(SectionType.SUMMARY),
]
```

## Secciones personalizadas (CUSTOM)

Añade contenido arbitrario:

```python
sections = [
    SectionConfig(SectionType.SUMMARY),
    SectionConfig(
        SectionType.CUSTOM,
        custom_content="""
        METODOLOGÍA
        
        Este análisis fue realizado utilizando técnicas avanzadas
        de procesamiento de datos con Python.
        """
    ),
    SectionConfig(SectionType.DATA),
]
```

## Desactivar secciones

```python
sections = [
    SectionConfig(SectionType.SUMMARY),
    SectionConfig(SectionType.DATA, enabled=False),  # No se muestra
]
```

## Ejemplo completo

```python
from pathlib import Path
import pandas as pd
from qry_doc import (
    ReportTemplate, 
    ReportGenerator,
    SectionType, 
    SectionConfig
)

# Datos
df = pd.DataFrame({
    'producto': ['Laptop', 'Mouse', 'Teclado'],
    'ventas': [1500, 800, 600]
})

# Definir estructura del reporte
sections = [
    # 1. Portada
    SectionConfig(SectionType.COVER),
    
    # 2. Resumen ejecutivo
    SectionConfig(SectionType.SUMMARY),
    
    # 3. Índice personalizado
    SectionConfig(
        SectionType.CUSTOM,
        custom_content="""
        CONTENIDO
        
        1. Resumen Ejecutivo
        2. Análisis de Datos
        3. Conclusiones
        """
    ),
    
    # 4. Tabla de datos
    SectionConfig(SectionType.DATA),
    
    # 5. Conclusiones
    SectionConfig(
        SectionType.CUSTOM,
        custom_content="""
        CONCLUSIONES
        
        • Las ventas muestran tendencia positiva
        • Laptop lidera el mercado
        • Se recomienda expandir la línea de productos
        """
    ),
]

# Template
template = ReportTemplate(
    cover_image_path=Path("public/portada.png"),
    sections=sections,
    primary_color="#1a1a2e",
)

# Generar con build_with_sections
generator = ReportGenerator("reporte_secciones.pdf", template=template)
generator.build_with_sections(
    title="Informe de Ventas 2024",
    summary="Análisis del desempeño comercial anual.",
    dataframe=df
)
```

## build() vs build_with_sections()

| Método | Uso |
|--------|-----|
| `build()` | Orden fijo: título, resumen, gráfico, datos |
| `build_with_sections()` | Usa el orden definido en `sections` |

!!! tip "Recomendación"
    Usa `build_with_sections()` cuando configures secciones personalizadas.

## Múltiples secciones CUSTOM

Puedes tener varias secciones personalizadas:

```python
sections = [
    SectionConfig(SectionType.SUMMARY),
    SectionConfig(SectionType.CUSTOM, custom_content="Sección 1..."),
    SectionConfig(SectionType.DATA),
    SectionConfig(SectionType.CUSTOM, custom_content="Sección 2..."),
    SectionConfig(SectionType.CUSTOM, custom_content="Sección 3..."),
]
```

## Secciones condicionales

```python
incluir_datos = True

sections = [
    SectionConfig(SectionType.SUMMARY),
]

if incluir_datos:
    sections.append(SectionConfig(SectionType.DATA))
```

## Referencia de SectionConfig

```python
@dataclass
class SectionConfig:
    section_type: SectionType    # Tipo de sección
    enabled: bool = True         # Si está activa
    custom_content: str | None   # Contenido para CUSTOM
```

## Ver también

- [SectionType API](../api/types.md#sectiontype)
- [SectionConfig API](../api/types.md#sectionconfig)
- [Portadas](cover-pages.md)
