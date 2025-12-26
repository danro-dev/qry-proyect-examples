"""
Ejemplo 01: Portadas Dinámicas con CoverBuilder
===============================================

Este ejemplo demuestra cómo crear portadas personalizadas usando CoverBuilder,
la nueva API fluida introducida en qry-doc v0.1.5.

Características demostradas:
- API fluida para configurar portadas
- Posicionamiento preciso de elementos
- Estilos personalizados (colores, fuentes, tamaños)
- Textos personalizados adicionales
- Colores de fondo
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

from qry_doc import QryDoc, TextAlignment
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
    # EJEMPLO 1: Portada básica
    # =========================================================================
    
    cover_basica = (
        qry.create_cover()
        .set_title("Reporte de Ventas 2024")
        .set_subtitle("Análisis Trimestral Q4")
        .set_date(datetime.now())
        .set_author("Equipo de Análisis de Datos")
    )
    
    qry.generate_report_with_builder(
        output_dir / "01a_portada_basica.pdf",
        cover=cover_basica,
        title="Reporte Q4 2024"
    )
    print("✅ 01a_portada_basica.pdf generado")
    
    # =========================================================================
    # EJEMPLO 2: Portada con estilos personalizados
    # =========================================================================
    
    cover_personalizada = (
        qry.create_cover()
        .set_title(
            "Informe Ejecutivo",
            font_size=48,
            color="#003366",
            font_family="Helvetica-Bold"
        )
        .set_subtitle(
            "Resultados del Cuarto Trimestre",
            font_size=24,
            color="#666666"
        )
        .set_date(
            datetime.now(),
            format="%d de %B, %Y",
            font_size=14,
            color="#999999"
        )
        .set_author(
            "Departamento de Finanzas",
            font_size=14,
            color="#999999"
        )
    )
    
    qry.generate_report_with_builder(
        output_dir / "01b_portada_personalizada.pdf",
        cover=cover_personalizada,
        title="Informe Ejecutivo Q4"
    )
    print("✅ 01b_portada_personalizada.pdf generado")
    
    # =========================================================================
    # EJEMPLO 3: Portada con posiciones exactas
    # =========================================================================
    
    cover_posicionada = (
        qry.create_cover()
        .set_title(
            "Análisis de Mercado",
            x=306.0,  # Centrado horizontalmente
            y=600.0,  # Parte superior
            font_size=42,
            alignment=TextAlignment.CENTER
        )
        .set_subtitle(
            "Tendencias y Proyecciones",
            x=306.0,
            y=550.0,
            alignment=TextAlignment.CENTER
        )
        .set_date(
            "Diciembre 2024",
            x=72.0,   # Margen izquierdo
            y=72.0,   # Margen inferior
            alignment=TextAlignment.LEFT
        )
        .set_author(
            "Equipo de Estrategia",
            x=540.0,  # Cerca del margen derecho
            y=72.0,
            alignment=TextAlignment.RIGHT
        )
    )
    
    qry.generate_report_with_builder(
        output_dir / "01c_portada_posicionada.pdf",
        cover=cover_posicionada,
        title="Análisis de Mercado"
    )
    print("✅ 01c_portada_posicionada.pdf generado")
    
    # =========================================================================
    # EJEMPLO 4: Portada completa con textos adicionales
    # =========================================================================
    
    cover_completa = (
        qry.create_cover()
        .set_title("Reporte Anual 2024", font_size=48, color="#1A237E")
        .set_subtitle("Resumen Ejecutivo", font_size=28, color="#3949AB")
        .add_custom_text(
            "CONFIDENCIAL",
            x=306.0,
            y=750.0,
            font_size=12,
            color="#FF0000",
            alignment=TextAlignment.CENTER
        )
        .add_custom_text(
            "Versión 1.0",
            x=540.0,
            y=50.0,
            font_size=10,
            color="#999999",
            alignment=TextAlignment.RIGHT
        )
        .set_date(datetime.now())
        .set_author("División Corporativa")
        .set_background_color("#F5F5F5")
    )
    
    qry.generate_report_with_builder(
        output_dir / "01d_portada_completa.pdf",
        cover=cover_completa,
        title="Reporte Anual"
    )
    print("✅ 01d_portada_completa.pdf generado")
    
    print(f"\n📁 Todos los reportes guardados en: {output_dir}")


if __name__ == "__main__":
    main()
