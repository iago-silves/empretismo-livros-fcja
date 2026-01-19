from sqlalchemy import Table, Column, Integer, String, Boolean
from app.infra.database import metadata

usuarios_table = Table(
    "usuarios",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nome", String(100), nullable=False),
    Column("email", String(120), nullable=False, unique=True),
    Column("telefone", String(20), nullable=False),
    Column("endereco", String(200), nullable=False),
    Column("bloqueado", Boolean, nullable=False, default=False),
)
