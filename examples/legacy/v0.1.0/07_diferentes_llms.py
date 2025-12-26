"""
07 - Usar Diferentes Proveedores LLM
====================================

Este ejemplo muestra cómo configurar qry-doc con diferentes
proveedores de modelos de lenguaje (LLM).

PandasAI 3.x usa paquetes separados para cada proveedor:
- pandasai-openai
- pandasai-litellm (para múltiples proveedores)

Proveedores soportados vía LiteLLM:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google (Gemini)
- Azure OpenAI
- Ollama (modelos locales)
- Y muchos más...
"""

from qry_doc import QryDoc
import pandasai as pai
import os


# =============================================================================
# OPENAI (GPT-4, GPT-3.5)
# =============================================================================

print("=" * 60)
print("OPENAI")
print("=" * 60)

print("""
Instalación:
```bash
pip install pandasai-openai
```

Configuración:
```python
import pandasai as pai
from pandasai_openai import OpenAI

# Opción 1: Usar variable de entorno OPENAI_API_KEY
llm = OpenAI()

# Opción 2: Pasar API key directamente
llm = OpenAI(api_token="sk-tu-api-key")

# Opción 3: Especificar modelo
llm = OpenAI(model="gpt-4")

# Configurar PandasAI
pai.config.set({"llm": llm})

# Usar con qry-doc
qry = QryDoc("datos.csv", llm=llm)
```

Variables de entorno:
- OPENAI_API_KEY: Tu API key de OpenAI
""")


# =============================================================================
# LITELLM (MÚLTIPLES PROVEEDORES)
# =============================================================================

print("\n" + "=" * 60)
print("LITELLM (MÚLTIPLES PROVEEDORES)")
print("=" * 60)

print("""
LiteLLM permite usar casi cualquier proveedor con una interfaz unificada.

Instalación:
```bash
pip install pandasai-litellm
```

Configuración:
```python
import os
import pandasai as pai
from pandasai_litellm import LiteLLM

# OpenAI
os.environ["OPENAI_API_KEY"] = "tu-api-key"
llm = LiteLLM(model="gpt-4.1-mini")

# Anthropic Claude
os.environ["ANTHROPIC_API_KEY"] = "tu-api-key"
llm = LiteLLM(model="claude-3-opus-20240229")

# Google Gemini
os.environ["GEMINI_API_KEY"] = "tu-api-key"
llm = LiteLLM(model="gemini/gemini-pro")

# Configurar PandasAI
pai.config.set({"llm": llm})

# Usar con qry-doc
qry = QryDoc("datos.csv", llm=llm)
```

Modelos disponibles vía LiteLLM:
- gpt-4, gpt-4-turbo, gpt-3.5-turbo (OpenAI)
- claude-3-opus, claude-3-sonnet, claude-3-haiku (Anthropic)
- gemini/gemini-pro (Google)
- mistral/mistral-large-latest (Mistral)
- command-r-plus (Cohere)
""")


# =============================================================================
# AZURE OPENAI
# =============================================================================

print("\n" + "=" * 60)
print("AZURE OPENAI")
print("=" * 60)

print("""
Instalación:
```bash
pip install pandasai-openai
```

Configuración:
```python
import pandasai as pai
from pandasai_openai import AzureOpenAI

llm = AzureOpenAI(
    api_base="https://tu-recurso.openai.azure.com/",
    api_key="tu-api-key",
    deployment_name="tu-deployment"
)

pai.config.set({"llm": llm})
qry = QryDoc("datos.csv", llm=llm)
```
""")


# =============================================================================
# OLLAMA (MODELOS LOCALES)
# =============================================================================

print("\n" + "=" * 60)
print("OLLAMA (MODELOS LOCALES)")
print("=" * 60)

