"""
Ejemplo 02: Configuración de Logo en Pie de Página
==================================================

Este ejemplo demuestra las diferentes opciones de configuración del logo
en el pie de página de los reportes PDF.

Características demostradas:
- Logo por defecto del paquete qry-doc
- Logo personalizado con ruta custom
- Diferentes posiciones: BOTTOM_RIGHT, BOTTOM_LEFT, BOTTOM_CENTER
- Dimensiones personalizables
- Desactivación del logo
"""

from pathlib import Path
import pandas as pd

from qry_doc import ReportTemplate, ReportGenerator, LogoPosition


def crear_reporte(output_path: Path, template: ReportTemplate, titulo: str, descripcion: str):
    """Función auxiliar para crear reportes con diferentes configuraciones."""
    df = pd.read_csv("examples/data/ventas.csv")
    
    generator = ReportGenerator(output_path, template=template)
    generator.build(
        title=titulo,
        summary=descripcion,
        dataframe=df.head(5)
    )
    print(f"✅ Generado: {output_path}")


def main():
    # Crear directorio de salida
    output_dir = Path("output/footer_logos")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logo_custom = Path("public/logo_op.png")
    
    # =========================================================================
    # EJEMPLO 1: Logo por defecto (incluido en qry-doc)
    # =========================================================================
    
    template_default = ReportTemplate(
        # footer_logo_enabled=True es el valor por defecto
        # footer_logo_path=None usa el logo por defecto del paquete
        footer_logo_position=LogoPosition.BOTTOM_RIGHT,  # Posición por defecto
        primary_color="#2c3e50",
    )
    
    crear_reporte(
        output_dir / "02a_logo_default.pdf",
        template_default,
        "Reporte con Logo por Defecto",
        """
        Este reporte utiliza el logo por defecto incluido en el paquete qry-doc.
        El logo aparece en la esquina inferior derecha de cada página.
        
        No es necesario especificar ninguna ruta de imagen.
        """
    )
    
    # =========================================================================
    # EJEMPLO 2: Logo personalizado
    # =========================================================================
    
    if logo_custom.exists():
        template_custom = ReportTemplate(
            footer_logo_path=logo_custom,  # Tu logo personalizado
            footer_logo_position=LogoPosition.BOTTOM_RIGHT,
            footer_logo_width=60.0,   # Ancho en puntos
            footer_logo_height=30.0,  # Alto en puntos
            primary_color="#e74c3c",
        )
        
        crear_reporte(
            output_dir / "02b_logo_custom.pdf",
            template_custom,
            "Reporte con Logo Personalizado",
            """
            Este reporte utiliza un logo personalizado de tu marca.
            Puedes especificar cualquier imagen PNG o JPG.
            
            Las dimensiones son configurables para ajustarse a tu diseño.
            """
        )
    else:
        print(f"⚠️  Logo personalizado no encontrado: {logo_custom}")
    
    # =========================================================================
    # EJEMPLO 3: Logo en diferentes posiciones
    # =========================================================================
    
    # Posición: Inferior izquierda
    template_left = ReportTemplate(
        footer_logo_position=LogoPosition.BOTTOM_LEFT,
        primary_color="#27ae60",
    )
    
    crear_reporte(
        output_dir / "02c_logo_izquierda.pdf",
        template_left,
        "Logo en Esquina Inferior Izquierda",
        """
        El logo puede posicionarse en la esquina inferior izquierda
        usando LogoPosition.BOTTOM_LEFT.
        
        Útil cuando el número de página está a la derecha.
        """
    )
    
    # Posición: Centro inferior
    template_center = ReportTemplate(
        footer_logo_position=LogoPosition.BOTTOM_CENTER,
        primary_color="#9b59b6",
    )
    
    crear_reporte(
        output_dir / "02d_logo_centro.pdf",
        template_center,
        "Logo Centrado en el Pie de Página",
        """
        El logo puede centrarse en el pie de página usando
        LogoPosition.BOTTOM_CENTER.
        
        Ideal para diseños simétricos y minimalistas.
        """
    )
    
    # =========================================================================
    # EJEMPLO 4: Sin logo (desactivado)
    # =========================================================================
    
    template_sin_logo = ReportTemplate(
        footer_logo_enabled=False,  # Desactiva el logo completamente
        primary_color="#34495e",
    )
    
    crear_reporte(
        output_dir / "02e_sin_logo.pdf",
        template_sin_logo,
        "Reporte sin Logo en Pie de Página",
        """
        El logo del pie de página puede desactivarse completamente
        estableciendo footer_logo_enabled=False.
        
        Solo se mostrará el número de página.
        """
    )
    
    # =========================================================================
    # EJEMPLO 5: Logo con dimensiones grandes
    # =========================================================================
    
    template_grande = ReportTemplate(
        footer_logo_width=80.0,   # Logo más grande
        footer_logo_height=40.0,
        footer_logo_position=LogoPosition.BOTTOM_RIGHT,
        primary_color="#f39c12",
    )
    
    crear_reporte(
        output_dir / "02f_logo_grande.pdf",
        template_grande,
        "Reporte con Logo Grande",
        """
        Las dimensiones del logo son completamente configurables.
        
        footer_logo_width y footer_logo_height permiten ajustar
        el tamaño según las necesidades de tu marca.
        """
    )
    
    print(f"\n📁 Todos los reportes generados en: {output_dir}/")


if __name__ == "__main__":
    main()
