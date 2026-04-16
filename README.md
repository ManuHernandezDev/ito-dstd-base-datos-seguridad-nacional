# Sistema de Integración de Datos de Seguridad (ETL)

## Equipo 4: Seguridad de Datos - Plataforma México (Índices Delictivos)

Este repositorio contiene los scripts automatizados para extraer, transformar y cargar (ETL) bases de datos públicas masivas sobre seguridad y justicia hacia un gestor PostgreSQL.

## Configuración e Instalación

1. Tener instalado PostgreSQL.
2. Crear la base de datos ejecutando en pgAdmin: `CREATE DATABASE seguridad_delictiva;`
3. Configurar tus credenciales en el archivo `config.py`.
4. Instalar las librerías necesarias: `pip install pandas sqlalchemy psycopg2-binary`

---

## Fuentes de Datos Integradas y Diccionarios

### 1. Incidencia Delictiva del Fuero Común (Nivel Municipal)

- **Organización:** Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública (SESNSP - México).
- **Enlace:** [Datos Abiertos SESNSP](https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva)
- **Clasificación:** **1ª Mano** (Datos recolectados y publicados directamente por el gobierno federal a través de las fiscalías estatales).
- **Diccionario de Datos (Principales):**
  - `cve._ent` (Cualitativa | `INTEGER`): Clave de identificación del estado.
  - `entidad` (Cualitativa | `VARCHAR`): Nombre del estado.
  - `cve._municipio` (Cualitativa | `INTEGER`): Clave de identificación del municipio.
  - `municipio` (Cualitativa | `VARCHAR`): Nombre del municipio.
  - `bien_juridico_afectado` (Cualitativa | `VARCHAR`): Categoría legal afectada (ej. El patrimonio).
  - `tipo_de_delito` (Cualitativa | `VARCHAR`): Nombre específico del delito.
  - `enero` / `febrero` (Cuantitativa | `INTEGER`): Conteo mensual de incidentes registrados en ese municipio.
