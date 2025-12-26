# Conexiones a Bases de Datos

<span class="version-badge">v0.1.0+</span>

qry-doc soporta conexiones a múltiples bases de datos SQL usando SQLAlchemy como backend.

## Bases de datos soportadas

| Base de datos | Prefijo | Driver requerido |
|---------------|---------|------------------|
| PostgreSQL | `postgresql://` | `psycopg2-binary` |
| MySQL | `mysql://` | `pymysql` |
| SQLite | `sqlite:///` | (incluido en Python) |
| SQL Server | `mssql://` | `pyodbc` |
| Oracle | `oracle://` | `cx_oracle` |

## Instalación de drivers

```bash
# PostgreSQL
pip install psycopg2-binary

# MySQL
pip install pymysql

# SQL Server
pip install pyodbc

# Oracle
pip install cx_oracle

# O instalar qry-doc con soporte para PostgreSQL
pip install qry-doc[postgres]

# O con soporte para MySQL
pip install qry-doc[mysql]
```

## Formato de conexión

El formato general de una cadena de conexión es:

```
driver://usuario:contraseña@host:puerto/base_de_datos
```

## PostgreSQL

### Conexión básica

```python
from qry_doc import QryDoc

# Conexión directa
qry = QryDoc("postgresql://usuario:contraseña@localhost:5432/mi_base")

# Consultar datos
resultado = qry.ask("¿Cuántos registros hay?")
print(resultado)
```

### Con variables de entorno (recomendado)

```python
import os
from qry_doc import QryDoc

# Usar variable de entorno para seguridad
DATABASE_URL = os.environ.get("DATABASE_URL")
qry = QryDoc(DATABASE_URL)
```

### Explorar estructura de la base de datos

```python
from qry_doc.data_source import DataSourceLoader

# Ver todas las tablas y vistas
db_info = DataSourceLoader.explore_database(
    "postgresql://usuario:contraseña@localhost:5432/mi_base"
)

print("Tablas encontradas:")
for tabla, info in db_info['tables'].items():
    print(f"  - {tabla}: {info['row_count']} filas")
    for col in info['columns']:
        print(f"      {col['name']} ({col['type']})")
```

### Cargar tabla específica

```python
from qry_doc.data_source import DataSourceLoader

# Cargar una tabla específica
df = DataSourceLoader.load_sql_table(
    "postgresql://usuario:contraseña@localhost:5432/mi_base",
    "ventas"
)

print(df.head())
```

### Ejecutar query personalizado

```python
from qry_doc.data_source import DataSourceLoader

# Ejecutar SQL personalizado
df = DataSourceLoader.load_sql_query(
    "postgresql://usuario:contraseña@localhost:5432/mi_base",
    """
    SELECT producto, SUM(cantidad) as total
    FROM ventas
    WHERE fecha >= '2024-01-01'
    GROUP BY producto
    ORDER BY total DESC
    """
)

print(df)
```

## MySQL

### Conexión básica

```python
from qry_doc import QryDoc

qry = QryDoc("mysql://usuario:contraseña@localhost:3306/mi_base")

# Generar reporte
qry.generate_report(
    "Analiza las ventas del último mes",
    "output/reporte_mysql.pdf",
    title="Análisis de Ventas"
)
```

### Con charset específico

```python
# MySQL con charset UTF-8
qry = QryDoc("mysql://usuario:contraseña@localhost:3306/mi_base?charset=utf8mb4")
```

## SQLite

### Conexión a archivo local

```python
from qry_doc import QryDoc

# Nota: SQLite usa 3 barras para rutas absolutas
qry = QryDoc("sqlite:///ruta/a/mi_base.db")

# O ruta relativa
qry = QryDoc("sqlite:///./datos/local.db")
```

### Base de datos en memoria

```python
# SQLite en memoria (útil para pruebas)
qry = QryDoc("sqlite:///:memory:")
```

## Ejemplo completo: PostgreSQL

