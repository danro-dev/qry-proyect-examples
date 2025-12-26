"""
Ejemplo 04: Sistema de Secciones Personalizadas
===============================================

Este ejemplo demuestra el sistema de secciones de qry-doc v0.1.3 que permite
controlar el orden y contenido de las diferentes partes del reporte.

Tipos de secciones disponibles (SectionType):
- COVER: Portada con imagen a página completa
- SUMMARY: Resumen ejecutivo con título
- DATA: Tabla de datos (DataFrame)
- CHART: Gráfico o visualización
- CUSTOM: Contenido personalizado arbitrario

Características demostradas:
- Orden personalizado de secciones
- Secciones habilitadas/deshabilitadas
- Contenido personalizado con CUSTOM
- Combinación de múltiples secciones
"""

from pathlib import Path
import pandas as pd

from qry_doc import (
    ReportTemplate, 
    ReportGenerator, 
    SectionType, 
    SectionConfig
)


def main():
    # Crear directorio de salida
    output_dir = Path("output/secciones")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Cargar datos
    df = pd.read_csv("examples/data/ventas.csv")
    portada = Path("public/portada.png")
    
    # =========================================================================
    # EJEMPLO 1: Orden por defecto (SUMMARY, CHART, DATA)
    # =========================================================================
    
    template_default = ReportTemplate(
        # Sin secciones configuradas = orden por defecto
        primary_color="#2c3e50",
    )
    
    generator = ReportGenerator(output_dir / "04a_orden_default.pdf", template_default)
    generator.build(
        title="Reporte con Orden por Defecto",
        summary="""
        Cuando no se configuran secciones explícitamente, qry-doc usa
        el orden por defecto: SUMMARY → CHART → DATA.
        
        Este es el comportamiento estándar para reportes simples.
        """,
        dataframe=df.head(8)
    )
    print("✅ Generado: 04a_orden_default.pdf")
    
    # =========================================================================
    # EJEMPLO 2: Orden personalizado (DATA primero, luego SUMMARY)
    # =========================================================================
    
    sections_data_first = [
        SectionConfig(SectionType.DATA),      # Datos primero
        SectionConfig(SectionType.SUMMARY),   # Resumen después
    ]
    
    template_data_first = ReportTemplate(
        sections=sections_data_first,
        primary_color="#e74c3c",
    )
    
    generator = ReportGenerator(output_dir / "04b_datos_primero.pdf", template_data_first)
    generator.build_with_sections(
        title="Datos Primero, Resumen Después",
        summary="""
        En este reporte, la tabla de datos aparece antes del resumen.
        
        Útil cuando los datos son lo más importante y el análisis
        es secundario.
        """,
        dataframe=df.head(8)
    )
    print("✅ Generado: 04b_datos_primero.pdf")
    
    # =========================================================================
    # EJEMPLO 3: Solo resumen (sin datos)
    # =========================================================================
    
    sections_solo_summary = [
        SectionConfig(SectionType.SUMMARY),
        # DATA deshabilitado
        SectionConfig(SectionType.DATA, enabled=False),
    ]
    
    template_solo_summary = ReportTemplate(
        sections=sections_solo_summary,
        primary_color="#27ae60",
    )
    
    generator = ReportGenerator(output_dir / "04c_solo_resumen.pdf", template_solo_summary)
    generator.build_with_sections(
        title="Reporte Ejecutivo (Solo Resumen)",
        summary="""
        Este reporte contiene únicamente el resumen ejecutivo.
        
        La sección de datos está deshabilitada (enabled=False),
        por lo que no aparece aunque se proporcione un DataFrame.
        
        Ideal para presentaciones ejecutivas donde los detalles
        técnicos no son necesarios.
        """,
        dataframe=df  # Se ignora porque DATA está deshabilitado
    )
    print("✅ Generado: 04c_solo_resumen.pdf")
    
    # =========================================================================
    # EJEMPLO 4: Secciones personalizadas (CUSTOM)
    # =========================================================================
    
    sections_custom = [
        SectionConfig(SectionType.SUMMARY),
        SectionConfig(
            SectionType.CUSTOM,
            custom_content="""
            METODOLOGÍA DEL ANÁLISIS
            
            Este análisis fue realizado utilizando técnicas avanzadas de
            procesamiento de datos con Python y la librería qry-doc.
            
            Los datos fueron recopilados durante el período Q4 2024 y
            procesados siguiendo los estándares de calidad ISO 9001.
            
            Para más información sobre la metodología, contactar al
            departamento de análisis de datos.
            """
        ),
        SectionConfig(SectionType.DATA),
        SectionConfig(
            SectionType.CUSTOM,
            custom_content="""
            NOTAS Y ADVERTENCIAS
            
            • Los datos presentados son preliminares y sujetos a revisión.
            • Las proyecciones se basan en tendencias históricas.
            • Consulte el apéndice para definiciones de términos técnicos.
            """
        ),
    ]
    
    template_custom = ReportTemplate(
        sections=sections_custom,
        primary_color="#9b59b6",
    )
    
    generator = ReportGenerator(output_dir / "04d_secciones_custom.pdf", template_custom)
    generator.build_with_sections(
        title="Reporte con Secciones Personalizadas",
        summary="""
        Este reporte demuestra el uso de secciones CUSTOM para agregar
        contenido arbitrario en cualquier parte del documento.
        
        Las secciones CUSTOM son ideales para:
        • Metodología
        • Notas legales
        • Advertencias
        • Información adicional
        """,
        dataframe=df.head(5)
    )
    print("✅ Generado: 04d_secciones_custom.pdf")
    
    # =========================================================================
    # EJEMPLO 5: Reporte completo con portada
    # =========================================================================
    
    if portada.exists():
        sections_completo = [
            SectionConfig(SectionType.COVER),     # Portada
            SectionConfig(SectionType.SUMMARY),   # Resumen
            SectionConfig(
                SectionType.CUSTOM,
                custom_content="""
                ÍNDICE DE CONTENIDOS
                
                1. Resumen Ejecutivo
                2. Análisis de Datos
                3. Conclusiones
                """
            ),
            SectionConfig(SectionType.DATA),      # Datos
        ]
        
        template_completo = ReportTemplate(
            cover_image_path=portada,
            sections=sections_completo,
            primary_color="#1a1a2e",
        )
        
        generator = ReportGenerator(output_dir / "04e_reporte_completo.pdf", template_completo)
        generator.build_with_sections(
            title="Informe Anual de Ventas 2024",
            summary="""
            Este informe presenta un análisis exhaustivo de las ventas
            durante el año fiscal 2024.
            
            Incluye:
            • Análisis de tendencias
            • Comparativas por región
            • Proyecciones para 2025
            """,
            dataframe=df.head(10)
        )
        print("✅ Generado: 04e_reporte_completo.pdf")
    else:
        print(f"⚠️  Portada no encontrada: {portada}")
    
    # =========================================================================
    # EJEMPLO 6: Múltiples secciones CUSTOM
    # =========================================================================
    
    sections_multi_custom = [
        SectionConfig(SectionType.SUMMARY),
        SectionConfig(
            SectionType.CUSTOM,
            custom_content="SECCIÓN 1: Introducción\n\nEsta es la primera sección personalizada."
        ),
        SectionConfig(
            SectionType.CUSTOM,
            custom_content="SECCIÓN 2: Desarrollo\n\nEsta es la segunda sección personalizada."
        ),
        SectionConfig(SectionType.DATA),
        SectionConfig(
            SectionType.CUSTOM,
            custom_content="SECCIÓN 3: Conclusiones\n\nEsta es la tercera sección personalizada."
        ),
    ]
    
    template_multi = ReportTemplate(
        sections=sections_multi_custom,
        primary_color="#f39c12",
    )
    
    generator = ReportGenerator(output_dir / "04f_multi_custom.pdf", template_multi)
    generator.build_with_sections(
        title="Reporte con Múltiples Secciones Custom",
        summary="Demostración de múltiples secciones CUSTOM intercaladas.",
        dataframe=df.head(3)
    )
    print("✅ Generado: 04f_multi_custom.pdf")
    
    print(f"\n📁 Todos los reportes generados en: {output_dir}/")


if __name__ == "__main__":
    main()
