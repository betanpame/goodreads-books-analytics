## Comparar SQL vs pandas (Fase 05 · Step 03)

Este paso verifica que los análisis SQL de la fase 05 coinciden con los CSV generados en pandas (fase 04).

### Ejecución rápida (recomendada)

````powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Invoke-Phase05ComparisonRefresh.ps1

### Pasos manuales

1. **Levanta los contenedores**

2. **Carga el dataset curado a PostgreSQL** (solo cuando `books_clean` cambie)

   ```powershell
   docker compose -f docker-compose.python.yml run --rm app `
   	python -m src.load_books_clean_to_postgres `
   	--csv-path data/derived/books_clean.csv `
   	--table books_clean
````

3. **Ejecuta el comparador SQL vs pandas**

   ```powershell
   docker compose -f docker-compose.python.yml run --rm app `
   	python -m src.analyses.portfolio.p04_sql_vs_pandas_compare `
   	--output-dir outputs/phase05_step03_task01
   ```

Resultados clave:

...

### Solución de problemas rápida

1. `*_differences.csv` presente → inspecciona el archivo correspondiente en `outputs/phase05_step03_task01/` para ver filas divergentes.

2. Vuelve a cargar `books_clean` con `scripts/Invoke-Phase05ComparisonRefresh.ps1` (o el paso manual 2) para garantizar que Postgres usa el CSV curado más reciente.

3. Ejecuta de nuevo el comparador; si la discrepancia persiste, revisa los SQL involucrados y actualiza la lógica en `src/analyses/sql_vs_pandas_compare.py`.

---

## SQL Portfolio Spotlight (Fase 05)

Durante Step 03 consolidamos todo el trabajo SQL dentro del flujo de Python/Docker para que cualquier reclutador pueda reproducirlo sin abrir notebooks. El guion es el siguiente:

- **Narrativa** -> Partimos de los CSV generados en pandas (Fase 04), los cargamos en PostgreSQL con `src.load_books_clean_to_postgres`, y luego usamos `src.analyses.portfolio.p04_sql_vs_pandas_compare` para demostrar que ambas capas responden las mismas preguntas de negocio.

### Capacidades SQL practicadas

| Activo                                                          | Descripción                                               | Cómo regenerarlo                                                                                                       |
| --------------------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `outputs/phase05_step03_task01/comparison_summary.{csv,md,png}` | Evidencia cuantitativa y visual del parity SQL vs pandas. | `docker compose -f docker-compose.python.yml run --rm app python -m src.analyses.portfolio.p04_sql_vs_pandas_compare`. |

# goodreads-books-analytics

Proyecto de análisis del dataset de libros de Goodreads con Python, PostgreSQL y Docker.

Este repositorio incluye:

- Scripts de limpieza y carga de datos en `src/`.
- Tests básicos en `tests/`.
- Documentación de apoyo en `docs/` (pandas, SQL, Docker, PostgreSQL).
- Un entorno de base de datos basado en Docker Compose para PostgreSQL.

## Start Here Map

Sigue las fases en orden; cada paso enlaza a sus notas y te recuerda los prerequisitos antes de ejecutar nada.

1. **Phase 01 – Project Setup and Environment**

   - [Step 01 – Understand Repository and Tools](plan/phase-01-project-setup-and-environment/steps/step-01-understand-repo-and-tools/) — Recorrido guiado por la estructura del repo y checklist de utilidades básicas. _Prereqs: repo clonado, Git + VS Code instalados._ Notas: [T1](docs/phase-01-step-01-task-01-notes.md) · [T2](docs/phase-01-step-01-task-02-notes.md) · [T3](docs/phase-01-step-01-task-03-notes.md)
   - [Step 02 – Design Python CLI Docker Environment](plan/phase-01-project-setup-and-environment/steps/step-02-design-python-docker-environment/) — Define la imagen/base de dependencias y variables necesarias para los contenedores de análisis. _Prereqs: Step 01 completado, Docker Desktop instalado._ Notas: [T1](docs/phase-01-step-02-task-01-notes.md) · [T2](docs/phase-01-step-02-task-02-notes.md) · [T3](docs/phase-01-step-02-task-03-notes.md)
   - [Step 03 – Implement and Test Docker Setup](plan/phase-01-project-setup-and-environment/steps/step-03-implement-and-test-docker-setup/) — Construye y prueba los contenedores de Python/PostgreSQL con comandos reproducibles. _Prereqs: Step 02 configurado, `.env` inicializado._ Notas: [T1](docs/phase-01-step-03-task-01-notes.md) · [T2](docs/phase-01-step-03-task-02-notes.md) · [T3](docs/phase-01-step-03-task-03-notes.md)

