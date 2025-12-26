"""
09 - Explorar Base de Datos
===========================

Este ejemplo se conecta a una base de datos PostgreSQL
y muestra toda su estructura: tablas, columnas y datos.
"""

from qry_doc.data_source import DataSourceLoader
import os

# URL de conexión
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:danro@127.0.0.1:5432/ap"
)

print("=" * 70)
print("🔍 EXPLORADOR DE BASE DE DATOS")
print("=" * 70)
print(f"\n📡 Conectando a: {DATABASE_URL.split('@')[1]}")  # Ocultar credenciales

try:
    # Explorar la base de datos
    db_info = DataSourceLoader.explore_database(DATABASE_URL)
    
    # Mostrar tablas
    print(f"\n📋 TABLAS ENCONTRADAS: {len(db_info['tables'])}")
    print("-" * 70)
    
    for table_name, info in db_info['tables'].items():
        print(f"\n🗂️  {table_name.upper()}")
        print(f"    Filas: {info['row_count']}")
        print(f"    Columnas ({len(info['columns'])}):")
        
        for col in info['columns']:
            print(f"      • {col['name']:20} → {col['type']}")
        
        # Mostrar muestra de datos
        print(f"\n    📊 Muestra de datos:")
        df = DataSourceLoader.load_sql_query(
            DATABASE_URL,
            f'SELECT * FROM "{table_name}" LIMIT 5'
        )
        print(df.to_string(index=False).replace('\n', '\n    '))
    
    # Mostrar vistas si hay
    if db_info['views']:
        print(f"\n👁️  VISTAS ENCONTRADAS: {len(db_info['views'])}")
        print("-" * 70)
        for view_name, info in db_info['views'].items():
            print(f"\n    {view_name}: {info['row_count']} filas")
    
    print("\n" + "=" * 70)
    print("✅ Exploración completada")
    print("=" * 70)

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Verifica que PostgreSQL esté corriendo y la URL sea correcta")
