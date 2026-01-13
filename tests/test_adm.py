from app.models.administrador import Administrador

def test_criar_administrador():
    admin = Administrador(
        nome="Admin",
        email="admin@email.com",
        senha_hash="hash123"
    )

    assert admin.nome == "Admin"
    assert admin.email == "admin@email.com"
    assert admin.ativo is True
