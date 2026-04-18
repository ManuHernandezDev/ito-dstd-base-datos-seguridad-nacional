# Sistema de Integracion de Datos de Seguridad - Plataforma Mexico

## Equipo 4: Seguridad de Datos - Plataforma México (Índices Delictivos)

#### Integrantes
- CANDELARIA VELAZQUEZ RODRIGO
- DIEGO GARCIA JENNIFER
- ELORZA PÉREZ JOAQUÍN BARUC
- GARCÍA GALLEGOS ERIC      
- HERNANDEZ SORIANO MANUEL  
- MARTÍNEZ MENDOZA JESÚS ÁNGEL


Este proyecto automatiza la extraccion, transformacion y carga (ETL) de bases de datos publicas masivas sobre seguridad y justicia hacia un gestor PostgreSQL.

La finalidad es proveer una base estructurada para el analisis y la toma de decisiones, simulando el funcionamiento de una plataforma nacional de seguridad aplicando principios de Clean Code.

## Configuracion e Instalacion

Para ejecutar este proyecto de forma local, sigue estos pasos:

1. Requisitos previos: Tener instalado Python 3 y PostgreSQL (pgAdmin).
2. Crear las Bases de Datos: En pgAdmin, deberas crear una base de datos distinta para cada fuente de informacion (los nombres exactos vienen en la descripcion de cada fuente mas abajo).
3. Instalar Dependencias: En la terminal de tu editor, activa tu entorno virtual y ejecuta:
   `pip install pandas sqlalchemy psycopg2-binary`
4. Ejecucion: Asegurate de tener los archivos CSV en la misma carpeta que los scripts correspondientes y ejecuta cada uno (ej. `python etl_sesnsp.py`).

Nota: Las credenciales de conexion a la base de datos (incluyendo el nombre especifico de la base de datos a la que apunta) estan configuradas directamente dentro de cada script de carga para facilitar su ejecucion individual.

---

## Fuentes de Datos Integradas y Diccionarios

### 1. Registro Nacional de Incidencia Delictiva (Nivel Municipal)

- Nombre de la base de datos en pgAdmin: bd_incidencia_sesnsp
- Archivo a ocupar: RNID-Delitos_Municipal-2026-feb2026.csv
- Organizacion: Secretariado Ejecutivo del Sistema Nacional de Seguridad Publica (SESNSP).
- Enlace Oficial: https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva
- Clasificacion de la fuente: 1a Mano (Datos oficiales publicados directamente por el gobierno federal).

#### Diccionario de Datos (Columnas Normalizadas):

- año (Cuantitativa | INTEGER): Año en el que se registro la incidencia.
- clave_ent (Cualitativa | INTEGER): Clave numerica identificadora del Estado.
- entidad (Cualitativa | VARCHAR): Nombre del Estado de la Republica.
- cve_municipio (Cualitativa | INTEGER): Clave numerica identificadora del Municipio.
- municipio (Cualitativa | VARCHAR): Nombre del Municipio.
- bien_juridico_afectado (Cualitativa | VARCHAR): Categoria legal afectada.
- tipo_de_delito (Cualitativa | VARCHAR): Nombre principal del delito.
- subtipo_de_delito (Cualitativa | VARCHAR): Clasificacion secundaria del delito.
- modalidad (Cualitativa | VARCHAR): Especificacion del delito (ej. Con violencia).
- enero a diciembre (Cuantitativa | INTEGER): Numero de incidentes en ese mes.

### 2. Carpetas de Investigacion FGJ de la Ciudad de Mexico (2024)

- Nombre de la base de datos en pgAdmin: bd_carpetas_cdmx
- Archivo a ocupar: carpetasFGJ_2024.csv
- Organizacion: Fiscalia General de Justicia de la Ciudad de Mexico (Datos Abiertos CDMX).
- Enlace Oficial: https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico
- Clasificacion de la fuente: 1a Mano (Extraido directamente del Sistema de Averiguaciones Previas de la Fiscalia).

#### Diccionario de Datos (Columnas Normalizadas):

- fecha_hecho (Cuantitativa/Temporal | DATE): Fecha exacta en la que presuntamente ocurrio el incidente.
- delito (Cualitativa | VARCHAR): Descripcion tipificada del crimen cometido.
- categoria_delito (Cualitativa | VARCHAR): Agrupacion general para fines estadisticos.
- alcaldia_hecho (Cualitativa | VARCHAR): Demarcacion territorial (Alcaldia) donde ocurrio el incidente.
- colonia_hecho (Cualitativa | VARCHAR): Nombre de la colonia donde se reporto el suceso.
- latitud (Cuantitativa | DECIMAL): Coordenada geografica (Eje Y) para mapeo espacial.
- longitud (Cuantitativa | DECIMAL): Coordenada geografica (Eje X) para mapeo espacial.

