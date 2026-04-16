import pandas as pd
from sqlalchemy import create_engine

# ==================== CONFIGURACION DE BASE DE DATOS ====================
USUARIO = "postgres"
CONTRASENA = "Max22161097"
HOST = "127.0.0.1"
PUERTO = "5432"
BASE_DATOS = "bd_registro_victimas"

def cargar_renavi_victimas():
    # 1. Conexion a la base de datos
    URL_DB = f"postgresql://{USUARIO}:{CONTRASENA}@{HOST}:{PUERTO}/{BASE_DATOS}"
    engine = create_engine(URL_DB)
    
    # Nombre del archivo que descargaste
    ruta_csv = 'inscripciones_renavi_2025.csv'
    
    print(f"\nIniciando lectura del archivo: {ruta_csv}")
    
    try:
        # 2. EXTRACCION
        df = pd.read_csv(ruta_csv, encoding='utf-8')
        
        # 3. TRANSFORMACION
        # Normalizamos nombres de columnas (quitar espacios, pasar a minusculas)
        df.columns = [str(c).strip().lower().replace(' ', '_') for c in df.columns]
        
        # Convertimos la columna fecha a formato datetime para que Postgres la reconozca
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        
        print(f"Archivo leido correctamente. Se procesaran {len(df)} registros.")
        
        # 4. CARGA: Subir a PostgreSQL
        nombre_tabla = 'fuente_renavi_victimas'
        print(f"Subiendo a PostgreSQL en la tabla '{nombre_tabla}'...")
        
        df.to_sql(nombre_tabla, engine, if_exists='replace', index=False)
        
        print(f"EXITO! Los datos ya estan en tu base de datos '{BASE_DATOS}'.")
        print(f"Ve a pgAdmin y revisa la tabla '{nombre_tabla}'.")
        
    except FileNotFoundError:
        print(f"ERROR: No encuentro el archivo '{ruta_csv}'.")
    except Exception as e:
        print(f"ERROR INESPERADO: {e}")

if __name__ == "__main__":
    cargar_renavi_victimas()