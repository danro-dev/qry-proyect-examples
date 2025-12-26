# Instalación

Esta guía te ayudará a instalar qry-doc y configurar tu entorno de desarrollo.

## Requisitos

- **Python 3.11+**
- Un proveedor de LLM (OpenAI, Anthropic, etc.)

## Instalación con uv (Recomendado)

[uv](https://docs.astral.sh/uv/) es un gestor de paquetes moderno y rápido para Python.

=== "Instalación básica"

    ```bash
    uv add qry-doc
    ```

=== "Con soporte OpenAI"

    ```bash
    uv add "qry-doc[openai]"
    ```

=== "Con múltiples proveedores"

    ```bash
    uv add "qry-doc[litellm]"
    ```

=== "Con AIBuilder (LangChain)"

    ```bash
    uv add "qry-doc[langchain]"
    ```

=== "Instalación completa"

    ```bash
    uv add "qry-doc[all]"
    ```

## Instalación con pip

Si prefieres usar pip:

=== "Instalación básica"

    ```bash
    pip install qry-doc
    ```

=== "Con soporte OpenAI"

    ```bash
    pip install "qry-doc[openai]"
    ```

=== "Con múltiples proveedores"

    ```bash
    pip install "qry-doc[litellm]"
    ```

=== "Con AIBuilder (LangChain)"

    ```bash
    pip install "qry-doc[langchain]"
    ```

=== "Instalación completa"

    ```bash
    pip install "qry-doc[all]"
    ```

## Desde código fuente

Para desarrollo o para obtener la última versión:

```bash
git clone https://github.com/danro-dev/qry-doc.git
cd qry-doc
uv sync
```

## Configuración del LLM

qry-doc utiliza [PandasAI](https://pandas-ai.com/) como motor de IA. Necesitas configurar un proveedor de LLM.

### OpenAI

```python
import pandasai as pai
from pandasai_openai import OpenAI

# Opción 1: Usando variable de entorno OPENAI_API_KEY
llm = OpenAI()

# Opción 2: Pasando el API key directamente
llm = OpenAI(api_token="sk-...")

# Configurar PandasAI
pai.config.set({"llm": llm})
```

!!! tip "Variable de entorno"
    Es recomendable usar variables de entorno para las API keys:
    ```bash
    export OPENAI_API_KEY="sk-..."
    ```

### Otros proveedores

qry-doc soporta múltiples proveedores a través de LiteLLM:

- **Anthropic** (Claude)
- **Google** (Gemini)
- **Azure OpenAI**
- **Ollama** (modelos locales)
- Y muchos más...

```python
from pandasai_litellm import LiteLLM

# Ejemplo con Claude
llm = LiteLLM(model="claude-3-opus-20240229")
```

## Verificar instalación

Ejecuta este código para verificar que todo está configurado correctamente:

```python
from qry_doc import QryDoc, ReportTemplate
import pandas as pd

# Crear datos de prueba
df = pd.DataFrame({
    'producto': ['A', 'B', 'C'],
    'ventas': [100, 200, 150]
})

# Verificar importaciones
print("✅ qry-doc instalado correctamente")
print(f"   Versión: 0.1.3")

# Verificar ReportTemplate
template = ReportTemplate()
print("✅ ReportTemplate disponible")

# Verificar nuevos tipos
from qry_doc import SectionType, LogoPosition, SectionConfig
print("✅ Nuevos tipos v0.1.3 disponibles")
```

## Extras opcionales

| Extra | Descripción | Comando |
|-------|-------------|---------|
| `openai` | Soporte para OpenAI GPT | `qry-doc[openai]` |
| `litellm` | Múltiples proveedores LLM | `qry-doc[litellm]` |
| `langchain` | AIBuilder con LangChain | `qry-doc[langchain]` |
| `postgres` | Conexión a PostgreSQL | `qry-doc[postgres]` |
| `mysql` | Conexión a MySQL | `qry-doc[mysql]` |
| `all` | Todos los extras | `qry-doc[all]` |

## Siguiente paso

Una vez instalado, continúa con el [Inicio Rápido](quickstart.md) para crear tu primer reporte.