### 3. Accidentes de Transito Terrestre en Zonas Urbanas y Suburbanas (2024)

- Nombre de la base de datos en pgAdmin: bd_accidentes_viales
- Archivo a ocupar: atus_anual_2024.csv
- Organizacion: Instituto Nacional de Estadistica y Geografia (INEGI).
- Enlace Oficial: https://www.inegi.org.mx/programas/accidentes/
- Clasificacion de la fuente: 1a Mano (Datos generados a partir de los registros administrativos de las direcciones de seguridad publica y vialidad).

#### Diccionario de Datos (Columnas Normalizadas):

- anio (Cuantitativa | INTEGER): Ano en que ocurrio el accidente.
- mes (Cuantitativa | INTEGER): Mes del siniestro.
- id_dia (Cuantitativa | INTEGER): Numero de dia del mes.
- diasemana (Cualitativa | VARCHAR): Nombre del dia de la semana.
- tipaccid (Cualitativa | VARCHAR): Tipo de accidente (ej. Colision con vehiculo, Volcadura, Caida de pasajero).
- causaacci (Cualitativa | VARCHAR): Causa presunta del accidente (ej. Conductor, Mala condicion del camino, Falla mecanica).
- sexo (Cualitativa | VARCHAR): Genero del conductor involucrado.
- condmuerto (Cuantitativa | INTEGER): Numero de conductores que perdieron la vida en el sitio.
- condherido (Cuantitativa | INTEGER): Numero de conductores lesionados.
- clasacc (Cualitativa | VARCHAR): Clasificacion final del evento (ej. Solo danos, No fatal, Fatal).

### 4. Inscripcion al Registro Nacional de Victimas (RENAVI)

- Nombre de la base de datos en pgAdmin: bd_registro_victimas
- Archivo a ocupar: inscripciones_renavi_2025.csv
- Organizacion: Comision Ejecutiva de Atencion a Victimas (CEAV).
- Enlace Oficial: https://www.datos.gob.mx/dataset/inscripcion_registro_nacional_victimas_renavi
- Clasificacion de la fuente: 1a Mano (Registros oficiales de personas inscritas en el padron nacional de victimas por delitos o violaciones a derechos humanos).

#### Diccionario de Datos (Columnas Normalizadas):

- id (Cuantitativa | INTEGER): Identificador unico consecutivo del registro.
- competencia (Cualitativa | VARCHAR): Ambito jurisdiccional del hecho (Federal o Estatal).
- fecha (Temporal | DATE): Fecha oficial de inscripcion en el registro.
- tipo_registro (Cualitativa | VARCHAR): Modalidad de formato de registro (ej. Fud).
- estatus (Cualitativa | VARCHAR): Situacion actual del registro (ej. Folio Asignado).
- tipo_victima (Cualitativa | VARCHAR): Clasificacion de la victima (Directa, Indirecta o Potencial).
- sexo (Cualitativa | VARCHAR): Genero de la victima registrada.
- materia (Cualitativa | VARCHAR): Naturaleza del suceso (Delito o Violacion a Derechos Humanos).

### 5. Reportes de Seguridad en el Sistema Ferroviario Mexicano (Robo y Vandalismo)

- Nombre de la base de datos en pgAdmin: bd_seguridad_transporte
- Archivo a ocupar: robo_vandalismo_SFM_2510.csv
- Organizacion: Agencia Reguladora del Transporte Ferroviario (ARTF).
- Enlace Oficial: https://www.datos.gob.mx/dataset/reportes_seguridad_sistema_ferroviario
- Clasificacion de la fuente: 1a Mano (Registros detallados de incidentes de seguridad que afectan la infraestructura y operacion ferroviaria nacional).

#### Diccionario de Datos (Columnas Normalizadas):

- num (Cuantitativa | INTEGER): Numero consecutivo de registro.
- fecha (Temporal | DATE): Fecha en la que se reporto el incidente.
- entidad_federativa (Cualitativa | VARCHAR): Estado donde ocurrio el evento.
- localidad (Cualitativa | VARCHAR): Municipio o poblacion especifica del suceso.
- categoria (Cualitativa | VARCHAR): Clasificacion general del evento (ej. Vandalismo al tren, Robo a via).
- tipo (Cualitativa | VARCHAR): Detalle especifico del incidente (ej. Cierre de angulares, Manipulacion de señales, Robo de componentes).
