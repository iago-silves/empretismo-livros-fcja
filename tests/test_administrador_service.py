from sqlalchemy.orm.session import Session
from app.services.administrador_service import AdministradorService

def test_criar_administrador(session: Session):
    admin = AdministradorService.criar(
        nome="Admin",
        email="admin@email.com",
        senha="123456",
        session=session
    )

    assert admin.id is not None # type: ignore
