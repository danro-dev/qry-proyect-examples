"""
06 - Manejo de Errores
======================

Este ejemplo muestra cómo manejar los diferentes tipos de errores
que pueden ocurrir al usar qry-doc.

Tipos de excepciones:
- QryDocError: Base para todos los errores
- QueryError: Error al interpretar consultas
- ExportError: Error al exportar datos
- ReportError: Error al generar reportes
- DataSourceError: Error al cargar datos
- ValidationError: Error de validación
"""

from qry_doc import (
    QryDoc,
    QryDocError,
    QueryError,
    ExportError,
    ReportError,
    DataSourceError,
    ValidationError,
)
import pandasai as pai
from pandasai_openai import OpenAI
import os

# Crear carpeta de salida
os.makedirs("output", exist_ok=True)


# =============================================================================
# ESTRUCTURA DE EXCEPCIONES
# =============================================================================

print("=" * 60)
print("ESTRUCTURA DE EXCEPCIONES")
print("=" * 60)

print("""
Jerarquía de excepciones en qry-doc:

QryDocError (base)
├── QueryError      - Errores al interpretar/ejecutar consultas
├── ExportError     - Errores al exportar a CSV
├── ReportError     - Errores al generar PDF
├── DataSourceError - Errores al cargar datos
└── ValidationError - Errores de validación

Todas las excepciones tienen:
- user_message: Mensaje amigable para mostrar al usuario
- internal_error: Excepción original (para debugging/logging)
""")


# =============================================================================
# ERROR AL CARGAR DATOS (DataSourceError)
# =============================================================================

print("\n" + "=" * 60)
print("ERROR AL CARGAR DATOS (DataSourceError)")
print("=" * 60)

llm = OpenAI()
pai.config.set({"llm": llm})

# Archivo que no existe
try:
    qry = QryDoc("archivo_inexistente.csv", llm=llm)
except DataSourceError as e:
    print(f"❌ Error capturado: {e.user_message}")
    # Output: "El archivo no existe: archivo_inexistente.csv"

# Formato no soportado
try:
    qry = QryDoc("datos.xyz", llm=llm)  # Extensión no reconocida
except DataSourceError as e:
    print(f"❌ Error capturado: {e.user_message}")
    # Output: "Formato de datos no reconocido..."

# Tipo de dato inválido
try:
    qry = QryDoc(12345, llm=llm)  # Número en lugar de path/DataFrame
except DataSourceError as e:
    print(f"❌ Error capturado: {e.user_message}")
    # Output: "Formato de datos no soportado (tipo: int)..."


# =============================================================================
# ERROR EN CONSULTAS (QueryError)
# =============================================================================

print("\n" + "=" * 60)
print("ERROR EN CONSULTAS (QueryError)")
print("=" * 60)

# Cargar datos válidos para probar errores de consulta
qry = QryDoc("data/ventas.csv", llm=llm)

# Consulta que puede fallar (depende del LLM)
try:
    # Consulta ambigua o que el LLM no puede interpretar
    respuesta = qry.ask("xyzabc123")  # Consulta sin sentido
except QueryError as e:
    print(f"❌ Error capturado: {e.user_message}")
    print(f"   Sugerencia: Reformule la pregunta con más detalle")


# =============================================================================
# ERROR AL EXPORTAR (ExportError)
# =============================================================================

print("\n" + "=" * 60)
print("ERROR AL EXPORTAR (ExportError)")
print("=" * 60)

# Consulta que no devuelve datos tabulares
try:
    qry.extract_to_csv(
        "¿Cuántas filas hay?",  # Devuelve un número, no una tabla
        "output/error.csv"
    )
except ExportError as e:
    print(f"❌ Error capturado: {e.user_message}")
    # Output: "El resultado no es tabular (tipo: int)..."

# Cómo evitarlo: pedir explícitamente datos tabulares
try:
    resultado = qry.extract_to_csv(
        "Muestra una tabla con el conteo de ventas por categoría",
        "output/conteo_categorias.csv"
    )
    print(f"✅ Exportación exitosa: {resultado}")
except ExportError as e:
    print(f"❌ Error: {e.user_message}")


