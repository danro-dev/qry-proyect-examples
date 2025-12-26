"""
02 - Consultas Básicas
======================

Este ejemplo muestra diferentes tipos de consultas que puedes hacer
con qry-doc usando lenguaje natural.

Tipos de consultas:
- Agregaciones (suma, promedio, conteo)
- Filtros y búsquedas
- Comparaciones
- Análisis temporales
- Rankings y ordenamientos
"""

from qry_doc import QryDoc
import pandasai as pai
from pandasai_openai import OpenAI

# Configuración
llm = OpenAI()
pai.config.set({"llm": llm})
qry = QryDoc("data/ventas.csv", llm=llm)


# =============================================================================
# CONSULTAS DE AGREGACIÓN
# =============================================================================

print("=" * 60)
print("CONSULTAS DE AGREGACIÓN")
print("=" * 60)

# Suma total
total_ventas = qry.ask("¿Cuál es el total de ventas en cantidad?")
print(f"Total de unidades vendidas: {total_ventas}")

# Promedio
precio_promedio = qry.ask("¿Cuál es el precio unitario promedio?")
print(f"Precio promedio: {precio_promedio}")

# Conteo
num_transacciones = qry.ask("¿Cuántas transacciones hay registradas?")
print(f"Número de transacciones: {num_transacciones}")

# Máximo y mínimo
venta_maxima = qry.ask("¿Cuál fue la venta más grande en cantidad?")
print(f"Venta más grande: {venta_maxima}")


# =============================================================================
# CONSULTAS CON FILTROS
# =============================================================================

print("\n" + "=" * 60)
print("CONSULTAS CON FILTROS")
print("=" * 60)

# Filtro por categoría
electronica = qry.ask("¿Cuántas unidades de Electrónica se vendieron?")
print(f"Ventas de Electrónica: {electronica}")

# Filtro por vendedor
ventas_maria = qry.ask("¿Cuánto vendió María García en total?")
print(f"Ventas de María García: {ventas_maria}")

# Filtro por región
ventas_norte = qry.ask("¿Cuál es el total de ventas en la región Norte?")
print(f"Ventas región Norte: {ventas_norte}")

# Filtro por producto específico
laptops = qry.ask("¿Cuántas Laptop Pro se vendieron?")
print(f"Laptops Pro vendidas: {laptops}")


# =============================================================================
# CONSULTAS DE COMPARACIÓN
# =============================================================================

print("\n" + "=" * 60)
print("CONSULTAS DE COMPARACIÓN")
print("=" * 60)

# Comparar categorías
comparacion = qry.ask("¿Qué categoría vendió más: Electrónica o Accesorios?")
print(f"Comparación de categorías: {comparacion}")

# Comparar vendedores
mejor_vendedor = qry.ask("¿Quién es el vendedor con más ventas en cantidad?")
print(f"Mejor vendedor: {mejor_vendedor}")

# Comparar regiones
mejor_region = qry.ask("¿Cuál es la región con mayores ingresos?")
print(f"Mejor región: {mejor_region}")


# =============================================================================
# CONSULTAS TEMPORALES
# =============================================================================

print("\n" + "=" * 60)
print("CONSULTAS TEMPORALES")
print("=" * 60)

# Por mes
ventas_enero = qry.ask("¿Cuánto se vendió en enero de 2024?")
print(f"Ventas en enero: {ventas_enero}")

# Tendencia
tendencia = qry.ask("¿Cómo evolucionaron las ventas mes a mes?")
print(f"Tendencia mensual: {tendencia}")

# Comparación temporal
comparacion_meses = qry.ask("¿En qué mes se vendió más?")
print(f"Mes con más ventas: {comparacion_meses}")


# =============================================================================
# CONSULTAS DE RANKING
# =============================================================================

print("\n" + "=" * 60)
print("CONSULTAS DE RANKING")
print("=" * 60)

# Top productos
top_productos = qry.ask("¿Cuáles son los 3 productos más vendidos?")
print(f"Top 3 productos: {top_productos}")

# Ranking de vendedores
ranking = qry.ask("Ordena los vendedores por total de ventas de mayor a menor")
print(f"Ranking vendedores: {ranking}")


# =============================================================================
# CONSULTAS COMPLEJAS
# =============================================================================

print("\n" + "=" * 60)
print("CONSULTAS COMPLEJAS")
print("=" * 60)

# Múltiples condiciones
compleja1 = qry.ask(
    "¿Cuántas unidades de Electrónica vendió María García en la región Norte?"
)
print(f"Consulta compleja 1: {compleja1}")

# Análisis cruzado
compleja2 = qry.ask(
    "¿Cuál es el producto más vendido en cada región?"
)
print(f"Consulta compleja 2: {compleja2}")

# Cálculo derivado
compleja3 = qry.ask(
    "¿Cuál es el ingreso total (cantidad * precio_unitario) por categoría?"
)
print(f"Consulta compleja 3: {compleja3}")


print("\n✅ Ejemplos de consultas completados")
