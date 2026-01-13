from sqlalchemy.orm import registry
from app.models.administrador import Administrador
from app.infra.tables.adm_table import administradores_table

mapper_registry = registry()
_mappers_started = False


def start_mappers():
    global _mappers_started

    if _mappers_started:
        return

    mapper_registry.map_imperatively(
        Administrador,
        administradores_table
    )

    _mappers_started = True
