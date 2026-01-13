from werkzeug.security import generate_password_hash, check_password_hash
from app.models.administrador import Administrador
from app.infra.database import SessionLocal


class AdministradorService:

    @staticmethod
    def criar(nome, email, senha, session=None):
        session = session or SessionLocal()

        if session.query(Administrador).filter_by(email=email).first():
            raise ValueError("Administrador já existe")

        senha_hash = generate_password_hash(senha)
        admin = Administrador(nome, email, senha_hash)

        session.add(admin)
        session.commit()
        session.refresh(admin)

        return admin

    @staticmethod
    def autenticar(email, senha, session=None):
        session = session or SessionLocal()

        admin = session.query(Administrador).filter_by(email=email).first()
        if not admin:
            return None

        if not check_password_hash(admin.senha_hash, senha):
            return None

        return admin
