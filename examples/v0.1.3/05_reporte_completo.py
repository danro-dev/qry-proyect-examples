"""
Ejemplo 05: Reporte Profesional Completo
========================================

Este ejemplo combina TODAS las nuevas características de qry-doc v0.1.3
para crear un reporte PDF profesional completo.

Características combinadas:
- ✅ Portada con imagen personalizada
- ✅ Logo en pie de página (personalizado o default)
- ✅ Fuentes personalizadas (si están disponibles)
- ✅ Sistema de secciones con orden personalizado
- ✅ Secciones CUSTOM para contenido adicional
- ✅ Colores corporativos

Este es el ejemplo más completo y representa un caso de uso real
para reportes empresariales.
"""

from pathlib import Path
import pandas as pd
from datetime import datetime

from qry_doc import (
    ReportTemplate, 
    SectionType, 
    SectionConfig,
    LogoPosition
)
from qry_doc.report_generator import ReportGenerator


def main():
    # =========================================================================
    # CONFIGURACIÓN DE RUTAS
    # =========================================================================
    
    output_path = Path("output/05_reporte_profesional.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    portada = Path("public/portada.png")
    logo = Path("public/logo_op.png")
    data_path = Path("examples/data/ventas.csv")
    
    # Verificar archivos necesarios
    if not portada.exists():
        print(f"⚠️  Portada no encontrada: {portada}")
        print("   El reporte se generará sin portada.")
        portada = None
    
    if not logo.exists():
        print(f"⚠️  Logo no encontrado: {logo}")
        print("   Se usará el logo por defecto.")
        logo = None
    
    # =========================================================================
    # CARGAR Y PREPARAR DATOS
    # =========================================================================
    
    df = pd.read_csv(data_path)
    fecha_actual = datetime.now().strftime("%d de %B de %Y")
    
    # =========================================================================
    # DEFINIR ESTRUCTURA DE SECCIONES
    # =========================================================================
    
    sections = [
        # 1. Portada (si hay imagen)
        SectionConfig(SectionType.COVER),
        
        # 2. Resumen ejecutivo
        SectionConfig(SectionType.SUMMARY),
        
        # 3. Índice / Tabla de contenidos
        SectionConfig(
            SectionType.CUSTOM,
            custom_content=f"""
            INFORMACIÓN DEL DOCUMENTO
            
            Fecha de generación: {fecha_actual}
            Versión: 1.0
            Clasificación: Interno
            
            CONTENIDO
            
            1. Resumen Ejecutivo
            2. Análisis de Datos
            3. Metodología
            4. Conclusiones y Recomendaciones
            """
        ),
        
        # 4. Datos principales
        SectionConfig(SectionType.DATA),
        
        # 5. Metodología
        SectionConfig(
            SectionType.CUSTOM,
            custom_content="""
            METODOLOGÍA
            
            Este análisis fue realizado utilizando las siguientes técnicas:
            
            • Análisis descriptivo de datos históricos
            • Comparación interanual de métricas clave
            • Segmentación por categorías de producto
            • Análisis de tendencias temporales
            
            Los datos fueron procesados con Python utilizando las librerías
            pandas para manipulación de datos y qry-doc para la generación
            de este reporte.
            
            Período de análisis: Q4 2024
            Fuente de datos: Sistema ERP corporativo
            """
        ),
        
        # 6. Conclusiones
        SectionConfig(
            SectionType.CUSTOM,
            custom_content="""
            CONCLUSIONES Y RECOMENDACIONES
            
            Basándonos en el análisis realizado, se presentan las siguientes
            conclusiones:
            
            1. CRECIMIENTO SOSTENIDO
               Las ventas muestran una tendencia positiva del 15% respecto
               al período anterior.
            
            2. PRODUCTOS ESTRELLA
               La categoría de electrónicos lidera las ventas con un 40%
               del total facturado.
            
            3. OPORTUNIDADES DE MEJORA
               Se identifican oportunidades en la región Sur que presenta
               menor penetración de mercado.
            
            RECOMENDACIONES
            
            • Incrementar inversión en marketing digital
            • Expandir la línea de productos electrónicos
            • Desarrollar estrategia específica para región Sur
            • Implementar programa de fidelización de clientes
            
            Para más información, contactar al departamento de análisis.
            """
        ),
    ]
    
    # =========================================================================
    # CONFIGURAR TEMPLATE PROFESIONAL
    # =========================================================================
    
    template = ReportTemplate(
        # Portada
        cover_image_path=portada,
        
        # Logo en pie de página
        footer_logo_path=logo,
        footer_logo_enabled=True,
        footer_logo_position=LogoPosition.BOTTOM_RIGHT,
        footer_logo_width=50.0,
        footer_logo_height=25.0,
        
        # Colores corporativos
        primary_color="#1a1a2e",  # Azul oscuro profesional
        
        # Estructura de secciones
        sections=sections,
    )
    
    # =========================================================================
    # GENERAR EL REPORTE
    # =========================================================================
    
    print("🔄 Generando reporte profesional...")
    
    generator = ReportGenerator(output_path, template=template)
    
    generator.build_with_sections(
        title="Informe de Análisis de Ventas Q4 2024",
        summary="""
        RESUMEN EJECUTIVO
        
        Este informe presenta un análisis exhaustivo del desempeño comercial
        durante el cuarto trimestre del año fiscal 2024. Los resultados
        demuestran un crecimiento sostenido en las principales líneas de
        negocio, superando las proyecciones establecidas al inicio del período.
        
        HALLAZGOS PRINCIPALES
        
        • Crecimiento del 15% en ventas totales vs Q3 2024
        • Laptop Pro se consolida como producto líder con 1,234 unidades
        • Expansión exitosa en 3 nuevos mercados regionales
        • Mejora del 8% en el margen de contribución
        
        PERSPECTIVAS
        
        Las proyecciones para Q1 2025 son optimistas, con un crecimiento
        esperado del 10-12% basado en las tendencias actuales y la
        estacionalidad histórica del mercado.
        """,
        dataframe=df.head(15)  # Top 15 registros
    )
    
    # =========================================================================
    # RESUMEN DE GENERACIÓN
    # =========================================================================
    
    print(f"\n{'='*60}")
    print("✅ REPORTE GENERADO EXITOSAMENTE")
    print(f"{'='*60}")
    print(f"📄 Archivo: {output_path}")
    print(f"📅 Fecha: {fecha_actual}")
    print(f"\n📋 Características utilizadas:")
    print(f"   • Portada: {'✅ Sí' if portada else '❌ No'}")
    print(f"   • Logo footer: {'✅ Personalizado' if logo else '✅ Por defecto'}")
    print(f"   • Secciones: {len(sections)} configuradas")
    print(f"   • Datos: {len(df.head(15))} registros incluidos")
    print(f"\n💡 Abre el PDF para ver el resultado final.")


if __name__ == "__main__":
    main()
