# ReportPresets

<span class="version-badge new">v0.1.5</span>

ReportPresets proporciona configuraciones predefinidas optimizadas para diferentes industrias, permitiendo crear reportes profesionales con estilos apropiados para cada sector.

## Uso básico

```python
from qry_doc import TemplateBuilder, ReportPresetType

# Crear template desde preset
template = TemplateBuilder.from_preset(ReportPresetType.FINANCIAL).build()
```

## Presets disponibles

### FINANCIAL

Ideal para banca, inversiones y contabilidad.

```python
template = TemplateBuilder.from_preset(ReportPresetType.FINANCIAL).build()
```

| Propiedad | Valor |
|-----------|-------|
| Color primario | `#003366` (Azul corporativo) |
| Color secundario | `#0066CC` |
| Fuente títulos | Helvetica-Bold |
| Fuente cuerpo | Helvetica |

---

### HEALTHCARE

Ideal para salud, farmacéutica y bienestar.

```python
template = TemplateBuilder.from_preset(ReportPresetType.HEALTHCARE).build()
```

| Propiedad | Valor |
|-----------|-------|
| Color primario | `#006666` (Verde/Teal) |
| Color secundario | `#00A3A3` |
| Fuente títulos | Helvetica-Bold |
| Fuente cuerpo | Helvetica |

---

### TECHNOLOGY

Ideal para software, TI y servicios digitales.

```python
template = TemplateBuilder.from_preset(ReportPresetType.TECHNOLOGY).build()
```

| Propiedad | Valor |
|-----------|-------|
| Color primario | `#5C2D91` (Púrpura moderno) |
| Color secundario | `#8661C5` |
| Fuente títulos | Helvetica-Bold |
| Fuente cuerpo | Helvetica |

---

### RETAIL

Ideal para comercio, e-commerce y ventas.

```python
template = TemplateBuilder.from_preset(ReportPresetType.RETAIL).build()
```

| Propiedad | Valor |
|-----------|-------|
| Color primario | `#E65100` (Naranja vibrante) |
| Color secundario | `#FF9800` |
| Fuente títulos | Helvetica-Bold |
| Fuente cuerpo | Helvetica |

---

### MANUFACTURING

Ideal para producción, logística e ingeniería.

```python
template = TemplateBuilder.from_preset(ReportPresetType.MANUFACTURING).build()
```

| Propiedad | Valor |
|-----------|-------|
| Color primario | `#455A64` (Gris industrial) |
| Color secundario | `#78909C` |
| Fuente títulos | Helvetica-Bold |
| Fuente cuerpo | Helvetica |

---

### CONSULTING

Ideal para consultoría, estrategia y servicios profesionales.

```python
template = TemplateBuilder.from_preset(ReportPresetType.CONSULTING).build()
```

| Propiedad | Valor |
|-----------|-------|
| Color primario | `#1A237E` (Azul marino) |
| Color secundario | `#C9A227` (Dorado) |
| Fuente títulos | Helvetica-Bold |
| Fuente cuerpo | Helvetica |

## Listar presets

```python
from qry_doc import ReportPreset

for name, description in ReportPreset.list_all():
    print(f"{name}: {description}")
```

Output:
```
Financial: Professional financial reports with blue tones...
Healthcare: Clean healthcare reports with green/teal tones...
Technology: Modern technology reports with purple tones...
Retail: Vibrant retail reports with orange/warm tones...
Manufacturing: Industrial manufacturing reports with gray/steel tones...
Consulting: Executive consulting reports with navy/gold tones...
```

## Obtener preset directamente

```python
from qry_doc import ReportPreset, ReportPresetType

preset = ReportPreset.get(ReportPresetType.FINANCIAL)

print(f"Nombre: {preset.name}")
print(f"Descripción: {preset.description}")
print(f"Color primario: {preset.primary_color}")
print(f"Color secundario: {preset.secondary_color}")
```

## Personalizar un preset

### Con TemplateBuilder

```python
from qry_doc import TemplateBuilder, ReportPresetType

template = (
    TemplateBuilder.from_preset(ReportPresetType.FINANCIAL)
    .with_colors(primary="#001122")  # Override color
    .with_margins(top=100)           # Override margen
    .with_charts(charts)             # Añadir gráficas
    .build()
)
```

### Con to_template()

```python
from qry_doc import ReportPreset, ReportPresetType

preset = ReportPreset.get(ReportPresetType.TECHNOLOGY)

# Crear template con overrides
template = preset.to_template(
    primary_color="#4A148C",
    margin_top=80.0
)
```

## Secciones por defecto

Cada preset incluye secciones predefinidas:

| Preset | Secciones |
|--------|-----------|
| FINANCIAL | Cover → Summary → Chart → Data |
| HEALTHCARE | Cover → Summary → Data → Chart |
| TECHNOLOGY | Summary → Chart → Chart → Data |
| RETAIL | Cover → Summary → Chart → Data |
| MANUFACTURING | Summary → Data → Chart → Data |
| CONSULTING | Cover → Summary → Chart → Data → Custom |

## Ejemplo completo

```python
from qry_doc import QryDoc, TemplateBuilder, ReportPresetType, ChartConfig

qry = QryDoc("ventas.csv", llm=llm)

# Definir gráficas
charts = [
    ChartConfig(chart_type='bar', title='Ventas', group_by='region', value_column='total'),
    ChartConfig(chart_type='pie', title='Distribución', group_by='categoria', value_column='cantidad'),
]

# Crear template desde preset con personalizaciones
template = (
    TemplateBuilder.from_preset(ReportPresetType.FINANCIAL)
    .with_margins(top=80, bottom=80)
    .with_charts(charts)
)

# Crear portada
cover = (
    qry.create_cover()
    .set_title("Informe Financiero Q4", color="#003366")
    .set_subtitle("Análisis de Resultados")
    .set_author("Departamento de Finanzas")
)

# Generar reporte
qry.generate_report_with_builder(
    "informe_financiero.pdf",
    cover=cover,
    template=template,
    title="Informe Q4 2024"
)

print("✅ Reporte financiero generado")
```

## Validación

Los presets validan que todos los campos requeridos estén presentes:

```python
preset = ReportPreset.get(ReportPresetType.FINANCIAL)
is_valid, error = preset.validate()

if not is_valid:
    print(f"Error: {error}")
```

## Ver también

- [TemplateBuilder](template-builder.md)
- [ChartConfig](chart-config.md)
- [CoverBuilder](cover-builder.md)
