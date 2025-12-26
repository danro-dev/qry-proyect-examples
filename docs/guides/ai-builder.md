# AIBuilder

<span class="version-badge new">v0.1.5</span>

AIBuilder es un agente inteligente que utiliza LangChain para ayudarte a preparar datos y obtener sugerencias de visualizaciones para tus reportes.

## Instalación

AIBuilder requiere la dependencia opcional de LangChain:

```bash
pip install "qry-doc[langchain]"
```

## Uso básico

```python
from qry_doc import QryDoc
import pandasai as pai
from pandasai_openai import OpenAI

llm = OpenAI()
pai.config.set({"llm": llm})

qry = QryDoc("datos.csv", llm=llm)

# Obtener el AIBuilder
ai = qry.ai_builder

# Verificar si LangChain está disponible
print(f"LangChain disponible: {ai.has_langchain}")
```

## Resumen de datos

Obtén un resumen estructurado de tu DataFrame:

```python
summary = ai.get_data_summary()

print(f"Dimensiones: {summary.shape}")
print(f"Columnas: {summary.columns}")
print(f"Columnas numéricas: {summary.numeric_columns}")
print(f"Columnas categóricas: {summary.categorical_columns}")
print(f"Tipos de datos: {summary.dtypes}")
print(f"Valores nulos: {summary.null_counts}")
```

### DataSummary

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `columns` | `list[str]` | Nombres de columnas |
| `dtypes` | `dict[str, str]` | Tipos de datos |
| `shape` | `tuple[int, int]` | (filas, columnas) |
| `sample` | `dict` | Muestra de datos |
| `numeric_columns` | `list[str]` | Columnas numéricas |
| `categorical_columns` | `list[str]` | Columnas categóricas |
| `null_counts` | `dict[str, int]` | Conteo de nulos |

## Sugerencias de gráficas

AIBuilder analiza tus datos y sugiere visualizaciones apropiadas:

```python
# Sin contexto - basado en estructura de datos
suggestions = ai.suggest_charts()

# Con contexto - considera tu objetivo
suggestions = ai.suggest_charts("Quiero analizar ventas por región")

for suggestion in suggestions:
    print(f"Tipo: {suggestion.config.chart_type}")
    print(f"Título: {suggestion.config.title}")
    print(f"Razón: {suggestion.reasoning}")
    print(f"Confianza: {suggestion.confidence:.0%}")
```

### ChartSuggestion

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `config` | `ChartConfig` | Configuración de la gráfica |
| `reasoning` | `str` | Razón de la sugerencia |
| `confidence` | `float` | Nivel de confianza (0.0 a 1.0) |

## Preparar datos para reportes

Genera datos estructurados para un reporte basado en una descripción:

```python
report_data = ai.prepare_report_data("Crear reporte trimestral de ventas")

print(f"Título sugerido: {report_data['title']}")
print(f"Puntos clave: {report_data['summary_points']}")
print(f"Gráficas sugeridas: {len(report_data['charts'])}")
print(f"Columnas relevantes: {report_data['columns']}")
```

### Estructura de retorno

```python
{
    "title": str,           # Título sugerido
    "summary_points": list, # Puntos clave del resumen
    "charts": list,         # Lista de ChartConfig
    "data_filters": dict,   # Filtros sugeridos
    "columns": list,        # Columnas relevantes
}
```

## Validar consultas

Verifica si una consulta es factible con los datos disponibles:

```python
is_valid, error = ai.validate_query("Total de ventas por región")

if is_valid:
    print("✓ Consulta válida")
else:
    print(f"✗ Error: {error}")
```

!!! tip "Validación previa"
    Usa `validate_query()` antes de ejecutar consultas costosas para evitar errores.

## Preguntas sobre los datos

Si LangChain está disponible, puedes hacer preguntas directas:

```python
if ai.has_langchain:
    respuesta = ai.ask("¿Cuáles son las columnas disponibles?")
    print(respuesta)
    
    respuesta = ai.ask("Dame un resumen de los datos")
    print(respuesta)
```

## Contexto de conversación

AIBuilder mantiene un contexto de conversación para interacciones iterativas:

```python
# Ver contexto actual
contexto = ai.get_context()
print(f"Mensajes en contexto: {len(contexto)}")

# Limpiar contexto
ai.clear_context()
```

!!! note "Límite de contexto"
    El contexto se limita a los últimos 20 mensajes para mantener el rendimiento.

## Ejemplo completo

```python
from qry_doc import QryDoc, TemplateBuilder
import pandasai as pai
from pandasai_openai import OpenAI

# Configurar
llm = OpenAI()
pai.config.set({"llm": llm})
qry = QryDoc("ventas.csv", llm=llm)

# Obtener AIBuilder
ai = qry.ai_builder

# Analizar datos
summary = ai.get_data_summary()
print(f"Analizando {summary.shape[0]} registros...")

# Obtener sugerencias
suggestions = ai.suggest_charts("análisis de ventas por región")

# Usar sugerencias para crear template
template = (
    qry.create_template()
    .with_colors("#003366")
    .with_charts([s.config for s in suggestions[:3]])
)

# Generar reporte
qry.generate_report_with_builder(
    "reporte_ai.pdf",
    template=template,
    title="Reporte Generado con AI"
)

print("✅ Reporte generado con sugerencias de AI")
```

## Sin LangChain

Si LangChain no está instalado, AIBuilder funciona con análisis básico:

```python
ai = qry.ai_builder

if not ai.has_langchain:
    print("LangChain no disponible, usando análisis básico")
    
# Estas funciones siempre funcionan:
summary = ai.get_data_summary()      # ✓
suggestions = ai.suggest_charts()     # ✓
report_data = ai.prepare_report_data("...") # ✓
is_valid, _ = ai.validate_query("...") # ✓

# ask() usa fallback básico sin LangChain
respuesta = ai.ask("¿Cuántos registros hay?")
```

## Ver también

- [ChartConfig](chart-config.md)
- [TemplateBuilder](template-builder.md)
- [QryDoc API](../api/qrydoc.md)
