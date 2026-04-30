import pandas as pd
from sqlalchemy import create_engine

# ==================== CONFIGURACION DE BASE DE DATOS ====================
USUARIO = USUARIO # Tu usuario
CONTRASENA = CONTRAEÑA # Tu contraseña
HOST = "127.0.0.1"
PUERTO = "5432"
BASE_DATOS = "bd_accidentes_viales"

def cargar_atus_inegi():
    # 1. Conexion a la base de datos
    URL_DB = f"postgresql://{USUARIO}:{CONTRASENA}@{HOST}:{PUERTO}/{BASE_DATOS}"
    engine = create_engine(URL_DB)
    
    # Nombre del archivo que descargaste
    ruta_csv = 'atus_anual_2024.csv'
    
    print(f"\nIniciando lectura del archivo: {ruta_csv}")
    
    try:
        # 2. EXTRACCION: Leemos con latin-1 para procesar acentos correctamente
        df = pd.read_csv(ruta_csv, encoding='latin-1', low_memory=False)
        
        # 3. TRANSFORMACION: Limpieza de nombres de columnas
        # El INEGI usa mayusculas, las pasamos a minusculas para estandarizar
        df.columns = [str(c).strip().lower().replace(' ', '_') for c in df.columns]
        
        print(f"Archivo leido correctamente. Se procesaran {len(df)} registros.")
        
        # 4. CARGA: Subir a PostgreSQL
        nombre_tabla = 'fuente_atus_inegi'
        print(f"Subiendo a PostgreSQL en la tabla '{nombre_tabla}'...")
        
        df.to_sql(nombre_tabla, engine, if_exists='replace', index=False)
        
        print(f"EXITO! Los datos ya estan en tu base de datos '{BASE_DATOS}'.")
        print(f"Ve a pgAdmin y revisa la tabla '{nombre_tabla}'.")
        
    except FileNotFoundError:
        print(f"ERROR: No encuentro el archivo '{ruta_csv}'.")
    except Exception as e:
        print(f"ERROR INESPERADO: {e}")

if __name__ == "__main__":
    cargar_atus_inegi()
