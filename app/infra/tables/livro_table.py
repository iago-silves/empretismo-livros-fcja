from sqlalchemy import Table, Column, Integer, String
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
    Column("local", String(100), nullable=False),
    Column("origem", String(100), nullable=False),
    Column("observacao", String(255), nullable=True),
)