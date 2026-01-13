from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime
from app.infra.database import metadata

administradores_table = Table(
    "administradores",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nome", String(100), nullable=False),
    Column("email", String(120), unique=True, nullable=False),
    Column("senha_hash", String(255), nullable=False),
    Column("ativo", Boolean, default=True),
    Column("criado_em", DateTime, nullable=False),
    Column("ultimo_login", DateTime, nullable=True),
)
