# Introducción a PostgreSQL en este proyecto

Este proyecto utiliza PostgreSQL como base de datos para almacenar la información del dataset de libros de Goodreads y poder consultarla mediante SQL.

## ¿Qué es PostgreSQL?

PostgreSQL es un sistema gestor de bases de datos relacional (RDBMS) de código abierto, robusto y muy extendido en entornos de producción.

Características relevantes para este proyecto:

- Soporta SQL estándar.
- Tiene tipos de datos avanzados.
- Es adecuado para análisis de datos y reporting.

## Cómo se ejecuta PostgreSQL aquí

No necesitas instalar PostgreSQL directamente en tu máquina. En lugar de eso, se levanta un contenedor Docker definido en `docker-compose.postgresql.yml`.

El servicio `postgres` se configura con variables de entorno leídas desde el archivo `.env` de la raíz del proyecto:

- `PROJECT_NAME`: se usa como prefijo para el nombre del contenedor.
- `POSTGRES_DB`: nombre de la base de datos por defecto.
- `POSTGRES_USER`: usuario administrador principal.
- `POSTGRES_PASSWORD`: contraseña del usuario.
- `POSTGRES_PORT`: puerto expuesto en tu máquina local.
- `POSTGRES_VERSION`: versión de la imagen oficial de PostgreSQL.

Opcionalmente, puedes definir también `POSTGRES_HOST` (por defecto `localhost`),
que será utilizado por los scripts de Python cuando construyan la URL de conexión.

## Configurar tu archivo `.env`

1. Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

En Windows PowerShell puedes usar:

```powershell
Copy-Item .env.example .env
```

2. Edita el archivo `.env` y ajusta los valores:

- Cambia `POSTGRES_PASSWORD` por una contraseña segura.
- Si el puerto `5432` ya está ocupado en tu máquina, cambia `POSTGRES_PORT` por otro (por ejemplo `5433`).

## Levantar PostgreSQL con Docker Compose

Desde la raíz del repositorio:

```bash
docker compose -f docker-compose.postgresql.yml up -d
```

Esto descargará (si es necesario) la imagen `postgres:<POSTGRES_VERSION>` y lanzará un contenedor con:

- La base de datos `POSTGRES_DB` creada automáticamente.
- El usuario `POSTGRES_USER` con la contraseña especificada.
- El puerto `POSTGRES_PORT` de tu máquina mapeado al puerto 5432 del contenedor.

Puedes comprobar que el servicio está arriba con:

```bash
docker compose -f docker-compose.postgresql.yml ps
```

## Conectarse a PostgreSQL

### Desde la línea de comandos (psql en el contenedor)

```bash
docker compose -f docker-compose.postgresql.yml exec -u postgres postgres psql -d $POSTGRES_DB
```

En PowerShell, si quieres indicar los valores explícitos:

```powershell
docker compose -f docker-compose.postgresql.yml exec -u postgres postgres psql -d goodreads
```

### Desde tu máquina (cliente SQL o librerías Python)

- **Host:** `localhost`
- **Puerto:** valor de `POSTGRES_PORT` (por defecto 5432)
- **Base de datos:** valor de `POSTGRES_DB` (por defecto `goodreads`)
- **Usuario:** valor de `POSTGRES_USER` (por defecto `goodreads_user`)
- **Contraseña:** valor de `POSTGRES_PASSWORD`

## Relación con los scripts de `src/`

Los scripts de la carpeta `src/` como `load_books_to_postgres.py` y `run_full_pipeline.py` deberán usar estos parámetros de conexión para comunicarse con el PostgreSQL en Docker.

En este repositorio esa lógica ya está centralizada en el módulo `src/db_config.py`,
que construye automáticamente una URL del tipo:

```text
postgresql+psycopg2://usuario:contraseña@host:puerto/base_de_datos
```

La prioridad es:

1. Si existe `DATABASE_URL` en el entorno, se usa tal cual.
2. Si no existe, se construye usando `POSTGRES_DB`, `POSTGRES_USER`,
   `POSTGRES_PASSWORD`, `POSTGRES_HOST` y `POSTGRES_PORT`.

## Administración básica

Algunos comandos útiles dentro de `psql`:

- Listar bases de datos: `\\l`
- Cambiar de base de datos: `\\c nombre_db`
- Listar tablas: `\\dt`
- Salir de psql: `\\q`

Para más ejemplos de SQL, revisa también `docs/sql-cheatsheet.md`.
