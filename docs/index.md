# qry-doc

<p align="center">
  <img src="assets/logo.png" alt="qry-doc" width="400">
</p>

<p align="center">
  <strong>Motor de análisis generativo para consultas en lenguaje natural</strong>
</p>

<p align="center">
  <a href="getting-started/installation/">Instalación</a> •
  <a href="getting-started/quickstart/">Inicio Rápido</a> •
  <a href="api/qrydoc/">API</a> •
  <a href="changelog/">Changelog</a>
</p>

---

**qry-doc** transforma el lenguaje natural en código ejecutable, visualizaciones y reportes PDF profesionales. Simplifica radicalmente la interacción con archivos CSV y bases de datos SQL.

```python
from qry_doc import QryDoc, ReportTemplate
import pandasai as pai
from pandasai_openai import OpenAI

# Configurar LLM
llm = OpenAI()
pai.config.set({"llm": llm})

qry = QryDoc("ventas.csv", llm=llm)

# Pregunta en español
respuesta = qry.ask("¿Cuál fue el producto más vendido en 2024?")
print(respuesta)  # "El producto más vendido fue 'Laptop Pro' con 1,234 unidades"

# Genera reporte PDF profesional
qry.generate_report("Análisis trimestral de ventas", "reporte_q4.pdf")
```

## ✨ Características

<div class="grid cards" markdown>

-   :speech_balloon: **Consultas en Lenguaje Natural**

    ---

    Pregunta sobre tus datos como si hablaras con un analista

-   :bar_chart: **Visualizaciones Automáticas**

    ---

    Genera gráficos relevantes sin escribir código

-   :page_facing_up: **Reportes PDF Profesionales**

    ---

    Crea documentos con tablas, gráficos y resúmenes

-   :file_folder: **Exportación CSV**

    ---

    Extrae resultados tabulares con encoding Excel-compatible

</div>

## 🆕 Novedades en v0.1.3

La versión 0.1.3 introduce mejoras significativas en la generación de PDFs:

| Característica | Descripción |
|----------------|-------------|
| :framed_picture: **Portadas** | Imágenes de portada a página completa |
| :label: **Footer Logo** | Logo en pie de página (default o personalizado) |
| :pencil2: **Fuentes Custom** | Soporte para fuentes TTF/OTF |
| :bookmark_tabs: **Secciones** | Sistema de secciones personalizables |

[Ver changelog completo](changelog.md){ .md-button }

## 🚀 Inicio Rápido

=== "Con uv (recomendado)"

    ```bash
    uv add qry-doc
    ```

=== "Con pip"

    ```bash
    pip install qry-doc
    ```

```python
from qry_doc import QryDoc, ReportTemplate
import pandasai as pai
from pandasai_openai import OpenAI

# Configurar
llm = OpenAI()
pai.config.set({"llm": llm})

# Crear instancia
qry = QryDoc("datos.csv", llm=llm)

# Hacer preguntas
respuesta = qry.ask("¿Cuántos registros hay?")
print(respuesta)
```

[Guía de instalación completa](getting-started/installation.md){ .md-button .md-button--primary }

## 📚 Documentación

- **[Instalación](getting-started/installation.md)** - Cómo instalar qry-doc
- **[Inicio Rápido](getting-started/quickstart.md)** - Tu primer reporte en 5 minutos
- **[Guías](guides/cover-pages.md)** - Tutoriales detallados de cada característica
- **[API Reference](api/qrydoc.md)** - Documentación técnica completa

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Abre un Pull Request

## 📄 Licencia

GPL-3.0 License - ver [LICENSE](https://github.com/danro-dev/qry-doc/blob/main/LICENSE) para más detalles.

---

<p align="center">
  Hecho con ❤️ por <a href="https://github.com/danro-dev">danro-dev</a>
</p>
