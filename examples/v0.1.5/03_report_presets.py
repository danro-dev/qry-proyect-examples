"""
Ejemplo 03: Presets por Industria
=================================

Este ejemplo demuestra cómo usar ReportPresets para crear reportes
con estilos predefinidos optimizados para diferentes industrias.

Características demostradas:
- Uso de presets predefinidos
- Listar presets disponibles
- Personalizar presets con overrides
- TemplateBuilder.from_preset()
"""

from pathlib import Path
import pandas as pd

from qry_doc import (
    QryDoc,
    ReportPreset,
    ReportPresetType,
    TemplateBuilder,
    SectionConfig,
    SectionType,
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
    # LISTAR PRESETS DISPONIBLES
    # =========================================================================
    
    print("\n📋 Presets disponibles:")
    print("-" * 60)
    for name, description in ReportPreset.list_all():
        print(f"• {name}")
        print(f"  {description[:60]}...")
    print()
    
    # =========================================================================
    # EJEMPLO 1: Preset FINANCIAL
    # =========================================================================
    
    template_financial = TemplateBuilder.from_preset(ReportPresetType.FINANCIAL)
    
    qry.generate_report_with_builder(
        output_dir / "03a_preset_financial.pdf",
        template=template_financial,
        title="Reporte Financiero Q4 2024"
    )
    print("✅ 03a_preset_financial.pdf generado")
    
    # =========================================================================
    # EJEMPLO 2: Preset HEALTHCARE
    # =========================================================================
    
    template_healthcare = TemplateBuilder.from_preset(ReportPresetType.HEALTHCARE)
    
    qry.generate_report_with_builder(
        output_dir / "03b_preset_healthcare.pdf",
        template=template_healthcare,
        title="Informe de Indicadores de Salud"
    )
    print("✅ 03b_preset_healthcare.pdf generado")
    
    # =========================================================================
    # EJEMPLO 3: Preset TECHNOLOGY
    # =========================================================================
    
    template_technology = TemplateBuilder.from_preset(ReportPresetType.TECHNOLOGY)
    
    qry.generate_report_with_builder(
        output_dir / "03c_preset_technology.pdf",
        template=template_technology,
        title="Dashboard de Métricas Tech"
    )
    print("✅ 03c_preset_technology.pdf generado")
    
    # =========================================================================
    # EJEMPLO 4: Preset RETAIL
    # =========================================================================
    
    template_retail = TemplateBuilder.from_preset(ReportPresetType.RETAIL)
    
    qry.generate_report_with_builder(
        output_dir / "03d_preset_retail.pdf",
        template=template_retail,
        title="Análisis de Ventas Retail"
    )
    print("✅ 03d_preset_retail.pdf generado")
    
    # =========================================================================
    # EJEMPLO 5: Preset MANUFACTURING
    # =========================================================================
    
    template_manufacturing = TemplateBuilder.from_preset(ReportPresetType.MANUFACTURING)
    
    qry.generate_report_with_builder(
        output_dir / "03e_preset_manufacturing.pdf",
        template=template_manufacturing,
        title="Reporte de Producción Industrial"
    )
    print("✅ 03e_preset_manufacturing.pdf generado")
    
    # =========================================================================
    # EJEMPLO 6: Preset CONSULTING
    # =========================================================================
    
    template_consulting = TemplateBuilder.from_preset(ReportPresetType.CONSULTING)
    
    qry.generate_report_with_builder(
        output_dir / "03f_preset_consulting.pdf",
        template=template_consulting,
        title="Informe de Consultoría Estratégica"
    )
    print("✅ 03f_preset_consulting.pdf generado")
    
    # =========================================================================
    # EJEMPLO 7: Preset personalizado con overrides
    # =========================================================================
    
    template_personalizado = (
        TemplateBuilder.from_preset(ReportPresetType.FINANCIAL)
        .with_colors(primary="#001122", secondary="#003366")
        .with_margins(top=100, bottom=80)
        .with_sections([
            SectionConfig(SectionType.SUMMARY),
            SectionConfig(SectionType.DATA),
        ])
    )
    
    cover = (
        qry.create_cover()
        .set_title("Informe Financiero Personalizado", color="#001122")
        .set_subtitle("Con overrides de preset")
        .set_author("Departamento de Finanzas")
    )
    
    qry.generate_report_with_builder(
        output_dir / "03g_preset_personalizado.pdf",
        cover=cover,
        template=template_personalizado,
        title="Informe Financiero Personalizado"
    )
    print("✅ 03g_preset_personalizado.pdf generado")
    
    # =========================================================================
    # MOSTRAR DETALLES DE UN PRESET
    # =========================================================================
    
    print("\n📊 Detalles del preset FINANCIAL:")
    preset = ReportPreset.get(ReportPresetType.FINANCIAL)
    print(f"   Nombre: {preset.name}")
    print(f"   Color primario: {preset.primary_color}")
    print(f"   Color secundario: {preset.secondary_color}")
    print(f"   Fuente títulos: {preset.title_font}")
    print(f"   Secciones: {len(preset.default_sections)}")
    
    print(f"\n📁 Todos los reportes guardados en: {output_dir}")


if __name__ == "__main__":
    main()