2. **Phase 02 – Data Loading and Initial Exploration**

   - [Step 01 – Inspect Dataset with pandas](plan/phase-02-data-loading-and-initial-exploration/steps/step-01-inspect-dataset-with-pandas/) — Abre `books.csv`, genera `.info()`/`.describe()` y detecta columnas clave. _Prereqs: Phase 01 entorno activo, archivo `data/books.csv` disponible._ Notas: [T1](docs/phase-02-step-01-task-01-notes.md) · [T2](docs/phase-02-step-01-task-02-notes.md) · [T3](docs/phase-02-step-01-task-03-notes.md)
   - [Step 02 – Design PostgreSQL Schema](plan/phase-02-data-loading-and-initial-exploration/steps/step-02-design-postgres-schema/) — Propone tablas/campos y define tipos para la futura carga. _Prereqs: Step 01 resuelto, conexión a PostgreSQL lista._ Notas: [T1](docs/phase-02-step-02-task-01-notes.md) · [T2](docs/phase-02-step-02-task-02-notes.md) · [T3](docs/phase-02-step-02-task-03-notes.md)
   - [Step 03 – Load Data into PostgreSQL](plan/phase-02-data-loading-and-initial-exploration/steps/step-03-load-data-into-postgres/) — Ejecuta la primera carga `books.csv → postgres` y documenta comandos `COPY`/Python. _Prereqs: Step 02 aprobado, contenedor postgres encendido._ Notas: [T1](docs/phase-02-step-03-task-01-notes.md) · [T2](docs/phase-02-step-03-task-02-notes.md) · [T3](docs/phase-02-step-03-task-03-notes.md)

3. **Phase 03 – EDA and Data Quality Assessment**

   - [Step 01 – Univariate EDA](plan/phase-03-eda-and-data-quality/steps/step-01-univariate-eda/) — Explora distribuciones y outliers clave. _Prereqs: Phase 02 outputs (`books_clean` preliminar) listos._ Notas: [T1](docs/phase-03-step-01-task-01-notes.md) · [T2](docs/phase-03-step-01-task-02-notes.md) · [T3](docs/phase-03-step-01-task-03-notes.md)
   - [Step 02 – Bivariate and Relationships](plan/phase-03-eda-and-data-quality/steps/step-02-bivariate-eda/) — Cruza métricas (p.ej., rating vs. páginas) y registra hallazgos. _Prereqs: Step 01 gráficos/CSV exportados._ Notas: [T1](docs/phase-03-step-02-task-01-notes.md) · [T2](docs/phase-03-step-02-task-02-notes.md) · [T3](docs/phase-03-step-02-task-03-notes.md)
   - [Step 03 – Data Quality + Cleaning Rules](plan/phase-03-eda-and-data-quality/steps/step-03-data-quality-and-cleaning-rules/) — Define reglas de limpieza y documenta decisiones sobre nulos, duplicados y formatos. _Prereqs: Step 02 insights, `docs/dataset-notes.md` abierto._ Notas: [T1](docs/phase-03-step-03-task-01-notes.md) · [T2](docs/phase-03-step-03-task-02-notes.md) · [T3](docs/phase-03-step-03-task-03-notes.md)

4. **Phase 04 – Business Analysis and Visualizations**

   - [Step 01 – Implement Cleaning in Python](plan/phase-04-business-analysis-and-visualizations/steps/step-01-implement-cleaning-in-python/) — Aplica reglas de Phase 03 para producir `books_clean.csv`. _Prereqs: data-quality plan cerrado._ Notas: [T1](docs/phase-04-step-01-task-01-notes.md)
   - [Step 02 – Define Metrics and Visuals](plan/phase-04-business-analysis-and-visualizations/steps/step-02-define-and-compute-metrics/) — Calcula KPIs y prototipa visualizaciones base. _Prereqs: Step 01 dataset limpio, métricas en `src/metrics/core_metrics.py`._ Notas: [T1](docs/phase-04-step-02-task-01-notes.md) · [T2](docs/phase-04-step-02-task-02-notes.md)

5. **Phase 05 – SQL Analysis in PostgreSQL**

   - [Step 01 – Validate Data in PostgreSQL](plan/phase-05-sql-analysis-in-postgres/steps/step-01-validate-data-in-postgres/) — Ejecuta CLIs de validación para comprobar schema/filas. _Prereqs: Docker stack (`python` + `postgresql`) operativo._ Notas: [T1](docs/phase-05-step-01-task-01-notes.md) · [T2](docs/phase-05-step-01-task-02-notes.md) · [T3](docs/phase-05-step-01-task-03-notes.md)
   - [Step 02 – Implement Core SQL Queries](plan/phase-05-sql-analysis-in-postgres/steps/step-02-implement-analysis-queries/) — Redacta queries con CTEs, window functions y tablas canónicas. _Prereqs: Step 01 parity checks verdes._ Notas: [T1](docs/phase-05-step-02-task-01-notes.md) · [T2](docs/phase-05-step-02-task-02-notes.md) · [T3](docs/phase-05-step-02-task-03-notes.md)
   - [Step 03 – SQL vs pandas Comparison](plan/phase-05-sql-analysis-in-postgres/steps/step-03-sql-vs-pandas-comparison/) — Corre `p04_sql_vs_pandas_compare` y documenta evidencias para portafolio. _Prereqs: Step 02 queries almacenadas, métricas de Phase 04._ Notas: [T1](docs/phase-05-step-03-task-01-notes.md) · [T2](docs/phase-05-step-03-task-02-notes.md)

