"""
Ejemplo 05: Preparación Inteligente con AIBuilder
=================================================

Este ejemplo demuestra cómo usar AIBuilder para análisis inteligente
de datos y preparación de reportes, introducido en qry-doc v0.1.5.

Características demostradas:
- Resumen estructurado de datos
- Sugerencias de gráficas
- Preparación de datos para reportes
- Validación de consultas
- Contexto de conversación

Requisitos:
- pip install "qry-doc[langchain]"
"""

from pathlib import Path
import pandas as pd

from qry_doc import QryDoc, DataSummary, ChartSuggestion
import pandasai as pai
from pandasai_openai import OpenAI


def main():
    # Configurar LLM
    llm = OpenAI()
    pai.config.set({"llm": llm})
    
    # Rutas
    data_path = Path("examples/data/ventas.csv")
    output_dir = Path("output/v0.1.5")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Cargar datos
    qry = QryDoc(data_path, llm=llm)
    print(f"📊 Datos cargados: {qry.shape[0]} filas, {qry.shape[1]} columnas")
    
    # =========================================================================
    # OBTENER AIBUILDER
    # =========================================================================
    
    ai = qry.ai_builder
    print(f"\n🤖 AIBuilder inicializado")
    print(f"   LangChain disponible: {ai.has_langchain}")
    
    # =========================================================================
    # RESUMEN ESTRUCTURADO DE DATOS
    # =========================================================================
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE DATOS")
    print("=" * 60)
    
    summary: DataSummary = ai.get_data_summary()
    
    print(f"Dimensiones: {summary.shape[0]} filas x {summary.shape[1]} columnas")
    print(f"\nColumnas: {summary.columns}")
    print(f"\nColumnas numéricas: {summary.numeric_columns}")
    print(f"Columnas categóricas: {summary.categorical_columns}")
    
    print("\nTipos de datos:")
    for col, dtype in summary.dtypes.items():
        print(f"  • {col}: {dtype}")
    
    print("\nValores nulos:")
    has_nulls = False
    for col, count in summary.null_counts.items():
        if count > 0:
            print(f"  • {col}: {count} nulos")
            has_nulls = True
    if not has_nulls:
        print("  (sin valores nulos)")
    
    # =========================================================================
    # SUGERENCIAS DE GRÁFICAS
    # =========================================================================
    
    print("\n" + "=" * 60)
    print("📈 SUGERENCIAS DE GRÁFICAS")
    print("=" * 60)
    
    # Sin contexto
    suggestions = ai.suggest_charts()
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n{i}. {suggestion.config.title}")
        print(f"   Tipo: {suggestion.config.chart_type}")
        print(f"   Agrupar por: {suggestion.config.group_by}")
        print(f"   Columna de valor: {suggestion.config.value_column}")
        print(f"   Razón: {suggestion.reasoning}")
        print(f"   Confianza: {suggestion.confidence:.0%}")
    
    # =========================================================================
    # SUGERENCIAS CON CONTEXTO
    # =========================================================================
    
    print("\n" + "=" * 60)
    print("📈 SUGERENCIAS CON CONTEXTO")
    print("=" * 60)
    
    suggestions_contexto = ai.suggest_charts("Quiero analizar las ventas por región y categoría")
    
    print("Contexto: 'Quiero analizar las ventas por región y categoría'")
    for suggestion in suggestions_contexto[:3]:
        print(f"\n• {suggestion.config.title}")
        print(f"  {suggestion.reasoning}")
    
    # =========================================================================
    # PREPARAR DATOS PARA REPORTE
    # =========================================================================
    
    print("\n" + "=" * 60)
    print("📄 PREPARACIÓN DE DATOS PARA REPORTE")
    print("=" * 60)
    
    report_data = ai.prepare_report_data("Crear un reporte trimestral de ventas por región")
    
    print(f"Título sugerido: {report_data['title']}")
    print(f"\nPuntos clave del resumen:")
    for point in report_data['summary_points']:
        print(f"  • {point}")
    
    print(f"\nGráficas sugeridas: {len(report_data['charts'])}")
    for chart in report_data['charts']:
        print(f"  • {chart.title} ({chart.chart_type})")
    
    print(f"\nColumnas relevantes: {report_data['columns']}")
    
    # =========================================================================
    # VALIDAR CONSULTAS
    # =========================================================================
    
    print("\n" + "=" * 60)
    print("✓ VALIDACIÓN DE CONSULTAS")
    print("=" * 60)
    
    consultas = [
        "Total de ventas por región",
        "Promedio de precio por categoría",
        "Cantidad vendida por vendedor",
    ]
    
    for consulta in consultas:
        is_valid, error = ai.validate_query(consulta)
        status = "✓" if is_valid else "✗"
        print(f"{status} '{consulta}'")
        if not is_valid:
            print(f"   Error: {error}")
    
    # =========================================================================
    # CONTEXTO DE CONVERSACIÓN
    # =========================================================================
    
    print("\n" + "=" * 60)
    print("💬 CONTEXTO DE CONVERSACIÓN")
    print("=" * 60)
    
    contexto = ai.get_context()
    print(f"Mensajes en contexto: {len(contexto)}")
    
    for msg in contexto[-4:]:
        role = "Usuario" if msg['role'] == 'user' else "AI"
        content = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
        print(f"  [{role}]: {content}")
    
    # Limpiar contexto
    ai.clear_context()
    print(f"\n✓ Contexto limpiado")
    print(f"Mensajes en contexto: {len(ai.get_context())}")
    
    # =========================================================================
    # GENERAR REPORTE CON SUGERENCIAS DE AI
    # =========================================================================
    
    print("\n" + "=" * 60)
    print("📊 GENERANDO REPORTE CON SUGERENCIAS DE AI")
    print("=" * 60)
    
    # Obtener nuevas sugerencias
    suggestions = ai.suggest_charts("análisis de ventas")
    
    # Usar las configuraciones sugeridas
    template = (
        qry.create_template()
        .with_colors("#003366")
        .with_charts([s.config for s in suggestions[:3]])
    )
    
    cover = (
        qry.create_cover()
        .set_title("Reporte Generado con AI")
        .set_subtitle("Sugerencias automáticas de visualización")
        .set_author("AIBuilder")
    )
    
    qry.generate_report_with_builder(
        output_dir / "05_reporte_ai.pdf",
        cover=cover,
        template=template,
        title="Reporte con Sugerencias de AI"
    )
    print("✅ 05_reporte_ai.pdf generado")
    
    print(f"\n📁 Reporte guardado en: {output_dir}")


if __name__ == "__main__":
    main()
