# QryDoc

La clase principal que actúa como punto de entrada (Facade) para toda la funcionalidad de qry-doc.

## Importación

```python
from qry_doc import QryDoc
```

## Constructor

```python
QryDoc(
    data_source: str | Path | DataFrame,
    llm: Any,
    api_key: str | None = None
)
```

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `data_source` | `str \| Path \| DataFrame` | Fuente de datos (ruta CSV o DataFrame) |
| `llm` | `Any` | Instancia del proveedor LLM |
| `api_key` | `str \| None` | API key opcional (fallback) |

### Ejemplo

```python
from qry_doc import QryDoc
import pandasai as pai
from pandasai_openai import OpenAI

llm = OpenAI()
pai.config.set({"llm": llm})

# Desde archivo CSV
qry = QryDoc("datos.csv", llm=llm)

# Desde DataFrame
import pandas as pd
df = pd.read_csv("datos.csv")
qry = QryDoc(df, llm=llm)
```

## Métodos

### ask()

Realiza una pregunta en lenguaje natural sobre los datos.

```python
def ask(self, query: str) -> str
```

#### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `query` | `str` | Pregunta en lenguaje natural |

#### Retorno

`str` - Respuesta generada por el LLM.

#### Ejemplo

```python
respuesta = qry.ask("¿Cuál es el total de ventas?")
print(respuesta)  # "El total de ventas es $1,234,567"
```

#### Excepciones

- `QueryError`: Si la consulta no puede ser interpretada o ejecutada.

---

### extract_to_csv()

Extrae datos basados en una consulta y los guarda como CSV.

```python
def extract_to_csv(
    self,
    query: str,
    output_path: str | Path,
    include_index: bool = False
) -> str
```

#### Parámetros

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `query` | `str` | - | Consulta que describe los datos a extraer |
| `output_path` | `str \| Path` | - | Ruta del archivo CSV de salida |
| `include_index` | `bool` | `False` | Incluir índice en el CSV |

#### Retorno

`str` - Mensaje de confirmación.

#### Ejemplo

```python
qry.extract_to_csv(
    "Top 10 clientes por ingresos",
    "top_clientes.csv"
)
```

#### Excepciones

- `ExportError`: Si la exportación falla.

---

### generate_report()

Genera un reporte PDF profesional.

```python
def generate_report(
    self,
    query: str,
    output_path: str | Path,
    title: str | None = None,
    template: ReportTemplate | None = None
) -> str
```

#### Parámetros

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `query` | `str` | - | Consulta para el análisis |
| `output_path` | `str \| Path` | - | Ruta del archivo PDF |
| `title` | `str \| None` | `None` | Título del reporte |
| `template` | `ReportTemplate \| None` | `None` | Template de estilo |

#### Retorno

`str` - Mensaje de confirmación.

#### Ejemplo

```python
from qry_doc import ReportTemplate

template = ReportTemplate(
    primary_color="#003366",
    cover_image_path=Path("portada.png"),
)

qry.generate_report(
    "Análisis de ventas Q4",
    "reporte.pdf",
    title="Informe Trimestral",
    template=template
)
```

#### Excepciones

- `ReportError`: Si la generación del reporte falla.
- `ValidationError`: Si la portada o recursos son inválidos.

## Propiedades

### dataframe

```python
@property
def dataframe(self) -> pd.DataFrame
```

Retorna el DataFrame subyacente.

### columns

```python
@property
def columns(self) -> list[str]
```

Retorna la lista de nombres de columnas.

### shape

```python
@property
def shape(self) -> tuple[int, int]
```

Retorna las dimensiones (filas, columnas).

## Context Manager

QryDoc puede usarse como context manager para limpieza automática:

```python
with QryDoc("datos.csv", llm=llm) as qry:
    respuesta = qry.ask("¿Cuántos registros hay?")
    qry.generate_report("Resumen", "reporte.pdf")
# Archivos temporales se limpian automáticamente
```

## Excepciones

| Excepción | Descripción |
|-----------|-------------|
| `QryDocError` | Excepción base |
| `QueryError` | Error en consulta |
| `ExportError` | Error en exportación |
| `ReportError` | Error en generación de reporte |
| `DataSourceError` | Error al cargar datos |
| `ValidationError` | Error de validación |

Todas las excepciones incluyen:

- `user_message`: Mensaje amigable para el usuario
- `internal_error`: Excepción original para debugging

```python
from qry_doc import QueryError

try:
    respuesta = qry.ask("consulta ambigua")
except QueryError as e:
    print(f"Error: {e.user_message}")
```

## Ver también

- [ReportTemplate](report-template.md)
- [Tipos y Enums](types.md)
