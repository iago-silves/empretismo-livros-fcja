from werkzeug.security import generate_password_hash, check_password_hash

from app.infra.database import SessionLocal
from app.models.administrador import Administrador
from app.models.usuario import Usuario
from app.models.livro import Livro
from app.models.emprestimo import Emprestimo

class AdministradorService:

    @staticmethod
    def cadastrar_adm(nome, email, senha, session=None):
        session = session or SessionLocal()

        if session.query(Administrador).filter_by(email=email).first():
            raise ValueError("Erro: Administrador já cadrastado!")

        senha_hash = generate_password_hash(senha)
        admin = Administrador(nome, email, senha_hash)

        session.add(admin)
        session.commit()
        session.refresh(admin)

        return admin

    @staticmethod
    def autenticar_adm(email, senha, session=None):
        session = session or SessionLocal()

        admin = session.query(Administrador).filter_by(email=email).first()
        if not admin:
            return None

        if not check_password_hash(admin.senha_hash, senha):
            return None

        return admin

    @staticmethod
    def cadastrar_usuario(nome, email, telefone, endereco, session=None):
        session = session or SessionLocal()

        if session.query(Usuario).filter_by(email=email).first():
            raise ValueError("Erro: Usuário já cadastrado!")
        
        usuario = Usuario(
            nome = nome,
            email = email,
            telefone = telefone,
            endereco = endereco
        )

        session.add(usuario)
        session.commit()
        session.refresh(usuario)

        return usuario
    
    @staticmethod
    def buscar_usuario_por_email(email, session=None):
        session = session or SessionLocal()

        return session.query(Usuario).filter_by(email=email).first()
    
    @staticmethod
    def bloquear_usuario(usuario: Usuario, session=None):
        session = session or SessionLocal()
        usuario.bloqueado = True
        session.commit()
    
    @staticmethod
    def desbloquear_usuario(usuario: Usuario, session=None):
        session = session or SessionLocal()
        usuario.bloqueado = False
        session.commit()
    
    @staticmethod
    def quantidade_emprestimos_ativos(usuario: Usuario, session=None) -> int:
        session = session or SessionLocal()

        return session.query(Emprestimo).filter(
            Emprestimo.usuario_id == usuario.id,
            Emprestimo.data_devolucao.is_(None)
        ).count()
    
    @staticmethod
    def autorizar_emprestimo(usuario: Usuario, livro: Livro, prazo_dias: int, session=None):
        session = session or SessionLocal()

        if usuario.bloqueado:
            raise ValueError("Usuário bloqueado")

        if AdministradorService.quantidade_emprestimos_ativos(usuario, session) >= 3:
            raise ValueError("Usuário atingiu o limite de empréstimos")


        emprestimo = Emprestimo(usuario, livro, prazo_dias)

        session.add(emprestimo)
        session.commit()
        session.refresh(emprestimo)

        return emprestimo

    @staticmethod
    def registrar_devolucao(emprestimo: Emprestimo, session=None):
        session = session or SessionLocal()

        emprestimo.devolucao()

        if emprestimo.atrasado():
            emprestimo.usuario.bloqueado = True

        session.commit()

    @staticmethod
    def renovar_emprestimo(emprestimo: Emprestimo, dias: int, session=None):
        session = session or SessionLocal()
        emprestimo.renovar(dias)
        session.commit()
