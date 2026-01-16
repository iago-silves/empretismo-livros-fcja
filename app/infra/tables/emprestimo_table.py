from sqlalchemy import (Table, Column, Integer, Boolean, DateTime, ForeignKey)
from app.infra.database import metadata

emprestimos_table = Table(
    "emprestimos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False),
    Column("livro_id", Integer, ForeignKey("livros.id"), nullable=False),
    Column("data_emprestimo", DateTime, nullable=False),
    Column("data_prevista_devolucao", DateTime, nullable=False),
    Column("data_devolucao", DateTime, nullable=True),
    Column("prazo_dias", Integer, nullable=False),
    Column("renovacoes", Integer, nullable=False, default=0),
    Column("exige_presenca_fisica", Boolean, nullable=False, default=False)
)