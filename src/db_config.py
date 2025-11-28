"""Utilidades para construir la URL de conexión a PostgreSQL.

Este módulo centraliza la lógica de lectura de variables de entorno
relacionadas con la base de datos y la construcción de ``DATABASE_URL``
para SQLAlchemy.

Se integra con la configuración basada en Docker descrita en
``docker-compose.postgresql.yml`` y en el archivo ``.env``.
"""
from __future__ import annotations

import os
from typing import Final


DEFAULT_DB_NAME: Final[str] = "goodreads"
DEFAULT_DB_USER: Final[str] = "goodreads_user"
DEFAULT_DB_PASSWORD: Final[str] = ""
DEFAULT_DB_HOST: Final[str] = "localhost"
DEFAULT_DB_PORT: Final[str] = "5432"


def build_database_url_from_env() -> str:
    """Construye una URL de conexión ``DATABASE_URL`` a partir de variables de entorno.

    Este helper permite configurar la conexión usando las variables
    proporcionadas en ``.env`` para el entorno Docker de PostgreSQL:

    - ``POSTGRES_DB``
    - ``POSTGRES_USER``
    - ``POSTGRES_PASSWORD``
    - ``POSTGRES_HOST`` (opcional, por defecto ``localhost``)
    - ``POSTGRES_PORT`` (opcional, por defecto ``5432``)

    Si ya existe ``DATABASE_URL`` en el entorno, se devuelve tal cual
    para mantener compatibilidad con configuraciones previas.
    """

    existing_url = os.getenv("DATABASE_URL")
    if existing_url:
        return existing_url

    db_name = os.getenv("POSTGRES_DB", DEFAULT_DB_NAME)
    db_user = os.getenv("POSTGRES_USER", DEFAULT_DB_USER)
    db_password = os.getenv("POSTGRES_PASSWORD", DEFAULT_DB_PASSWORD)
    db_host = os.getenv("POSTGRES_HOST", DEFAULT_DB_HOST)
    db_port = os.getenv("POSTGRES_PORT", DEFAULT_DB_PORT)

    if not db_name or not db_user:
        raise RuntimeError(
            "POSTGRES_DB y POSTGRES_USER deben estar definidos o bien proporcionar "
            "directamente DATABASE_URL en el entorno."
        )

    return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
