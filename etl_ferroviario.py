import pandas as pd
from sqlalchemy import create_engine

# ==================== CONFIGURACION DE BASE DE DATOS ====================
USUARIO = USUARIO # Tu usuario
CONTRASENA = CONTRASEÑA # Tu contraseña
HOST = "127.0.0.1"
PUERTO = "5432"
BASE_DATOS = "bd_seguridad_transporte"

def cargar_seguridad_ferroviaria():
    # 1. Conexion a la base de datos
    URL_DB = f"postgresql://{USUARIO}:{CONTRASENA}@{HOST}:{PUERTO}/{BASE_DATOS}"
    engine = create_engine(URL_DB)
    
    # Nombre del archivo que subiste
    ruta_csv = 'robo_vandalismo_SFM_2510.csv'
    
    print(f"\nIniciando lectura del archivo: {ruta_csv}")
    
    try:
        # 2. EXTRACCION: Usamos latin-1 por los acentos en estados y localidades
        df = pd.read_csv(ruta_csv, encoding='latin-1')
        
        # 3. TRANSFORMACION
        # Normalizamos nombres de columnas a minusculas
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # Convertimos la fecha a formato datetime
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        
        print(f"Archivo leido correctamente. Se procesaran {len(df)} registros.")
        
        # 4. CARGA: Subir a PostgreSQL
        nombre_tabla = 'fuente_robo_vandalismo_trenes'
        print(f"Subiendo a PostgreSQL en la tabla '{nombre_tabla}'...")
        
        df.to_sql(nombre_tabla, engine, if_exists='replace', index=False)
        
        print(f"EXITO! Los datos ya estan en tu base de datos '{BASE_DATOS}'.")
        print(f"Ve a pgAdmin y revisa la tabla '{nombre_tabla}'.")
        
    except FileNotFoundError:
        print(f"ERROR: No encuentro el archivo '{ruta_csv}'.")
    except Exception as e:
        print(f"ERROR INESPERADO: {e}")

if __name__ == "__main__":
    cargar_seguridad_ferroviaria()
