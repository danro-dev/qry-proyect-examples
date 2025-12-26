# Ejemplos v0.1.5

Esta carpeta contiene ejemplos de las nuevas funcionalidades introducidas en qry-doc v0.1.5.

## Nuevas funcionalidades

| Ejemplo | Descripción |
|---------|-------------|
| `01_cover_builder.py` | Portadas dinámicas con CoverBuilder |
| `02_template_builder.py` | Templates personalizados con TemplateBuilder |
| `03_report_presets.py` | Presets por industria |
| `04_chart_config.py` | Múltiples gráficas con ChartConfig |
| `05_ai_builder.py` | Preparación inteligente con AIBuilder |
| `06_ejemplo_completo.py` | Ejemplo completo combinando todas las funcionalidades |

## Requisitos

```bash
# Instalación básica
pip install qry-doc

# Con soporte para AIBuilder
pip install "qry-doc[langchain]"

# Con soporte para OpenAI
pip install "qry-doc[openai]"
```

## Ejecución

```bash
# Desde la raíz del proyecto
cd qry-proyect

# Ejecutar un ejemplo
python examples/v0.1.5/01_cover_builder.py
```

## Datos de ejemplo

Los ejemplos usan el archivo `examples/data/ventas.csv` que contiene datos de ventas ficticios.
