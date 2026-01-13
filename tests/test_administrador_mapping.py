from app.models.administrador import Administrador

def test_persistir_administrador(session):
    admin = Administrador(
        nome="Admin",
        email="admin@email.com",
        senha_hash="hash"
    )

    session.add(admin)
    session.commit()

    admin_db = session.query(Administrador).first()

    assert admin_db.email == "admin@email.com"
