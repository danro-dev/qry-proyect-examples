# ChartConfig

<span class="version-badge new">v0.1.5</span>

ChartConfig permite configurar múltiples gráficas en un solo reporte PDF, con soporte para diferentes tipos de visualizaciones.

## Uso básico

```python
from qry_doc import ChartConfig

chart = ChartConfig(
    chart_type='bar',
    title='Ventas por Región',
    group_by='region',
    value_column='total'
)
```

## Parámetros

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `chart_type` | `str` | - | Tipo de gráfica (requerido) |
| `title` | `str` | - | Título de la gráfica (requerido) |
| `data_query` | `str` | `None` | Query para generar datos |
| `group_by` | `str` | `None` | Columna para agrupar |
| `value_column` | `str` | `None` | Columna de valores |
| `color` | `str` | `None` | Color hex (#RRGGBB) |
| `figsize` | `tuple` | `(10, 6)` | Tamaño en pulgadas |

## Tipos de gráficas

| Tipo | Descripción | Mejor para |
|------|-------------|------------|
| `bar` | Barras verticales | Comparar categorías (≤12) |
| `barh` | Barras horizontales | Muchas categorías (>12) |
| `line` | Líneas | Series temporales |
| `pie` | Pastel | Distribución (≤6 categorías) |
| `scatter` | Dispersión | Correlación entre variables |
| `area` | Área | Tendencias acumulativas |

## Ejemplos por tipo

### Gráfica de barras

```python
chart_bar = ChartConfig(
    chart_type='bar',
    title='Ventas por Región',
    group_by='region',
    value_column='total',
    color='#003366'
)
```

### Gráfica de pastel

```python
chart_pie = ChartConfig(
    chart_type='pie',
    title='Distribución por Categoría',
    group_by='categoria',
    value_column='cantidad',
    color='#E65100'
)
```

### Gráfica de líneas

```python
chart_line = ChartConfig(
    chart_type='line',
    title='Tendencia Mensual',
    group_by='mes',
    value_column='ventas',
    color='#006666'
)
```

### Gráfica de dispersión

```python
chart_scatter = ChartConfig(
    chart_type='scatter',
    title='Precio vs Cantidad',
    group_by='precio',
    value_column='cantidad',
    color='#5C2D91'
)
```

## Múltiples gráficas

Puedes incluir hasta 10 gráficas en un reporte:

```python
from qry_doc import QryDoc, ChartConfig

qry = QryDoc("ventas.csv", llm=llm)

charts = [
    ChartConfig(
        chart_type='bar',
        title='Ventas por Región',
        group_by='region',
        value_column='total',
        color='#003366'
    ),
    ChartConfig(
        chart_type='pie',
        title='Distribución por Categoría',
        group_by='categoria',
        value_column='cantidad',
        color='#E65100'
    ),
    ChartConfig(
        chart_type='line',
        title='Tendencia Mensual',
        group_by='mes',
        value_column='ventas',
        color='#006666'
    ),
]

template = qry.create_template().with_charts(charts)

qry.generate_report_with_builder(
    "reporte_multi_graficas.pdf",
    template=template,
    title="Análisis Completo"
)
```

!!! warning "Límite de gráficas"
    El máximo es 10 gráficas por reporte. Intentar añadir más generará un `ValidationError`.

## Tamaño personalizado

```python
# Gráfica más grande
chart_grande = ChartConfig(
    chart_type='bar',
    title='Gráfica Grande',
    group_by='region',
    value_column='total',
    figsize=(14, 8)  # Ancho x Alto en pulgadas
)

# Gráfica cuadrada (ideal para pie)
chart_cuadrada = ChartConfig(
    chart_type='pie',
    title='Distribución',
    group_by='categoria',
    value_column='cantidad',
    figsize=(8, 8)
)
```

## Validación

ChartConfig valida automáticamente:

- `chart_type` debe ser uno de los tipos soportados
- `title` no puede estar vacío
- `color` debe ser formato hex válido
- `figsize` debe tener dimensiones positivas

```python
# Validar manualmente
is_valid, error = chart.validate()
if not is_valid:
    print(f"Error: {error}")

# O usar el factory method que valida automáticamente
chart = ChartConfig.create(
    chart_type='bar',
    title='Mi Gráfica',
    group_by='region',
    value_column='total'
)  # Lanza ValidationError si es inválido
```

## Factory method

Usa `ChartConfig.create()` para crear y validar en un solo paso:

```python
from qry_doc import ChartConfig
from qry_doc.exceptions import ValidationError

try:
    chart = ChartConfig.create(
        chart_type='bar',
        title='Ventas',
        group_by='region',
        value_column='total',
        color='#003366'
    )
except ValidationError as e:
    print(f"Configuración inválida: {e.user_message}")
```

## Validar lista de gráficas

```python
from qry_doc.chart_config import validate_chart_list

charts = [chart1, chart2, chart3]
is_valid, error = validate_chart_list(charts)

if not is_valid:
    print(f"Error: {error}")
```

## Constantes útiles

```python
from qry_doc import VALID_CHART_TYPES, ChartTypeEnum

# Set de tipos válidos
print(VALID_CHART_TYPES)
# {'bar', 'barh', 'line', 'pie', 'scatter', 'area'}

# Enum para autocompletado
ChartTypeEnum.BAR.value    # 'bar'
ChartTypeEnum.PIE.value    # 'pie'
ChartTypeEnum.LINE.value   # 'line'
```

## Ver también

- [TemplateBuilder](template-builder.md)
- [AIBuilder](ai-builder.md) - Para sugerencias automáticas de gráficas
- [Múltiples Gráficas (guía anterior)](multiple-charts.md)
