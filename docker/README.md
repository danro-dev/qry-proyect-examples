# Base de Datos PostgreSQL para qry-doc

Este directorio contiene la configuración de Docker para una base de datos PostgreSQL de ejemplo.

## Requisitos

- Docker y Docker Compose instalados

## Inicio Rápido

```bash
# Iniciar la base de datos
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Detener y eliminar datos
docker-compose down -v
```

## Datos de Conexión

- **Host:** localhost
- **Puerto:** 5432
- **Usuario:** qry_user
- **Contraseña:** qry_password
- **Base de datos:** qry_ventas

## Cadena de Conexión

```
postgresql://qry_user:qry_password@localhost:5432/qry_ventas
```

## Estructura de la Base de Datos

### Tablas

| Tabla | Descripción |
|-------|-------------|
| `categorias` | Categorías de productos |
| `productos` | Catálogo de productos |
| `regiones` | Regiones geográficas |
| `vendedores` | Información de vendedores |
| `clientes` | Información de clientes |
| `ventas` | Transacciones de venta |

### Vista

- `vista_ventas_detalle`: Vista pre-unida con todos los datos de ventas, ideal para análisis.

## Uso con qry-doc

```python
from qry_doc import QryDoc
from pandasai_openai import OpenAI

llm = OpenAI()
qry = QryDoc("postgresql://qry_user:qry_password@localhost:5432/qry_ventas", llm=llm)

# Hacer consultas
respuesta = qry.ask("¿Cuál es el total de ventas?")
print(respuesta)
```

## Datos de Ejemplo

La base de datos viene pre-cargada con:
- 6 categorías
- 22 productos
- 5 regiones
- 8 vendedores
- 10 clientes
- ~35 transacciones de venta (Oct 2024 - Ene 2025)
