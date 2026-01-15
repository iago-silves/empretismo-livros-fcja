from sqlalchemy import Table, Column, Integer, String, Boolean
from app.infra.database import metadata

livros_table = Table(
    "livros",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("autor", String(150), nullable=False),
    Column("titulo", String(200), nullable=False),
    Column("editora", String(150), nullable=False),
    Column("edicao", String(50), nullable=False),
    Column("ano", Integer, nullable=False),
    Column("origem", String(100), nullable=False),
    Column("observação", String(255), nullable=True),
    Column("disponivel", Boolean, nullable=False, default=True),
)