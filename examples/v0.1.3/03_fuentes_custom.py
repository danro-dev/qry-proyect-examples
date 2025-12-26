"""
Ejemplo 03: Fuentes Personalizadas (TTF/OTF)
============================================

Este ejemplo demuestra cómo usar fuentes personalizadas en los reportes PDF.
qry-doc v0.1.3 soporta fuentes TrueType (.ttf) y OpenType (.otf).

Características demostradas:
- custom_title_font_path: Fuente para títulos y encabezados
- custom_body_font_path: Fuente para el cuerpo del texto
- Fallback automático a Helvetica si la fuente es inválida
- Validación de rutas de fuentes

Nota: Para ejecutar este ejemplo necesitas tener archivos de fuentes TTF/OTF.
      Puedes descargar fuentes gratuitas de Google Fonts (fonts.google.com).
"""

from pathlib import Path
import pandas as pd

from qry_doc import ReportTemplate
from qry_doc.report_generator import ReportGenerator


def main():
    # Crear directorio de salida
    output_dir = Path("output/fuentes")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Rutas a fuentes personalizadas (ajusta según tus archivos)
    # Puedes descargar estas fuentes de fonts.google.com
    fonts_dir = Path("fonts")
    
    # Cargar datos
    df = pd.read_csv("examples/data/ventas.csv")
    
    # =========================================================================
    # EJEMPLO 1: Fuentes por defecto (Helvetica)
    # =========================================================================
    
    template_default = ReportTemplate(
        # Sin fuentes personalizadas, usa Helvetica
        title_font="Helvetica-Bold",
        body_font="Helvetica",
        primary_color="#2c3e50",
    )
    
    generator = ReportGenerator(output_dir / "03a_fuentes_default.pdf", template_default)
    generator.build(
        title="Reporte con Fuentes por Defecto",
        summary="""
        Este reporte utiliza las fuentes por defecto de ReportLab:
        Helvetica-Bold para títulos y Helvetica para el cuerpo.
        
        Estas fuentes están siempre disponibles y no requieren
        archivos externos.
        """,
        dataframe=df.head(5)
    )
    print("✅ Generado: 03a_fuentes_default.pdf")
    
    # =========================================================================
    # EJEMPLO 2: Fuentes personalizadas (si existen)
    # =========================================================================
    
    # Buscar fuentes disponibles en el sistema
    posibles_fuentes = [
        fonts_dir / "Montserrat-Bold.ttf",
        fonts_dir / "Montserrat-Regular.ttf",
        fonts_dir / "OpenSans-Bold.ttf",
        fonts_dir / "OpenSans-Regular.ttf",
        fonts_dir / "Roboto-Bold.ttf",
        fonts_dir / "Roboto-Regular.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    
    title_font = None
    body_font = None
    
    for font in posibles_fuentes:
        if font.exists():
            if "Bold" in font.name and title_font is None:
                title_font = font
            elif "Bold" not in font.name and body_font is None:
                body_font = font
    
    if title_font and body_font:
        template_custom = ReportTemplate(
            custom_title_font_path=title_font,
            custom_body_font_path=body_font,
            primary_color="#e74c3c",
        )
        
        generator = ReportGenerator(output_dir / "03b_fuentes_custom.pdf", template_custom)
        generator.build(
            title="Reporte con Fuentes Personalizadas",
            summary=f"""
            Este reporte utiliza fuentes personalizadas:
            
            • Títulos: {title_font.name}
            • Cuerpo: {body_font.name}
            
            Las fuentes personalizadas permiten mantener la identidad
            visual de tu marca en todos los documentos generados.
            """,
            dataframe=df.head(5)
        )
        print(f"✅ Generado: 03b_fuentes_custom.pdf")
        print(f"   - Fuente títulos: {title_font}")
        print(f"   - Fuente cuerpo: {body_font}")
    else:
        print("⚠️  No se encontraron fuentes personalizadas.")
        print("   Para usar fuentes custom, descarga archivos TTF de fonts.google.com")
        print(f"   y colócalos en: {fonts_dir}/")
    
    # =========================================================================
    # EJEMPLO 3: Demostración de fallback automático
    # =========================================================================
    
    # Usar una ruta inválida para demostrar el fallback
    template_fallback = ReportTemplate(
        custom_title_font_path=Path("fuente_inexistente.ttf"),  # No existe
        custom_body_font_path=Path("otra_fuente_inexistente.ttf"),  # No existe
        primary_color="#27ae60",
    )
    
    generator = ReportGenerator(output_dir / "03c_fuentes_fallback.pdf", template_fallback)
    generator.build(
        title="Reporte con Fallback de Fuentes",
        summary="""
        Este reporte demuestra el comportamiento de fallback.
        
        Cuando se especifica una fuente que no existe o es inválida,
        qry-doc automáticamente usa Helvetica como respaldo.
        
        Esto garantiza que los reportes siempre se generen correctamente,
        incluso si hay problemas con las fuentes personalizadas.
        """,
        dataframe=df.head(5)
    )
    print("✅ Generado: 03c_fuentes_fallback.pdf (con fallback a Helvetica)")
    
    # =========================================================================
    # EJEMPLO 4: Solo fuente de títulos personalizada
    # =========================================================================
    
    if title_font:
        template_solo_titulo = ReportTemplate(
            custom_title_font_path=title_font,
            # body_font usa Helvetica por defecto
            primary_color="#9b59b6",
        )
        
        generator = ReportGenerator(output_dir / "03d_solo_titulo_custom.pdf", template_solo_titulo)
        generator.build(
            title="Solo Títulos Personalizados",
            summary="""
            Puedes personalizar solo la fuente de títulos y mantener
            Helvetica para el cuerpo del texto.
            
            Esto es útil cuando quieres destacar los encabezados
            con una fuente distintiva de tu marca.
            """,
            dataframe=df.head(5)
        )
        print("✅ Generado: 03d_solo_titulo_custom.pdf")
    
    print(f"\n📁 Todos los reportes generados en: {output_dir}/")
    print("\n💡 Tip: Descarga fuentes gratuitas de https://fonts.google.com")


if __name__ == "__main__":
    main()
