from sqlalchemy.orm import registry
from app.models.administrador import Administrador
from app.models.livro import Livro
from app.models.emprestimo import Emprestimo
from app.models.usuario import Usuario
from app.infra.tables.adm_table import administradores_table
from app.infra.tables.livro_table import livros_table
from app.infra.tables.emprestimo_table import emprestimos_table
from app.infra.tables.usuario_table import usuarios_table

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

    mapper_registry.map_imperatively(
        Livro,
        livros_table
    )

    mapper_registry.map_imperatively(
        Emprestimo,
        emprestimos_table
    )

    mapper_registry.map_imperatively(
        Usuario,
        usuarios_table
    )

    _mappers_started = True
