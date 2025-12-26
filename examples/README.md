# Ejemplos y Guías de qry-doc

Esta carpeta contiene ejemplos prácticos y guías detalladas para usar qry-doc.

## Contenido

| Archivo | Descripción |
|---------|-------------|
| [01_inicio_rapido.py](01_inicio_rapido.py) | Primeros pasos con qry-doc |
| [02_consultas_basicas.py](02_consultas_basicas.py) | Cómo hacer preguntas sobre tus datos |
| [03_exportar_csv.py](03_exportar_csv.py) | Exportar resultados a archivos CSV |
| [04_generar_reportes.py](04_generar_reportes.py) | Crear reportes PDF profesionales |
| [05_templates_personalizados.py](05_templates_personalizados.py) | Personalizar el estilo de reportes |
| [06_manejo_errores.py](06_manejo_errores.py) | Gestión de errores y excepciones |
| [07_diferentes_llms.py](07_diferentes_llms.py) | Usar diferentes proveedores de IA |

## Datos de ejemplo

La carpeta `data/` contiene archivos CSV de ejemplo para practicar:

- `ventas.csv` - Datos de ventas ficticios
- `clientes.csv` - Base de datos de clientes
- `productos.csv` - Catálogo de productos

## Requisitos

```bash
# Instalar qry-doc
pip install qry-doc

# O con uv
uv add qry-doc
```

## Configuración

Antes de ejecutar los ejemplos, configura tu API key:

```bash
export OPENAI_API_KEY="sk-tu-api-key"
```

O usa otro proveedor LLM (ver `07_diferentes_llms.py`).
