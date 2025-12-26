"""
01 - Inicio Rápido con qry-doc
==============================

Este ejemplo muestra los primeros pasos para usar qry-doc.
Aprenderás a:
- Configurar el LLM
- Cargar datos
- Hacer tu primera consulta

Requisitos:
- pip install qry-doc pandasai-openai
- Configurar OPENAI_API_KEY como variable de entorno
"""

from qry_doc import QryDoc
import pandasai as pai
from pandasai_openai import OpenAI

# =============================================================================
# PASO 1: Configurar el LLM (Modelo de Lenguaje)
# =============================================================================

# Opción A: Usar variable de entorno OPENAI_API_KEY (recomendado)
llm = OpenAI()

# Opción B: Pasar el API key directamente (no recomendado para producción)
# llm = OpenAI(api_token="sk-tu-api-key-aqui")

# Configurar PandasAI con el LLM
pai.config.set({"llm": llm})


# =============================================================================
# PASO 2: Cargar los datos
# =============================================================================

# Desde un archivo CSV
qry = QryDoc("data/ventas.csv", llm=llm)

# También puedes cargar desde un DataFrame de pandas:
# import pandas as pd
# df = pd.read_excel("datos.xlsx")
# qry = QryDoc(df, llm=llm)


# =============================================================================
# PASO 3: Explorar los datos
# =============================================================================

# Ver las columnas disponibles
print("Columnas disponibles:")
print(qry.columns)
# Output: ['fecha', 'producto', 'categoria', 'cantidad', 'precio_unitario', 'vendedor', 'region']

# Ver las dimensiones (filas, columnas)
print(f"\nDimensiones: {qry.shape[0]} filas x {qry.shape[1]} columnas")


# =============================================================================
# PASO 4: Hacer tu primera consulta
# =============================================================================

# Pregunta en lenguaje natural
respuesta = qry.ask("¿Cuántas ventas hay en total?")
print(f"\nRespuesta: {respuesta}")

# Otra pregunta
respuesta = qry.ask("¿Cuál es el producto más vendido?")
print(f"Producto más vendido: {respuesta}")


# =============================================================================
# PASO 5: Usar como context manager (recomendado)
# =============================================================================

# El context manager limpia automáticamente los archivos temporales
with QryDoc("data/ventas.csv", llm=llm) as qry:
    total = qry.ask("¿Cuál es el total de ingresos?")
    print(f"\nTotal de ingresos: {total}")
# Los archivos temporales se eliminan automáticamente aquí


print("\n✅ ¡Felicidades! Has completado tu primer ejemplo con qry-doc")
