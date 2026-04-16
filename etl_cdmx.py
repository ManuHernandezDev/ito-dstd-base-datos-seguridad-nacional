import pandas as pd
from sqlalchemy import create_engine

# ==================== CONFIGURACIÓN DE BASE DE DATOS ====================
USUARIO = "postgres"
CONTRASENA = "Max22161097"
HOST = "127.0.0.1"
PUERTO = "5432"
BASE_DATOS = "bd_carpetas_cdmx"

# ==================== FUNCIÓN PRINCIPAL ETL ====================
def cargar_carpetas_cdmx():
    # 1. Conexión a la base de datos
    URL_DB = f"postgresql://{USUARIO}:{CONTRASENA}@{HOST}:{PUERTO}/{BASE_DATOS}"
    engine = create_engine(URL_DB)
    
    # Nombre del archivo que subiste
    ruta_csv = 'carpetasFGJ_2024.csv'
    
    print(f"\nIniciando lectura del archivo: {ruta_csv}")
    
    try:
        # 2. EXTRACCIÓN: Leemos con utf-8 (confirmado que viene en este formato)
        df = pd.read_csv(ruta_csv, encoding='utf-8', low_memory=False)
        
        # 3. TRANSFORMACIÓN: Limpieza de seguridad
        # Aunque ya vienen bien, aplicamos Clean Code por si hay espacios ocultos
        df.columns = [str(c).strip().lower().replace(' ', '_').replace('.', '') for c in df.columns]
        
        print(f"Archivo leído correctamente. Se procesarán {len(df)} registros.")
        
        # 4. CARGA: Subir a PostgreSQL
        nombre_tabla = 'fuente_fgj_cdmx'
        print(f"Subiendo a PostgreSQL en la tabla '{nombre_tabla}'... (esto puede tardar un poco por la cantidad de datos)")
        
        df.to_sql(nombre_tabla, engine, if_exists='replace', index=False)
        
        print(f"¡ÉXITO! Los datos ya están en tu base de datos '{BASE_DATOS}'.")
        print(f"Ve a pgAdmin y revisa que la tabla '{nombre_tabla}' tenga los datos.")
        
    except FileNotFoundError:
        print(f"ERROR: No encuentro el archivo '{ruta_csv}'. Asegúrate de que esté en la misma carpeta que este script.")
    except Exception as e:
        print(f"ERROR INESPERADO: {e}")

# ==================== EJECUCIÓN ====================
if __name__ == "__main__":
    cargar_carpetas_cdmx()