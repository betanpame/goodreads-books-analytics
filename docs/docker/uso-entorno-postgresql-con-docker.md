# Uso del entorno PostgreSQL con Docker en este proyecto

Este documento explica paso a paso cómo usar el entorno de base de datos PostgreSQL provisto por Docker y Docker Compose en este repositorio.

## 1. Preparar variables de entorno

1. En la raíz del repositorio, copia el archivo de ejemplo:

```powershell
Copy-Item .env.example .env
```

2. Abre `.env` con tu editor favorito y revisa/ajusta:

**Variables OBLIGATORIAS**

- `POSTGRES_DB`: nombre de la base de datos.
- `POSTGRES_USER`: usuario administrador.
- `POSTGRES_PASSWORD`: contraseña (cámbiala por algo seguro).

**Variables RECOMENDADAS / OPCIONALES**

- `PROJECT_NAME`: identificador del proyecto (puede dejarse por defecto).
- `POSTGRES_VERSION`: versión de la imagen de PostgreSQL (por ejemplo `17`, `16`, `15-alpine`).
- `POSTGRES_PORT`: puerto de tu máquina a mapear con el 5432 del contenedor.
- `POSTGRES_HOST`: host al que se conectarán los scripts de Python (normalmente `localhost`).
- `DATABASE_URL`: si la defines, los scripts de Python usarán esta URL directamente.

## 2. Levantar la base de datos

Desde la raíz del proyecto:

```powershell
docker compose -f docker-compose.postgresql.yml up -d
```

Este comando:

- Lee las variables de `.env`.
- Arranca el servicio `postgres`.
- Crea (si no existe) el volumen `postgres_data` donde se guardan los datos.

Para ver el estado de los servicios:

```powershell
docker compose -f docker-compose.postgresql.yml ps
```

## 3. Ver logs y diagnosticar problemas

Para ver los logs del contenedor:

```powershell
docker compose -f docker-compose.postgresql.yml logs -f postgres
```

Si el contenedor no arranca:

- Revisa que `POSTGRES_PASSWORD` no esté vacío.
- Revisa que el puerto definido en `POSTGRES_PORT` no esté ocupado.

## 4. Conectarse a la base de datos

### 4.1. Usando `psql` dentro del contenedor

```powershell
docker compose -f docker-compose.postgresql.yml exec -u postgres postgres psql -d goodreads
```

(ajusta el nombre de la base de datos si cambiaste `POSTGRES_DB`).

### 4.2. Usando un cliente externo (GUI) o scripts Python

Parámetros típicos de conexión:

- Host: `localhost`
- Puerto: valor de `POSTGRES_PORT`
- Base de datos: valor de `POSTGRES_DB`
- Usuario: valor de `POSTGRES_USER`
- Contraseña: valor de `POSTGRES_PASSWORD`

## 5. Detener y limpiar

Para detener los contenedores, manteniendo los datos en el volumen:

```powershell
docker compose -f docker-compose.postgresql.yml down
```

Para detener los contenedores y eliminar el volumen (se borran los datos):

```powershell
docker compose -f docker-compose.postgresql.yml down -v
```

## 6. Relación con otras fases del proyecto

- En las fases de **carga de datos** y **análisis en SQL**, este servicio PostgreSQL será el destino donde se cargará la información del CSV de Goodreads.
- Los scripts en `src/` deberán configurarse para leer las variables de entorno de conexión (por ejemplo con `os.getenv`) de forma que sea fácil cambiar de entorno (desarrollo, pruebas, producción).

Revisa también:

- `docs/docker/intro-docker-y-docker-compose.md` para conceptos básicos.
- `docs/postgresql/intro-postgresql.md` para detalles de PostgreSQL.
