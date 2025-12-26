"""
Ejemplo 01: Portada Básica en Reportes PDF
==========================================

Este ejemplo demuestra cómo agregar una imagen de portada a página completa
en los reportes PDF generados con qry-doc v0.1.3.

La portada se muestra como primera página del documento, escalada automáticamente
para ajustarse al tamaño de página manteniendo la relación de aspecto.

Características demostradas:
- cover_image_path: Ruta a la imagen de portada
- Escalado automático de imagen
- Integración con el resto del reporte
"""

from pathlib import Path
import pandas as pd

from qry_doc import ReportTemplate
from qry_doc.report_generator import ReportGenerator


def main():
    # Rutas de archivos
    portada_path = Path("public/portada.png")
    output_path = Path("output/01_reporte_con_portada.pdf")
    data_path = Path("examples/data/ventas.csv")
    
    # Verificar que existe la portada
    if not portada_path.exists():
        print(f"⚠️  No se encontró la portada en: {portada_path}")
        print("   Asegúrate de tener el archivo portada.png en la carpeta public/")
        return
    
    # Crear directorio de salida si no existe
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Cargar datos de ejemplo
    df = pd.read_csv(data_path)
    
    # =========================================================================
    # CONFIGURACIÓN DE TEMPLATE CON PORTADA
    # =========================================================================
    
    template = ReportTemplate(
        # Configurar la imagen de portada
        cover_image_path=portada_path,
        
        # Configuración básica del reporte
        primary_color="#1a1a2e",
        title_font="Helvetica-Bold",
        body_font="Helvetica",
    )
    
    # =========================================================================
    # GENERAR EL REPORTE
    # =========================================================================
    
    generator = ReportGenerator(output_path, template=template)
    
    # Construir el reporte con portada
    generator.build(
        title="Informe de Ventas Q4 2024",
        summary="""
        Este informe presenta un análisis detallado de las ventas del cuarto 
        trimestre de 2024. Los datos muestran un crecimiento sostenido en 
        todas las categorías de productos.
        
        Puntos destacados:
        • Incremento del 15% respecto al trimestre anterior
        • Laptop Pro se mantiene como producto líder
        • Expansión exitosa en nuevos mercados
        """,
        dataframe=df.head(10)  # Primeras 10 filas como muestra
    )
    
    print(f"✅ Reporte generado exitosamente: {output_path}")
    print(f"   - Portada: {portada_path}")
    print(f"   - Páginas: Portada + contenido")


if __name__ == "__main__":
    main()
