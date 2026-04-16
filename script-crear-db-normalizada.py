import psycopg2
import csv

# ==================== CONEXIÓN A POSTGRESQL ====================
conn = psycopg2.connect(
    host="127.0.0.1",
    database="seguridad_delictiva",
    user="postgres",
    password="Max22161097"          
)
cur = conn.cursor()

print("Conectado a PostgreSQL...")

# ==================== CREAR TABLAS (3NF) ====================
cur.execute("""
    DROP TABLE IF EXISTS registro, colonia, ciudad, estado, estatus, 
                       delito, tipo_delito, gravedad, persona CASCADE;

    CREATE TABLE gravedad (
        id_gravedad SERIAL PRIMARY KEY,
        nivel VARCHAR(30) UNIQUE NOT NULL
    );

    CREATE TABLE tipo_delito (
        id_tipo_delito SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        id_gravedad INTEGER REFERENCES gravedad(id_gravedad)
    );

    CREATE TABLE delito (
        id_delito SERIAL PRIMARY KEY,
        nombre VARCHAR(150) NOT NULL,
        id_tipo_delito INTEGER REFERENCES tipo_delito(id_tipo_delito)
    );

    CREATE TABLE estado (
        id_estado SERIAL PRIMARY KEY,
        nombre VARCHAR(80) UNIQUE NOT NULL
    );

    CREATE TABLE ciudad (
        id_ciudad SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        id_estado INTEGER REFERENCES estado(id_estado)
    );

    CREATE TABLE colonia (
        id_colonia SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        id_ciudad INTEGER REFERENCES ciudad(id_ciudad)
    );

    CREATE TABLE estatus (
        id_estatus SERIAL PRIMARY KEY,
        nombre VARCHAR(30) UNIQUE NOT NULL
    );

    CREATE TABLE persona (
        id_persona SERIAL PRIMARY KEY,
        curp VARCHAR(18) UNIQUE NOT NULL,
        nombre VARCHAR(100),
        apellido VARCHAR(100),
        edad INTEGER,
        genero CHAR(1),
        domicilio TEXT
    );

    CREATE TABLE registro (
        id_registro SERIAL PRIMARY KEY,
        id_persona INTEGER REFERENCES persona(id_persona),
        id_delito INTEGER REFERENCES delito(id_delito),
        id_colonia INTEGER REFERENCES colonia(id_colonia),
        id_estatus INTEGER REFERENCES estatus(id_estatus),
        fecha DATE,
        hora TIME,
        reincidente BOOLEAN,
        numero_delitos INTEGER,
        peso_delito NUMERIC(5,2),
        indice_delictivo NUMERIC(8,2),
        zona_postal VARCHAR(10),
        fuero VARCHAR(20),
        arma_fuego BOOLEAN,
        recuperado BOOLEAN,
        tiempo_respuesta_minutos INTEGER
    );
""")

print("Tablas creadas correctamente")

# ==================== INSERTAR DATOS DESDE CSV ====================
with open('datos_delictivos_no_normalizados.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # Diccionarios para evitar duplicados
    gravedades = {}
    tipos = {}
    delitos_dict = {}
    estados = {}
    ciudades = {}
    colonias = {}
    estatuses = {}

    for row in reader:
        # Gravedad
        if row['gravedad'] not in gravedades:
            cur.execute("INSERT INTO gravedad (nivel) VALUES (%s) RETURNING id_gravedad", (row['gravedad'],))
            gravedades[row['gravedad']] = cur.fetchone()[0]

        # Tipo de delito
        clave_tipo = (row['tipo_delito'], row['gravedad'])
        if clave_tipo not in tipos:
            cur.execute("""
                INSERT INTO tipo_delito (nombre, id_gravedad) 
                VALUES (%s, %s) RETURNING id_tipo_delito
            """, (row['tipo_delito'], gravedades[row['gravedad']]))
            tipos[clave_tipo] = cur.fetchone()[0]

        # Delito
        if row['delito'] not in delitos_dict:
            cur.execute("""
                INSERT INTO delito (nombre, id_tipo_delito) 
                VALUES (%s, %s) RETURNING id_delito
            """, (row['delito'], tipos[clave_tipo]))
            delitos_dict[row['delito']] = cur.fetchone()[0]

        # Estado
        if row['estado'] not in estados:
            cur.execute("INSERT INTO estado (nombre) VALUES (%s) RETURNING id_estado", (row['estado'],))
            estados[row['estado']] = cur.fetchone()[0]

        # Ciudad
        clave_ciudad = (row['ciudad'], row['estado'])
        if clave_ciudad not in ciudades:
            cur.execute("""
                INSERT INTO ciudad (nombre, id_estado) 
                VALUES (%s, %s) RETURNING id_ciudad
            """, (row['ciudad'], estados[row['estado']]))
            ciudades[clave_ciudad] = cur.fetchone()[0]

        # Colonia
        clave_colonia = (row['colonia'], row['ciudad'])
        if clave_colonia not in colonias:
            cur.execute("""
                INSERT INTO colonia (nombre, id_ciudad) 
                VALUES (%s, %s) RETURNING id_colonia
            """, (row['colonia'], ciudades[clave_ciudad]))
            colonias[clave_colonia] = cur.fetchone()[0]

        # Estatus
        if row['estatus'] not in estatuses:
            cur.execute("INSERT INTO estatus (nombre) VALUES (%s) RETURNING id_estatus", (row['estatus'],))
            estatuses[row['estatus']] = cur.fetchone()[0]

        # Persona
        cur.execute("""
            INSERT INTO persona (curp, nombre, apellido, edad, genero, domicilio)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (curp) DO NOTHING
            RETURNING id_persona
        """, (row['curp'], row['nombre'], row['apellido'], int(row['edad']), row['genero'], row['domicilio']))

        if cur.rowcount == 0:   # Ya existía
            cur.execute("SELECT id_persona FROM persona WHERE curp = %s", (row['curp'],))
        persona_id = cur.fetchone()[0]

        # Registro
        cur.execute("""
            INSERT INTO registro 
            (id_persona, id_delito, id_colonia, id_estatus, fecha, hora, reincidente, 
             numero_delitos, peso_delito, indice_delictivo, zona_postal, fuero, 
             arma_fuego, recuperado, tiempo_respuesta_minutos)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            persona_id,
            delitos_dict[row['delito']],
            colonias[clave_colonia],
            estatuses[row['estatus']],
            row['fecha'],
            row['hora'],
            bool(int(row['reincidente'])),
            int(row['numero_delitos']),
            float(row['peso_delito']),
            float(row['indice_delictivo']),
            row['zona_postal'],
            row['fuero'],
            row['arma_fuego'].lower() == 'true',
            row['recuperado'].lower() == 'true',
            int(row['tiempo_respuesta_minutos'])
        ))

conn.commit()
cur.close()
conn.close()
print("¡Base de datos creada e insertados todos los registros correctamente!")