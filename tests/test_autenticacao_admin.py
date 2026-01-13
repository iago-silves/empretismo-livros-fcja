from app.services.administrador_service import AdministradorService

def test_autenticar_admin(session):
    AdministradorService.criar(
        nome="Admin",
        email="admin@email.com",
        senha="123456",
        session=session
    )

    admin = AdministradorService.autenticar(
        email="admin@email.com",
        senha="123456",
        session=session
    )

    assert admin is not None
