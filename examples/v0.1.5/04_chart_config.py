"""
Ejemplo 04: Múltiples Gráficas con ChartConfig
==============================================

Este ejemplo demuestra cómo incluir múltiples gráficas en un reporte
usando ChartConfig, introducido en qry-doc v0.1.5.

Características demostradas:
- Crear configuraciones de gráficas
- Diferentes tipos de gráficas
- Múltiples gráficas en un reporte
- Validación de configuraciones
- Tamaños personalizados
"""

from pathlib import Path
import pandas as pd

from qry_doc import (
    QryDoc,
    ChartConfig,
    ChartTypeEnum,
    TemplateBuilder,
    VALID_CHART_TYPES,
)
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
    print(f"   Columnas: {qry.columns}")
    
    # =========================================================================
    # MOSTRAR TIPOS DE GRÁFICAS DISPONIBLES
    # =========================================================================
    
    print(f"\n📈 Tipos de gráficas soportados: {VALID_CHART_TYPES}")
    
    # =========================================================================
    # EJEMPLO 1: Gráfica individual
    # =========================================================================
    
    chart_bar = ChartConfig(
        chart_type='bar',
        title='Ventas por Región',
        group_by='region',
        value_column='cantidad',
        color='#003366'
    )
    
    # Validar configuración
    is_valid, error = chart_bar.validate()
    print(f"\n✓ Gráfica de barras válida: {is_valid}")
    
    template_single = qry.create_template().with_colors("#003366").with_charts([chart_bar])
    
    qry.generate_report_with_builder(
        output_dir / "04a_grafica_individual.pdf",
        template=template_single,
        title="Reporte con Gráfica Individual"
    )
    print("✅ 04a_grafica_individual.pdf generado")
    
    # =========================================================================
    # EJEMPLO 2: Múltiples gráficas
    # =========================================================================
    
    charts_multiple = [
        ChartConfig(
            chart_type='bar',
            title='Ventas por Región',
            group_by='region',
            value_column='cantidad',
            color='#003366'
        ),
        ChartConfig(
            chart_type='pie',
            title='Distribución por Categoría',
            group_by='categoria',
            value_column='cantidad',
            color='#E65100'
        ),
        ChartConfig(
            chart_type='barh',
            title='Top Vendedores',
            group_by='vendedor',
            value_column='cantidad',
            color='#5C2D91'
        ),
    ]
    
    template_multiple = (
        qry.create_template()
        .with_colors("#003366")
        .with_charts(charts_multiple)
    )
    
    qry.generate_report_with_builder(
        output_dir / "04b_multiples_graficas.pdf",
        template=template_multiple,
        title="Reporte con Múltiples Gráficas"
    )
    print("✅ 04b_multiples_graficas.pdf generado")
    
    # =========================================================================
    # EJEMPLO 3: Todos los tipos de gráficas
    # =========================================================================
    
    # Nota: Usamos columnas que existen en el CSV
    charts_todos_tipos = [
        ChartConfig(
            chart_type='bar',
            title='Gráfica de Barras',
            group_by='region',
            value_column='cantidad'
        ),
        ChartConfig(
            chart_type='barh',
            title='Barras Horizontales',
            group_by='categoria',
            value_column='cantidad'
        ),
        ChartConfig(
            chart_type='pie',
            title='Gráfica de Pastel',
            group_by='categoria',
            value_column='cantidad'
        ),
    ]
    
    template_tipos = (
        qry.create_template()
        .with_colors("#006666")
        .with_charts(charts_todos_tipos)
    )
    
    qry.generate_report_with_builder(
        output_dir / "04c_todos_tipos.pdf",
        template=template_tipos,
        title="Demostración de Tipos de Gráficas"
    )
    print("✅ 04c_todos_tipos.pdf generado")
    
    # =========================================================================
    # EJEMPLO 4: Gráficas con tamaños personalizados
    # =========================================================================
    
    charts_tamanos = [
        ChartConfig(
            chart_type='bar',
            title='Gráfica Grande',
            group_by='region',
            value_column='cantidad',
            figsize=(14, 8)  # Más ancha
        ),
        ChartConfig(
            chart_type='pie',
            title='Gráfica Cuadrada',
            group_by='categoria',
            value_column='cantidad',
            figsize=(8, 8)  # Cuadrada
        ),
    ]
    
    template_tamanos = (
        qry.create_template()
        .with_colors("#1A237E")
        .with_charts(charts_tamanos)
    )
    
    qry.generate_report_with_builder(
        output_dir / "04d_tamanos_personalizados.pdf",
        template=template_tamanos,
        title="Gráficas con Tamaños Personalizados"
    )
    print("✅ 04d_tamanos_personalizados.pdf generado")
    
    # =========================================================================
    # EJEMPLO 5: Usando factory method con validación
    # =========================================================================
    
    try:
        chart_validado = ChartConfig.create(
            chart_type='bar',
            title='Gráfica Validada',
            group_by='region',
            value_column='cantidad',
            color='#FF5722'
        )
        print(f"\n✓ ChartConfig.create() validó correctamente")
        
        template_validado = (
            qry.create_template()
            .with_colors("#FF5722")
            .with_charts([chart_validado])
        )
        
        qry.generate_report_with_builder(
            output_dir / "04e_factory_method.pdf",
            template=template_validado,
            title="Gráfica con Factory Method"
        )
        print("✅ 04e_factory_method.pdf generado")
        
    except Exception as e:
        print(f"✗ Error de validación: {e}")
    
    # =========================================================================
    # MOSTRAR LÍMITE DE GRÁFICAS
    # =========================================================================
    
    print(f"\n⚠️  Límite máximo de gráficas por reporte: 10")
    
    print(f"\n📁 Todos los reportes guardados en: {output_dir}")


if __name__ == "__main__":
    main()