print("""
Ollama permite ejecutar modelos localmente sin API keys.

1. Instalar Ollama: https://ollama.ai/download

2. Descargar un modelo:
   ```bash
   ollama pull llama3
   ollama pull codellama
   ollama pull mistral
   ```

3. Usar con qry-doc vía LiteLLM:
   ```python
   import pandasai as pai
   from pandasai_litellm import LiteLLM
   
   # Usar modelo local de Ollama
   llm = LiteLLM(model="ollama/llama3")
   
   pai.config.set({"llm": llm})
   qry = QryDoc("datos.csv", llm=llm)
   ```

Modelos recomendados para análisis de datos:
- ollama/llama3 (general, bueno para consultas)
- ollama/codellama (especializado en código)
- ollama/mistral (rápido y eficiente)

Ventajas:
- Sin costos de API
- Privacidad total (datos no salen de tu máquina)
- Sin límites de uso
""")


# =============================================================================
# EJEMPLO PRÁCTICO: CAMBIAR ENTRE PROVEEDORES
# =============================================================================

print("\n" + "=" * 60)
print("EJEMPLO PRÁCTICO: CAMBIAR ENTRE PROVEEDORES")
print("=" * 60)

print("""
Patrón para cambiar fácilmente entre proveedores:

```python
import os
import pandasai as pai
from qry_doc import QryDoc

def get_llm(provider="openai"):
    '''Obtiene el LLM según el proveedor especificado.'''
    
    if provider == "openai":
        from pandasai_openai import OpenAI
        return OpenAI()
    
    elif provider == "litellm":
        from pandasai_litellm import LiteLLM
        return LiteLLM(model="gpt-4.1-mini")
    
    elif provider == "claude":
        from pandasai_litellm import LiteLLM
        return LiteLLM(model="claude-3-opus-20240229")
    
    elif provider == "ollama":
        from pandasai_litellm import LiteLLM
        return LiteLLM(model="ollama/llama3")
    
    else:
        raise ValueError(f"Proveedor no soportado: {provider}")

# Uso
provider = os.environ.get("LLM_PROVIDER", "openai")
llm = get_llm(provider)
pai.config.set({"llm": llm})
qry = QryDoc("datos.csv", llm=llm)
```

Esto permite cambiar de proveedor con una variable de entorno:
```bash
export LLM_PROVIDER=claude
python mi_script.py
```
""")


# =============================================================================
# COMPARACIÓN DE PROVEEDORES
# =============================================================================

print("\n" + "=" * 60)
print("COMPARACIÓN DE PROVEEDORES")
print("=" * 60)

print("""
┌─────────────┬──────────────┬─────────────┬──────────────┐
│ Proveedor   │ Velocidad    │ Calidad     │ Costo        │
├─────────────┼──────────────┼─────────────┼──────────────┤
│ GPT-4       │ Media        │ Excelente   │ Alto         │
│ GPT-3.5     │ Rápida       │ Buena       │ Bajo         │
│ Claude 3    │ Media        │ Excelente   │ Medio-Alto   │
│ Gemini Pro  │ Rápida       │ Buena       │ Bajo         │
│ Ollama      │ Variable*    │ Variable*   │ Gratis       │
└─────────────┴──────────────┴─────────────┴──────────────┘

* Depende del modelo y hardware local

Recomendaciones:
- Producción con presupuesto: GPT-3.5 o Gemini Pro
- Máxima calidad: GPT-4 o Claude 3 Opus
- Privacidad/sin costos: Ollama con llama3
- Experimentación: LiteLLM para probar varios
""")


# =============================================================================
# INSTALACIÓN DE EXTENSIONES
# =============================================================================

print("\n" + "=" * 60)
print("INSTALACIÓN DE EXTENSIONES")
print("=" * 60)

print("""
PandasAI 3.x usa paquetes separados para cada proveedor LLM:

# Para OpenAI
pip install pandasai-openai

# Para múltiples proveedores (recomendado)
pip install pandasai-litellm

# Instalación completa
pip install qry-doc pandasai-openai pandasai-litellm
""")


print("\n✅ Guía de proveedores LLM completada")