# =============================================================================
# ERROR AL GENERAR REPORTE (ReportError)
# =============================================================================

print("\n" + "=" * 60)
print("ERROR AL GENERAR REPORTE (ReportError)")
print("=" * 60)

try:
    # Intentar generar reporte (puede fallar por varias razones)
    qry.generate_report(
        "Analiza las ventas",
        "output/reporte_test.pdf"
    )
    print("✅ Reporte generado correctamente")
except ReportError as e:
    print(f"❌ Error capturado: {e.user_message}")
    if e.internal_error:
        print(f"   Error interno: {type(e.internal_error).__name__}")


# =============================================================================
# CAPTURAR CUALQUIER ERROR DE QRY-DOC
# =============================================================================

print("\n" + "=" * 60)
print("CAPTURAR CUALQUIER ERROR DE QRY-DOC")
print("=" * 60)

def procesar_consulta_segura(qry, consulta):
    """Procesa una consulta manejando todos los errores posibles."""
    try:
        return qry.ask(consulta)
    except QryDocError as e:
        # Captura CUALQUIER error de qry-doc
        print(f"Error en qry-doc: {e.user_message}")
        return None

# Uso
resultado = procesar_consulta_segura(qry, "¿Cuál es el total de ventas?")
if resultado:
    print(f"Resultado: {resultado}")


# =============================================================================
# ACCEDER AL ERROR INTERNO (PARA LOGGING)
# =============================================================================

print("\n" + "=" * 60)
print("ACCEDER AL ERROR INTERNO (PARA LOGGING)")
print("=" * 60)

import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def exportar_con_logging(qry, consulta, path):
    """Exporta datos con logging detallado de errores."""
    try:
        return qry.extract_to_csv(consulta, path)
    except ExportError as e:
        # Mensaje amigable para el usuario
        print(f"No se pudo exportar: {e.user_message}")
        
        # Log detallado para debugging
        if e.internal_error:
            logger.error(
                f"Error interno en exportación: {e.internal_error}",
                exc_info=e.internal_error
            )
        
        return None

# Uso
exportar_con_logging(qry, "¿Total?", "output/test.csv")


# =============================================================================
# PATRÓN TRY-EXCEPT RECOMENDADO
# =============================================================================

print("\n" + "=" * 60)
print("PATRÓN TRY-EXCEPT RECOMENDADO")
print("=" * 60)

print("""
💡 Patrón recomendado para manejar errores:

```python
from qry_doc import (
    QryDoc, 
    QueryError, 
    ExportError, 
    ReportError,
    DataSourceError
)

try:
    # Cargar datos
    qry = QryDoc("datos.csv", llm=llm)
    
    # Hacer consulta
    respuesta = qry.ask("Mi pregunta")
    
    # Exportar
    qry.extract_to_csv("Mi consulta", "salida.csv")
    
    # Generar reporte
    qry.generate_report("Mi análisis", "reporte.pdf")
    
except DataSourceError as e:
    print(f"Error al cargar datos: {e.user_message}")
    
except QueryError as e:
    print(f"Error en consulta: {e.user_message}")
    print("Intente reformular la pregunta")
    
except ExportError as e:
    print(f"Error al exportar: {e.user_message}")
    print("Asegúrese de pedir datos tabulares")
    
except ReportError as e:
    print(f"Error al generar reporte: {e.user_message}")
```
""")


# =============================================================================
# SANITIZACIÓN DE ERRORES (SEGURIDAD)
# =============================================================================

print("\n" + "=" * 60)
print("SANITIZACIÓN DE ERRORES (SEGURIDAD)")
print("=" * 60)

print("""
🔒 qry-doc sanitiza automáticamente los mensajes de error para
   proteger información sensible:

   - API keys (sk-xxx...) → [REDACTED]
   - Contraseñas → [REDACTED]
   - Rutas completas del sistema → ...archivo.ext
   - Cadenas de conexión SQL → [REDACTED]

   Esto significa que puedes mostrar e.user_message al usuario
   sin preocuparte por exponer datos sensibles.
""")


print("\n✅ Ejemplos de manejo de errores completados")
