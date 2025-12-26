# Inicio Rápido

Esta guía te llevará desde cero hasta generar tu primer reporte PDF profesional en menos de 5 minutos.

## Prerrequisitos

- qry-doc instalado ([ver instalación](installation.md))
- API key de OpenAI (u otro proveedor LLM)
- Un archivo CSV con datos

## 1. Configurar el LLM

```python
import pandasai as pai
from pandasai_openai import OpenAI

# Configurar OpenAI
llm = OpenAI()  # Usa OPENAI_API_KEY del entorno
pai.config.set({"llm": llm})
```

## 2. Cargar datos

```python
from qry_doc import QryDoc

# Desde archivo CSV
qry = QryDoc("ventas.csv", llm=llm)

# O desde un DataFrame
import pandas as pd
df = pd.read_csv("ventas.csv")
qry = QryDoc(df, llm=llm)
```

## 3. Hacer preguntas

```python
# Pregunta simple
respuesta = qry.ask("¿Cuántos registros hay?")
print(respuesta)

# Análisis más complejo
tendencia = qry.ask("¿Cómo han evolucionado las ventas mes a mes?")
print(tendencia)
```

## 4. Generar un reporte PDF

```python
# Reporte básico
qry.generate_report(
    "Análisis de ventas del trimestre",
    "mi_reporte.pdf"
)
```

## 5. Personalizar el reporte

```python
from qry_doc import ReportTemplate

# Template personalizado
template = ReportTemplate(
    primary_color="#003366",
    title_font="Helvetica-Bold",
)

qry.generate_report(
    "Análisis de ventas",
    "reporte_personalizado.pdf",
    title="Informe Q4 2024",
    template=template
)
```

## Ejemplo completo

```python
"""
Ejemplo completo de qry-doc
"""
import pandasai as pai
from pandasai_openai import OpenAI
from qry_doc import QryDoc, ReportTemplate

# 1. Configurar LLM
llm = OpenAI()
pai.config.set({"llm": llm})

# 2. Cargar datos
qry = QryDoc("ventas.csv", llm=llm)

# 3. Explorar datos
print(f"Columnas: {qry.columns}")
print(f"Registros: {qry.shape[0]}")

# 4. Hacer preguntas
total = qry.ask("¿Cuál es el total de ventas?")
print(f"Total: {total}")

top_producto = qry.ask("¿Cuál es el producto más vendido?")
print(f"Top producto: {top_producto}")

# 5. Exportar a CSV
qry.extract_to_csv(
    "Top 10 productos por ventas",
    "top_productos.csv"
)

# 6. Generar reporte PDF
template = ReportTemplate(
    primary_color="#1a1a2e",
)

qry.generate_report(
    "Resumen ejecutivo de ventas Q4 2024",
    "reporte_ventas.pdf",
    title="Informe de Ventas",
    template=template
)

print("✅ Reporte generado: reporte_ventas.pdf")
```

## Características avanzadas (v0.1.3)

La versión 0.1.3 añade nuevas características para PDFs:

### Portada personalizada

```python
from pathlib import Path

template = ReportTemplate(
    cover_image_path=Path("mi_portada.png"),
)
```

### Logo en pie de página

```python
from qry_doc import LogoPosition

template = ReportTemplate(
    footer_logo_path=Path("mi_logo.png"),
    footer_logo_position=LogoPosition.BOTTOM_RIGHT,
)
```

### Sistema de secciones

```python
from qry_doc import SectionType, SectionConfig

sections = [
    SectionConfig(SectionType.COVER),
    SectionConfig(SectionType.SUMMARY),
    SectionConfig(SectionType.DATA),
]

template = ReportTemplate(sections=sections)
```

[Ver guías detalladas](../guides/cover-pages.md){ .md-button .md-button--primary }

## Siguiente paso

Explora las guías detalladas para cada característica:

- [Portadas](../guides/cover-pages.md)
- [Logo en Footer](../guides/footer-logos.md)
- [Fuentes Personalizadas](../guides/custom-fonts.md)
- [Sistema de Secciones](../guides/sections.md)
