import pandas as pd
from sqlalchemy import create_engine

# ==================== CONFIGURACIÓN DE BASE DE DATOS ====================
# Las credenciales están directamente aquí para facilitar la portabilidad
USUARIO = "postgres"
CONTRASENA = "Max22161097"
HOST = "127.0.0.1"
PUERTO = "5432"
BASE_DATOS = "bd_incidencia_sesnsp"

# ==================== FUNCIÓN PRINCIPAL ETL ====================
def cargar_sesnsp_municipal():
    # 1. Conexión a la base de datos
    URL_DB = f"postgresql://{USUARIO}:{CONTRASENA}@{HOST}:{PUERTO}/{BASE_DATOS}"
    engine = create_engine(URL_DB)
    
    # Nombre de tu archivo CSV
    ruta_csv = 'RNID-Delitos_Municipal-2026-feb2026.csv'
    
    print(f"\nIniciando lectura del archivo: {ruta_csv}")
    
    try:
        # 2. EXTRACCIÓN: Leemos con latin-1 para evitar el error "0xf1" (la 'ñ')
        df = pd.read_csv(ruta_csv, encoding='latin-1', low_memory=False)
        
        # 3. TRANSFORMACIÓN: Limpieza de columnas para PostgreSQL
        nuevas_columnas = []
        for c in df.columns:
            col_limpia = str(c).strip().lower()
            col_limpia = col_limpia.replace(' ', '_')
            col_limpia = col_limpia.replace('.', '')
            col_limpia = col_limpia.replace('ñ', 'n')  
            col_limpia = col_limpia.replace('í', 'i')  
            nuevas_columnas.append(col_limpia)
            
        df.columns = nuevas_columnas
        
        print(f"Archivo leído correctamente. Se procesarán {len(df)} registros.")
        
        # 4. CARGA: Subir a PostgreSQL
        nombre_tabla = 'fuente_sesnsp_municipal'
        print(f"Subiendo a PostgreSQL en la tabla '{nombre_tabla}'... (espera unos segundos)")
        
        # if_exists='replace' borra la tabla y la vuelve a crear si la corres dos veces
        df.to_sql(nombre_tabla, engine, if_exists='replace', index=False)
        
        print(f"¡ÉXITO! Los datos ya están en tu base de datos '{BASE_DATOS}'.")
        print(f"Ve a pgAdmin y revisa que la tabla '{nombre_tabla}' tenga los datos.")
        
    except FileNotFoundError:
        print(f"ERROR: No encuentro el archivo '{ruta_csv}'. Asegúrate de que esté en la misma carpeta que este script.")
    except Exception as e:
        print(f"ERROR INESPERADO: {e}")

# ==================== EJECUCIÓN ====================
if __name__ == "__main__":
    cargar_sesnsp_municipal()