```python
"""
Ejemplo completo de conexión a PostgreSQL con qry-doc
"""
import os
from pathlib import Path
from qry_doc import QryDoc, ReportTemplate
from qry_doc.data_source import DataSourceLoader

# Configuración
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/ventas_db"
)
OUTPUT_DIR = Path("output/postgres")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Explorar la base de datos
print("📊 Explorando base de datos...")
try:
    db_info = DataSourceLoader.explore_database(DATABASE_URL)
    
    print(f"\nTablas ({len(db_info['tables'])}):")
    for tabla, info in db_info['tables'].items():
        print(f"  📋 {tabla}: {info['row_count']} filas")
        
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# 2. Conectar con selección automática de tabla
print("\n🔗 Conectando...")
qry = QryDoc(DATABASE_URL)
print(f"✅ Conectado - {qry.shape[0]} filas, {qry.shape[1]} columnas")
print(f"   Columnas: {qry.columns}")

# 3. Hacer consultas con lenguaje natural
print("\n💬 Consultas:")
respuesta = qry.ask("¿Cuál es el total de ventas?")
print(f"   Total ventas: {respuesta}")

respuesta = qry.ask("¿Cuáles son los 5 productos más vendidos?")
print(f"   Top 5 productos: {respuesta}")

# 4. Exportar datos filtrados
print("\n📁 Exportando datos...")
qry.export_dataframe(OUTPUT_DIR / "todos_los_datos.csv")

# 5. Generar reporte PDF
print("\n📄 Generando reporte...")
template = ReportTemplate(
    primary_color="#2c3e50",
    footer_logo_enabled=True
)

qry.generate_report(
    "Genera un análisis ejecutivo de las ventas",
    OUTPUT_DIR / "reporte_ventas.pdf",
    title="Análisis de Ventas",
    template=template,
    include_chart=True,
    chart_type='bar'
)

print(f"\n✅ Completado! Archivos en: {OUTPUT_DIR}")
```

## Ejemplo completo: MySQL

```python
"""
Ejemplo de conexión a MySQL
"""
import os
from qry_doc import QryDoc
from qry_doc.data_source import DataSourceLoader

MYSQL_URL = "mysql://root:password@localhost:3306/tienda"

# Explorar
db_info = DataSourceLoader.explore_database(MYSQL_URL)
print(f"Tablas: {list(db_info['tables'].keys())}")

# Conectar y consultar
qry = QryDoc(MYSQL_URL)
print(qry.ask("¿Cuántos clientes hay registrados?"))

# Cargar tabla específica
clientes = DataSourceLoader.load_sql_table(MYSQL_URL, "clientes")
print(f"Clientes: {len(clientes)}")
```

## Ejemplo completo: SQLite

```python
"""
Ejemplo de conexión a SQLite
"""
from qry_doc import QryDoc
from qry_doc.data_source import DataSourceLoader

SQLITE_URL = "sqlite:///./datos/inventario.db"

# Conectar
qry = QryDoc(SQLITE_URL)

# Consultar
print(qry.ask("¿Cuántos productos hay en stock?"))
print(qry.ask("¿Cuáles productos tienen stock bajo?"))

# Exportar
qry.export_dataframe("output/inventario_completo.csv")
```

## Manejo de errores

```python
from qry_doc import QryDoc
from qry_doc.exceptions import DataSourceError

try:
    qry = QryDoc("postgresql://usuario:contraseña@localhost:5432/mi_base")
except DataSourceError as e:
    print(f"Error de conexión: {e}")
    # Posibles causas:
    # - Servidor no disponible
    # - Credenciales incorrectas
    # - Base de datos no existe
    # - Driver no instalado
```

## Buenas prácticas

### 1. Usar variables de entorno

```python
import os

# Nunca hardcodear credenciales
DATABASE_URL = os.environ["DATABASE_URL"]
qry = QryDoc(DATABASE_URL)
```

### 2. Usar archivos .env

```bash
# .env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/mi_base
```

```python
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]
```

### 3. Cerrar conexiones

```python
# Usar context manager
with QryDoc(DATABASE_URL) as qry:
    resultado = qry.ask("¿Cuántos registros hay?")
    print(resultado)
# Conexión cerrada automáticamente
```

## Solución de problemas

### Error: "No module named 'psycopg2'"

```bash
pip install psycopg2-binary
```

### Error: "Connection refused"

- Verificar que el servidor de base de datos esté corriendo
- Verificar host y puerto
- Verificar firewall

### Error: "Authentication failed"

- Verificar usuario y contraseña
- Verificar permisos del usuario en la base de datos

### Error: "Database does not exist"

- Verificar nombre de la base de datos
- Crear la base de datos si no existe

## Ver también

- [Inicio rápido](../getting-started/quickstart.md)
- [API QryDoc](../api/qrydoc.md)
- [Exportación CSV](../getting-started/quickstart.md#exportar-a-csv)
