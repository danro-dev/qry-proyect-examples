"""
Ejemplo 06: Ejemplo Completo - Todas las Funcionalidades v0.1.5
===============================================================

Este ejemplo combina todas las nuevas funcionalidades de qry-doc v0.1.5
para crear un reporte profesional completo.

Funcionalidades utilizadas:
- AIBuilder para análisis inteligente
- CoverBuilder para portada dinámica
- TemplateBuilder con preset personalizado
- ChartConfig para múltiples gráficas
- ReportPresets como base
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

from qry_doc import (
    QryDoc,
    TemplateBuilder,
    ReportPresetType,
    ChartConfig,
    SectionConfig,
    SectionType,
    LogoPosition,
    TextAlignment,
)
import pandasai as pai
from pandasai_openai import OpenAI


def main():
    print("=" * 70)
    print("🚀 EJEMPLO COMPLETO - qry-doc v0.1.5")
    print("=" * 70)
    
    # =========================================================================
    # CONFIGURACIÓN INICIAL
    # =========================================================================
    
    llm = OpenAI()
    pai.config.set({"llm": llm})
    
    data_path = Path("examples/data/ventas.csv")
    output_dir = Path("output/v0.1.5")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    qry = QryDoc(data_path, llm=llm)
    print(f"\n📊 Datos cargados: {qry.shape[0]} filas, {qry.shape[1]} columnas")
    print(f"   Columnas: {qry.columns}")
    
    # =========================================================================
    # PASO 1: ANÁLISIS CON AIBUILDER
    # =========================================================================
    
    print("\n" + "-" * 70)
    print("PASO 1: Análisis con AIBuilder")
    print("-" * 70)
    
    ai = qry.ai_builder
    
    # Obtener resumen
    summary = ai.get_data_summary()
    print(f"✓ Resumen obtenido: {summary.shape[0]} filas, {len(summary.numeric_columns)} columnas numéricas")
    
    # Obtener sugerencias de gráficas
    suggestions = ai.suggest_charts("análisis completo de ventas por región y categoría")
    print(f"✓ {len(suggestions)} sugerencias de gráficas obtenidas")
    
    for s in suggestions[:3]:
        print(f"  • {s.config.title} ({s.config.chart_type}) - {s.confidence:.0%} confianza")
    
    # =========================================================================
    # PASO 2: CREAR PORTADA CON COVERBUILDER
    # =========================================================================
    
    print("\n" + "-" * 70)
    print("PASO 2: Crear portada con CoverBuilder")
    print("-" * 70)
    
    cover = (
        qry.create_cover()
        # Título principal
        .set_title(
            "Informe Ejecutivo de Ventas",
            font_size=42,
            color="#003366",
            y=550.0
        )
        # Subtítulo
        .set_subtitle(
            f"Análisis Q4 {datetime.now().year}",
            font_size=24,
            color="#666666",
            y=490.0
        )
        # Marca de agua
        .add_custom_text(
            "GENERADO CON qry-doc v0.1.5",
            x=306.0,
            y=750.0,
            font_size=10,
            color="#CCCCCC",
            alignment=TextAlignment.CENTER
        )
        # Fecha
        .set_date(
            datetime.now(),
            format="%d de %B, %Y"
        )
        # Autor
        .set_author("Equipo de Análisis de Datos")
        # Versión
        .add_custom_text(
            "Versión 1.0",
            x=540.0,
            y=50.0,
            font_size=10,
            color="#999999",
            alignment=TextAlignment.RIGHT
        )
        # Fondo
        .set_background_color("#FAFAFA")
    )
    
    print("✓ Portada configurada con título, subtítulo, fecha, autor y marca de agua")
    
    # =========================================================================
    # PASO 3: CREAR GRÁFICAS CON CHARTCONFIG
    # =========================================================================
    
    print("\n" + "-" * 70)
    print("PASO 3: Crear gráficas con ChartConfig")
    print("-" * 70)
    
    # Usar sugerencias de AI + gráficas personalizadas
    charts = [
        # Gráfica sugerida por AI
        suggestions[0].config if suggestions else ChartConfig(
            chart_type='bar',
            title='Ventas por Región',
            group_by='region',
            value_column='cantidad',
            color='#003366'
        ),
        # Gráfica personalizada
        ChartConfig(
            chart_type='pie',
            title='Distribución por Categoría',
            group_by='categoria',
            value_column='cantidad',
            color='#E65100',
            figsize=(8, 8)
        ),
        # Otra gráfica personalizada
        ChartConfig(
            chart_type='barh',
            title='Rendimiento por Vendedor',
            group_by='vendedor',
            value_column='cantidad',
            color='#006666'
        ),
    ]
    
    print(f"✓ {len(charts)} gráficas configuradas:")
    for chart in charts:
        print(f"  • {chart.title} ({chart.chart_type})")
    
    # =========================================================================
    # PASO 4: CREAR TEMPLATE CON TEMPLATEBUILDER
    # =========================================================================
    
    print("\n" + "-" * 70)
    print("PASO 4: Crear template con TemplateBuilder")
    print("-" * 70)
    
    template = (
        # Iniciar desde preset FINANCIAL
        TemplateBuilder.from_preset(ReportPresetType.FINANCIAL)
        # Personalizar colores
        .with_colors(primary="#003366", secondary="#0066CC")
        # Personalizar márgenes
        .with_margins(top=80, bottom=80, left=72, right=72)
        # Configurar footer
        .with_footer(
            logo_position=LogoPosition.BOTTOM_RIGHT,
            logo_width=100,
            logo_height=50
        )
        # Configurar secciones
        .with_sections([
            SectionConfig(SectionType.SUMMARY),
            SectionConfig(SectionType.CHART),
            SectionConfig(SectionType.DATA),
            SectionConfig(
                SectionType.CUSTOM,
                custom_content="""
                NOTAS DEL REPORTE
                -----------------
                Este reporte fue generado automáticamente usando qry-doc v0.1.5.
                
                Las gráficas fueron sugeridas por AIBuilder basándose en el análisis
                de la estructura de los datos.
                
                Para más información, contacte al equipo de análisis de datos.
                """
            ),
        ])
        # Añadir gráficas
        .with_charts(charts)
    )
    
    print("✓ Template configurado:")
    print("  • Base: Preset FINANCIAL")
    print("  • Colores personalizados")
    print("  • Márgenes ajustados")
    print("  • Footer con logo")
    print(f"  • {len(charts)} gráficas")
    print("  • 4 secciones (Summary, Chart, Data, Custom)")
    
    # =========================================================================
    # PASO 5: GENERAR REPORTE FINAL
    # =========================================================================
    
    print("\n" + "-" * 70)
    print("PASO 5: Generar reporte final")
    print("-" * 70)
    
    output_path = output_dir / "06_reporte_completo.pdf"
    
    qry.generate_report_with_builder(
        output_path,
        cover=cover,
        template=template,
        title="Informe Ejecutivo de Ventas Q4 2024",
        summary=f"""
        RESUMEN EJECUTIVO
        
        Este informe presenta un análisis completo de las ventas del cuarto 
        trimestre de 2024, generado automáticamente con qry-doc v0.1.5.
        
        DATOS ANALIZADOS:
        • {summary.shape[0]:,} registros procesados
        • {len(summary.numeric_columns)} métricas numéricas
        • {len(summary.categorical_columns)} dimensiones categóricas
        
        VISUALIZACIONES:
        • {len(charts)} gráficas generadas
        • Sugerencias basadas en análisis de AI
        
        METODOLOGÍA:
        El análisis fue realizado utilizando AIBuilder para identificar
        las visualizaciones más relevantes basándose en la estructura
        de los datos.
        """
    )
    
    print(f"✅ Reporte generado exitosamente: {output_path}")
    
    # =========================================================================
    # RESUMEN FINAL
    # =========================================================================
    
    print("\n" + "=" * 70)
    print("📋 RESUMEN DE FUNCIONALIDADES UTILIZADAS")
    print("=" * 70)
    print("""
    ✓ AIBuilder
      - get_data_summary() para análisis de datos
      - suggest_charts() para sugerencias de visualización
    
    ✓ CoverBuilder
      - set_title(), set_subtitle() para textos principales
      - set_date(), set_author() para metadatos
      - add_custom_text() para elementos adicionales
      - set_background_color() para fondo
    
    ✓ TemplateBuilder
      - from_preset() para iniciar desde preset
      - with_colors(), with_margins() para personalización
      - with_footer() para configurar pie de página
      - with_sections() para estructura del reporte
      - with_charts() para múltiples gráficas
    
    ✓ ChartConfig
      - Múltiples tipos de gráficas
      - Colores y tamaños personalizados
      - Integración con sugerencias de AI
    
    ✓ ReportPresets
      - FINANCIAL como base del template
    """)
    
    print(f"📁 Archivo generado: {output_path}")
    print(f"   Tamaño: {output_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
