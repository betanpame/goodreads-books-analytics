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

## Comparar SQL vs pandas (Fase 05 · Step 03)

Este paso verifica que los análisis SQL de la fase 05 coinciden con los CSV generados en pandas (fase 04).

### Ejecución rápida (recomendada)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Invoke-Phase05ComparisonRefresh.ps1
```

El script anterior levanta los contenedores, recarga `books_clean`, ejecuta el comparador y regenera el gráfico `comparison_summary.png`. Usa `-Cases` para limitar métricas o `-SkipChart` si no necesitas el PNG.

### Pasos manuales

1. **Levanta los contenedores**

   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
   ```

2. **Carga el dataset curado a PostgreSQL** (solo cuando `books_clean` cambie)

   ```powershell
   docker compose -f docker-compose.python.yml run --rm app `
   	python -m src.load_books_clean_to_postgres `
   	--csv-path data/derived/books_clean.csv `
   	--table books_clean
   ```

3. **Ejecuta el comparador SQL vs pandas**

   ```powershell
   docker compose -f docker-compose.python.yml run --rm app `
   	python -m src.analyses.sql_vs_pandas_compare `
   	--output-dir outputs/phase05_step03_task01
   ```

Resultados clave:

- `outputs/phase05_step03_task01/comparison_summary.csv` y `.md` muestran métricas, filas y estado (`Match`).
- `outputs/phase05_step03_task01/comparison_summary.png` brinda un gráfico listo para presentaciones.
- Archivos `*_differences.csv` solo aparecen cuando existen discrepancias; si quieres reiniciar la evidencia, elimina esos archivos y vuelve a correr el comando.
- Documentación extendida: `docs/phase-05-step-03-task-01-notes.md`.

### Solución de problemas rápida

1. `*_differences.csv` presente → inspecciona el archivo correspondiente en `outputs/phase05_step03_task01/` para ver filas divergentes.
2. Vuelve a cargar `books_clean` con `scripts/Invoke-Phase05ComparisonRefresh.ps1` (o el paso manual 2) para garantizar que Postgres usa el CSV curado más reciente.
3. Ejecuta de nuevo el comparador; si la discrepancia persiste, revisa los SQL involucrados y actualiza la lógica en `src/analyses/sql_vs_pandas_compare.py`.

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
