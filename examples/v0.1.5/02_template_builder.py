"""
Ejemplo 02: Templates Personalizados con TemplateBuilder
========================================================

Este ejemplo demuestra cómo crear templates de reportes usando TemplateBuilder,
la nueva API fluida introducida en qry-doc v0.1.5.

Características demostradas:
- API fluida encadenable
- Configuración de colores, fuentes y márgenes
- Configuración de header y footer
- Sistema de secciones
- Integración con CoverBuilder
"""

from pathlib import Path
import pandas as pd

from qry_doc import (
    QryDoc,
    TemplateBuilder,
    SectionConfig,
    SectionType,
    LogoPosition,
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
    
    # =========================================================================
    # EJEMPLO 1: Template básico
    # =========================================================================
    
    template_basico = (
        qry.create_template()
        .with_colors(primary="#003366")
        .with_fonts(title_font="Helvetica-Bold", body_font="Helvetica")
    )
    
    qry.generate_report_with_builder(
        output_dir / "02a_template_basico.pdf",
        template=template_basico,
        title="Reporte con Template Básico"
    )
    print("✅ 02a_template_basico.pdf generado")
    
    # =========================================================================
    # EJEMPLO 2: Template con márgenes personalizados
    # =========================================================================
    
    template_margenes = (
        qry.create_template()
        .with_colors(primary="#006666", secondary="#00A3A3")
        .with_margins(top=100, bottom=80, left=72, right=72)
    )
    
    qry.generate_report_with_builder(
        output_dir / "02b_template_margenes.pdf",
        template=template_margenes,
        title="Reporte con Márgenes Personalizados"
    )
    print("✅ 02b_template_margenes.pdf generado")
    
    # =========================================================================
    # EJEMPLO 3: Template con footer personalizado
    # =========================================================================
    
    template_footer = (
        qry.create_template()
        .with_colors(primary="#5C2D91")
        .with_footer(
            logo_position=LogoPosition.BOTTOM_CENTER,
            logo_width=100,
            logo_height=50,
            height=40
        )
    )
    
    qry.generate_report_with_builder(
        output_dir / "02c_template_footer.pdf",
        template=template_footer,
        title="Reporte con Footer Personalizado"
    )
    print("✅ 02c_template_footer.pdf generado")
    
    # =========================================================================
    # EJEMPLO 4: Template con secciones personalizadas
    # =========================================================================
    
    template_secciones = (
        qry.create_template()
        .with_colors(primary="#E65100")
        .with_sections([
            SectionConfig(SectionType.SUMMARY),
            SectionConfig(SectionType.DATA),
            SectionConfig(
                SectionType.CUSTOM,
                custom_content="Este es un contenido personalizado añadido al final del reporte."
            ),
        ])
    )
    
    qry.generate_report_with_builder(
        output_dir / "02d_template_secciones.pdf",
        template=template_secciones,
        title="Reporte con Secciones Personalizadas"
    )
    print("✅ 02d_template_secciones.pdf generado")
    
    # =========================================================================
    # EJEMPLO 5: Template completo
    # =========================================================================
    
    template_completo = (
        qry.create_template()
        .with_colors(primary="#1A237E", secondary="#C9A227")
        .with_fonts(title_font="Helvetica-Bold", body_font="Helvetica")
        .with_margins(top=80, bottom=80, left=72, right=72)
        .with_footer(
            logo_position=LogoPosition.BOTTOM_RIGHT,
            logo_width=120,
            logo_height=60
        )
        .with_sections([
            SectionConfig(SectionType.SUMMARY),
            SectionConfig(SectionType.DATA),
        ])
    )
    
    # Combinar con CoverBuilder
    cover = (
        qry.create_cover()
        .set_title("Informe Completo", color="#1A237E")
        .set_subtitle("Con Template Personalizado")
        .set_author("Equipo de Desarrollo")
    )
    
    qry.generate_report_with_builder(
        output_dir / "02e_template_completo.pdf",
        cover=cover,
        template=template_completo,
        title="Informe Completo"
    )
    print("✅ 02e_template_completo.pdf generado")
    
    print(f"\n📁 Todos los reportes guardados en: {output_dir}")


if __name__ == "__main__":
    main()
