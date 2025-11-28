# Introducción a Docker y Docker Compose

Este proyecto usa Docker y Docker Compose para levantar un contenedor con PostgreSQL de forma reproducible y aislada de tu sistema operativo.

## ¿Qué es Docker?

Docker es una plataforma que permite empaquetar aplicaciones y sus dependencias en contenedores ligeros. Un contenedor es un proceso aislado que tiene todo lo necesario para ejecutar una aplicación (binarios, librerías, configuración mínima).

Beneficios principales:

- Entornos reproducibles.
- Aislamiento respecto a la máquina host.
- Fácil despliegue en otras máquinas.

## ¿Qué es Docker Compose?

Docker Compose es una herramienta para definir y ejecutar aplicaciones multi-contenedor usando archivos YAML (por ejemplo `docker-compose.yml`).

En este repositorio utilizamos el archivo `docker-compose.postgresql.yml` para describir el servicio de base de datos PostgreSQL que necesita el proyecto.

## Requisitos previos

- Tener instalado Docker Desktop (Windows / macOS) o Docker Engine (Linux).
- Docker Compose viene integrado en Docker Desktop.

Puedes verificar la instalación con:

```bash
docker --version
docker compose version
```

## Archivo `docker-compose.postgresql.yml`

En la raíz del proyecto hay un archivo llamado `docker-compose.postgresql.yml` que define un servicio `postgres` con la imagen oficial de PostgreSQL.

Puntos clave:

- La versión de PostgreSQL se controla con la variable de entorno `POSTGRES_VERSION` (recomendada).
- El puerto externo se controla con `POSTGRES_PORT` (recomendado).
- Se crea un volumen `postgres_data` para persistir los datos.
- Las credenciales mínimas necesarias son `POSTGRES_DB`, `POSTGRES_USER` y `POSTGRES_PASSWORD`.
- Opcionalmente puedes definir `POSTGRES_HOST` y/o `DATABASE_URL`.

Todas estas variables se leen desde un archivo `.env` (que tú vas a crear a partir de `.env.example`). En ese archivo se indica cuáles son obligatorias y cuáles son opcionales.

## Comandos básicos con Docker Compose

Desde la raíz del proyecto, con tu archivo `.env` ya configurado:

- Levantar el contenedor en segundo plano:

```bash
docker compose -f docker-compose.postgresql.yml up -d
```

- Ver el estado de los servicios:

```bash
docker compose -f docker-compose.postgresql.yml ps
```

- Ver logs del contenedor de PostgreSQL:

```bash
docker compose -f docker-compose.postgresql.yml logs -f postgres
```

- Detener los contenedores (manteniendo los datos en el volumen):

```bash
docker compose -f docker-compose.postgresql.yml down
```

- Detener los contenedores y eliminar los volúmenes (¡borra los datos!):

```bash
docker compose -f docker-compose.postgresql.yml down -v
```

---

Para detalles específicos de configuración de PostgreSQL en este proyecto, revisa también `docs/postgresql/intro-postgresql.md`.
