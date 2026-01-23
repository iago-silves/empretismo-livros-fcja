from werkzeug.security import generate_password_hash, check_password_hash

from app.infra.database import SessionLocal
from sqlalchemy import select, insert

from app.infra.tables.adm_table import administradores_table
from app.infra.tables.emprestimo_table import emprestimos_table

from app.models.administrador import Administrador
from app.models.usuario import Usuario
from app.models.livro import Livro
from app.models.emprestimo import Emprestimo

class AdministradorService:

    @staticmethod
    def cadastrar_adm(nome, email, senha, session=None):
        session = session or SessionLocal()

        stmt = select(administradores_table).where(administradores_table.c.email == email)

        if session.execute(stmt).first():
            raise ValueError("Erro: Administrador já cadrastado!")

        senha_hash = generate_password_hash(senha)
        
        stmt = insert(administradores_table).values(
            nome = nome,
            email = email,
            senha_hash = senha_hash
        )

        resultado = session.execute(stmt)
        session.commit()

        return {
            "nome": nome,
            "email": email
        }

    @staticmethod
    def autenticar_adm(email, senha, session=None):
        session = session or SessionLocal()

        stmt = select(administradores_table).where(
            administradores_table.c.email == email
            )
        
        resultado = session.execute(stmt).first()

        if not resultado:
            return None
        
        row = resultado._mapping

        admin = Administrador(
            nome=row["nome"],
            email=row["email"],
            senha_hash=row["senha_hash"],
        )

        admin.id = row["id"]
        admin.ativo = row["ativo"]

        if not admin.verificar_senha(senha):
            return None
        
        admin.registrar_login()
        session.commit()

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

        return session.query(emprestimos_table).filter(
            emprestimos_table.c.usuario_id == usuario.id,
            emprestimos_table.c.data_devolucao.is_(None)
        ).count()
    
    @staticmethod
    def autorizar_emprestimo(usuario: Usuario, livro: Livro, prazo_dias: int, session=None):
        session = session or SessionLocal()

        if usuario.id is None or livro.id is None:
            raise ValueError("Usuário e livro precisam estar cadastrados no banco")


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
