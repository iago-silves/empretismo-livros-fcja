import pytest

from sqlalchemy.orm.session import Session
from app.models.administrador import Administrador
from app.services.administrador_service import AdministradorService


def test_criar_administrador(session: Session):
    admin = AdministradorService.cadastrar_adm(
        nome="Admin",
        email="admin@email.com",
        senha="123456",
        session=session
    )

    assert admin.id is not None 


def test_cadastro_adm():
    admin = Administrador(
        nome="Admin",
        email="admin@email.com",
        senha_hash="hash123"
    )

    assert admin.nome == "Admin"
    assert admin.email == "admin@email.com"
    assert admin.ativo is True



def test_autenticar_admin(session):
    AdministradorService.cadastrar_adm(
        nome="Admin",
        email="admin@email.com",
        senha="123456",
        session=session
    )

    admin = AdministradorService.autenticar_adm(
        email="admin@email.com",
        senha="123456",
        session=session
    )

    assert admin is not None
