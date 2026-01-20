import pytest
from app.infra.database import SessionLocal
from app.models.usuario import Usuario


@pytest.fixture
def session():
    session = SessionLocal()

    # Limpa a tabela antes de cada teste
    session.query(Usuario).delete()
    session.commit()

    yield session

    session.close()
