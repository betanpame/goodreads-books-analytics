# goodreads-books-analytics

Proyecto de análisis del dataset de libros de Goodreads con Python, PostgreSQL y Docker.

Este repositorio incluye:

- Scripts de limpieza y carga de datos en `src/`.
- Tests básicos en `tests/`.
- Documentación de apoyo en `docs/` (pandas, SQL, Docker, PostgreSQL).
- Un entorno de base de datos basado en Docker Compose para PostgreSQL.

---

## Requisitos previos

- Python 3.10+ (se recomienda usar un entorno virtual).
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS) o Docker Engine (Linux).

---

## Configurar el entorno `.env`

En la raíz del proyecto hay un archivo de ejemplo de variables de entorno:

```bash
.env.example
```

En Windows PowerShell, crea tu archivo `.env` copiando el ejemplo:

```powershell
Copy-Item .env.example .env
```

Luego edita `.env` y revisa especialmente:

- `PROJECT_NAME`: prefijo para el nombre del contenedor.
- `POSTGRES_VERSION`: versión de la imagen de PostgreSQL (por ejemplo `17`).
- `POSTGRES_DB`: nombre de la base de datos.
- `POSTGRES_USER`: usuario.
- `POSTGRES_PASSWORD`: contraseña (cámbiala por algo seguro).
- `POSTGRES_PORT`: puerto en tu máquina (por defecto `5432`).
- `POSTGRES_HOST`: host que usarán los scripts de Python para conectarse (normalmente `localhost`).

Opcionalmente, puedes definir también `DATABASE_URL`. Si existe, tendrá prioridad sobre las demás variables de conexión.

---

## Levantar PostgreSQL con Docker Compose

El servicio de base de datos se define en `docker-compose.postgresql.yml`.

Desde la raíz del proyecto:

```powershell
docker compose -f docker-compose.postgresql.yml up -d
```

Comandos útiles:

```powershell
# Ver estado de los servicios
docker compose -f docker-compose.postgresql.yml ps

# Ver logs de PostgreSQL
docker compose -f docker-compose.postgresql.yml logs -f postgres

# Detener servicios (manteniendo datos)
docker compose -f docker-compose.postgresql.yml down

# Detener servicios y borrar volúmenes (borra datos)
docker compose -f docker-compose.postgresql.yml down -v
```

Más detalles en:

- `docs/docker/intro-docker-y-docker-compose.md`
- `docs/docker/uso-entorno-postgresql-con-docker.md`
- `docs/postgresql/intro-postgresql.md`

---

## Ejecutar el pipeline de datos

Se asume que ya tienes el entorno virtual configurado en `.venv` y las dependencias instaladas.

### 1. Cargar `books.csv` directamente en PostgreSQL

```powershell
C:/Users/Pamela/Documents/GitHub/goodreads-books-analytics/.venv/Scripts/python.exe -m src.load_books_to_postgres --table books
```

El script leerá la conexión desde `DATABASE_URL` o, si no existe, desde las variables `POSTGRES_*` definidas en `.env`.

### 2. Ejecutar el pipeline completo y (opcionalmente) cargar en PostgreSQL

```powershell
# Solo limpiar y guardar CSV limpio
C:/Users/Pamela/Documents/GitHub/goodreads-books-analytics/.venv/Scripts/python.exe -m src.run_full_pipeline

# Limpiar, guardar CSV limpio y cargarlo a PostgreSQL
C:/Users/Pamela/Documents/GitHub/goodreads-books-analytics/.venv/Scripts/python.exe -m src.run_full_pipeline --load-to-postgres
```

---

## Documentación adicional

- `docs/dataset-notes.md`: notas sobre el dataset de Goodreads.
- `docs/pandas-cheatsheet.md`: recordatorio rápido de pandas.
- `docs/sql-cheatsheet.md`: recordatorio rápido de SQL.
- `docs/repo-notes.md`: notas generales sobre el repositorio y el plan del proyecto.

La carpeta `plan/` contiene una guía fase por fase para ir desarrollando el proyecto de forma estructurada.

### Ayudas rápidas (Fase 05 · SQL)

- `sql/README.md` describe el flujo completo para ejecutar scripts con Docker y `psql`.
- `scripts/Invoke-Task03Run.ps1` ejecuta los tres análisis avanzados de la Fase 05 · Step 02 · Task 03 sin reescribir los comandos (`powershell -ExecutionPolicy Bypass -File .\scripts\Invoke-Task03Run.ps1 -Script all`).