6. **Phase 06 – Documentation and Storytelling**

   - [Step 01 – Organize Portfolio Scripts](plan/phase-06-documentation-and-storytelling/steps/step-01-organize-src/analyses/) — Reestructura `src/analyses/` en portfolio/support/archive y agrega docstrings. _Prereqs: Phase 05 artefactos generados, pruebas básicas verdes._ Notas: [T1](docs/phase6-step1-task1-notes.md) · [T2](docs/phase6-step1-task2-notes.md) · [T3](docs/phase6-step1-task3-notes.md)

7. **Phase 07 – Production Readiness and Next Steps**
   - [Step 01 – Refine Docker Setup](plan/phase-07-production-readiness-and-next-steps/steps/step-01-refine-docker-setup/) — Consolida los archivos de orquestación para compartir el entorno. _Prereqs: Fases 01–06 consolidadas._
   - [Step 02 – Document End-to-End Run Instructions](plan/phase-07-production-readiness-and-next-steps/steps/step-02-document-run-instructions/) — Redacta guías rápidas para reclutadores o colaboradores. _Prereqs: Step 01 contenedores listos._
   - [Step 03 – Define Cloud + Extension Roadmap](plan/phase-07-production-readiness-and-next-steps/steps/step-03-define-next-steps/) — Lista mejoras futuras (deploy cloud, dashboards, jobs). _Prereqs: Runbook del Step 02 publicado._

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

## SQL Portfolio Spotlight (Fase 05)

Durante Step 03 consolidamos todo el trabajo SQL dentro del flujo de Python/Docker para que cualquier reclutador pueda reproducirlo sin abrir notebooks. El guion es el siguiente:

- **Narrativa** → Partimos de los CSV generados en pandas (Fase 04), los cargamos en PostgreSQL con `src.load_books_clean_to_postgres`, y luego usamos `src.analyses.sql_vs_pandas_compare` para demostrar que ambas capas responden las mismas preguntas de negocio.
- **Preguntas respondidas** → Rankings de autores/libros, evolución temporal de ratings, idiomas/publishers más sólidos, duplicados, engagement percentiles y rolling windows.
- **Entrega visual** → `scripts/Invoke-Phase05ComparisonRefresh.ps1 -ExportSlide` refresca métricas, genera `comparison_summary.png` y exporta una diapositiva (`outputs/phase05_step03_task01/phase05_sql_vs_pandas.pptx`) lista para portfolios o entrevistas.

### Capacidades SQL practicadas

- Agrupaciones con `GROUP BY`, filtros con `HAVING` y cláusulas `WHERE` parametrizadas vía CTEs.
- Ventanas (`ROW_NUMBER`, `PERCENTILE_CONT`, frames de 3 años) para rankings por autor y métricas rolling.
- Combinación de vistas canonicalizadas + staging (`book_authors_stage`) para evitar duplicados en los KPIs.
- Exportación repetible desde Python (sin Jupyter) usando Docker Compose para garantizar el mismo entorno en cualquier máquina.

### Activos para mostrar en el portfolio

| Activo                                                          | Descripción                                                    | Cómo regenerarlo                                                                                           |
| --------------------------------------------------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `README.md` · sección “SQL Portfolio Spotlight”                 | Resumen ejecutivo en tono profesional, listo para recruiters.  | Actual archivo (sin pasos adicionales).                                                                    |
| `docs/phase-05-step-03-task-02-notes.md`                        | Bitácora detallada (paso a paso, comandos PowerShell).         | `powershell -ExecutionPolicy Bypass -File .\scripts\Invoke-Phase05ComparisonRefresh.ps1` + seguir la nota. |
| `outputs/phase05_step03_task01/comparison_summary.{csv,md,png}` | Evidencia cuantitativa y visual del parity SQL vs pandas.      | `docker compose -f docker-compose.python.yml run --rm app python -m src.analyses.sql_vs_pandas_compare`.   |
| `docs/phase-05-step-03-task-01-slide.pptx`                      | Diapositiva con storytelling (ingresa directo en portafolios). | `scripts/Invoke-Phase05ComparisonRefresh.ps1 -ExportSlide`.                                                |

Toda la fase opera con `docker compose` y módulos de Python; evita notebooks para mantener trazabilidad y favorecer automatización/CI. Para más contexto, revisa las notas del Task 02 (`docs/phase-05-step-03-task-02-notes.md`).

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
