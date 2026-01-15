from sqlalchemy import (Table, Column, Integer, DateTime, ForeingnKey)
from app.infra.database import metadata

emprestimos_table = Table(
    "emprestimos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("usuario_id", Integer, ForeingnKey("usuarios.id"), nullable=False),
    Column("livro_id", Integer, ForeingnKey("livros.id"), nullable=False),
    Column("data_emprestimo", DateTime, nullable=False),
    Column("data_prevista_devolucao", DateTime, nullable=False),
    Column("data_devolucao", DateTime, nullable=True),
    Column("prazo_dias", Integer, nullable=False),
    Column("renovacoes", Integer, nullable=False, default=0),
)