from werkzeug.security import generate_password_hash

from app.infra.database import SessionLocal
from sqlalchemy import select, insert, update

from datetime import datetime

from app.infra.tables.adm_table import administradores_table
from app.infra.tables.emprestimo_table import emprestimos_table
from app.infra.tables.usuario_table import usuarios_table
from app.infra.tables.livro_table import livros_table

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

        session.execute(stmt)
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
        
        update_stmt = (
            update(administradores_table)
            .where(administradores_table.c.id == admin.id)
            .values(
                ativo=True,
                ultimo_login=datetime.utcnow()
            )
        )

        session.execute(update_stmt)
        session.commit()

        return admin
    
    @staticmethod
    def cadastrar_usuario(nome, email, telefone, endereco, session=None):
        session = session or SessionLocal()

        # Verifica se já existe usuário
        stmt = select(usuarios_table.c.id).where(
            usuarios_table.c.email == email
        )

        if session.execute(stmt).first():
            raise ValueError("Erro: Usuário já cadastrado!")

        # Insere usuário
        stmt = (
            insert(usuarios_table)
            .values(
                nome=nome,
                email=email,
                telefone=telefone,
                endereco=endereco,
                bloqueado=False
            )
            .returning(usuarios_table.c.id)
        )

        result = session.execute(stmt)
        usuario_id = result.scalar_one()

        session.commit()

        return {
            "id": usuario_id,
            "nome": nome,
            "email": email
        }
    
    @staticmethod
    def buscar_usuario_por_email(email, session=None, somente_id=False):
        session = session or SessionLocal()

        if somente_id:
            stmt = select(
                usuarios_table.c.id,
                usuarios_table.c.email
            ).where(usuarios_table.c.email == email)
        else:
            stmt = select(usuarios_table).where(
                usuarios_table.c.email == email
            )

        resultado = session.execute(stmt).first()

        if not resultado:
            return None

        row = resultado._mapping

        if somente_id:
            usuario = Usuario(
                nome="",
                email=row["email"],
                telefone="",
                endereco=""
            )
            usuario.id = row["id"]
            return usuario

        usuario = Usuario(
            nome=row["nome"],
            email=row["email"],
            telefone=row["telefone"],
            endereco=row["endereco"]
        )

        usuario.id = row["id"]
        usuario.bloqueado = row["bloqueado"]

        return usuario
    
    @staticmethod
    def buscar_usuario_por_id(usuario_id, session=None):
        session = session or SessionLocal()

        stmt = select(usuarios_table).where(
            usuarios_table.c.id == usuario_id
        )

        resultado = session.execute(stmt).first()

        if not resultado:
            return None

        row = resultado._mapping

        usuario = Usuario(
            nome=row["nome"],
            email=row["email"],
            telefone=row["telefone"],
            endereco=row["endereco"]
        )

        usuario.id = row["id"]
        usuario.bloqueado = row["bloqueado"]

        return usuario
    
    @staticmethod
    def bloquear_usuario(usuario: Usuario, session=None):
        session = session or SessionLocal()

        stmt = (
            update(usuarios_table)
            .where(usuarios_table.c.id == usuario.id)
            .values(bloqueado=True)
        )

        session.execute(stmt)
        session.commit()
    
    @staticmethod
    def desbloquear_usuario(usuario: Usuario, session=None):
        session = session or SessionLocal()

        stmt = (
            update(usuarios_table)
            .where(usuarios_table.c.id == usuario.id)
            .values(bloqueado=False)
        )

        session.execute(stmt)
        session.commit()
    
    @staticmethod
    def cadastrar_livro(
        autor: str,
        titulo: str,
        editora: str,
        edicao: str,
        ano: int,
        local: str,
        origem: str,
        observacao: str,
        session=None
    ):
        session = session or SessionLocal()

        if not autor or not titulo:
            raise ValueError("Autor e título são obrigatórios")

        stmt = (
            insert(livros_table)
            .values(
                autor=autor,
                titulo=titulo,
                editora=editora,
                edicao=edicao,
                ano=ano,
                local=local,
                origem=origem,
                observacao=observacao
            )
            .returning(livros_table.c.id)
        )

        result = session.execute(stmt)
        livro_id = result.scalar_one()

        session.commit()

        return {
            "mensagem": "Livro cadastrado com sucesso",
            "livro_id": livro_id
        }

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

        stmt = (
            insert(emprestimos_table)
            .values(
                usuario_id=usuario.id,
                livro_id=livro.id,
                prazo_dias=prazo_dias,
                data_emprestimo=emprestimo.data_emprestimo,
                data_prevista_devolucao=emprestimo.data_prevista_devolucao,
                data_devolucao=None
            )
            .returning(emprestimos_table.c.id)
        )

        result = session.execute(stmt)
        emprestimo.id = result.scalar_one()

        session.commit()

        return emprestimo
    
    @staticmethod
    def registrar_devolucao(emprestimo: Emprestimo, session=None):
        session = session or SessionLocal()

        emprestimo.devolucao()

        stmt = (
            update(emprestimos_table)
            .where(emprestimos_table.c.id == emprestimo.id)
            .values(data_devolucao=emprestimo.data_devolucao)
        )

        session.execute(stmt)

        if emprestimo.atrasado():
            stmt_bloqueio = (
                update(usuarios_table)
                .where(usuarios_table.c.id == emprestimo.usuario.id)
                .values(bloqueado=True)
            )
            session.execute(stmt_bloqueio)

        session.commit()

    @staticmethod
    def renovar_emprestimo(emprestimo: Emprestimo, dias: int, session=None):
        session = session or SessionLocal()

        emprestimo.renovar(dias)

        stmt = (
            update(emprestimos_table)
            .where(emprestimos_table.c.id == emprestimo.id)
            .values(
                data_prevista_devolucao=emprestimo.data_prevista_devolucao
            )
        )

        session.execute(stmt)
        session.commit()

    @staticmethod
    def buscar_emprestimo_por_id(emprestimo_id, session=None):
        session = session or SessionLocal()

        stmt = select(emprestimos_table).where(
            emprestimos_table.c.id == emprestimo_id
        )

        result = session.execute(stmt).first()

        if not result:
            return None

        row = result._mapping

        usuario = AdministradorService.buscar_usuario_por_id(
            row["usuario_id"], session
        )

        livro = AdministradorService.buscar_livro_por_id(
            row["livro_id"], session
        )

        if not usuario or not livro:
            return None

        emprestimo = Emprestimo(usuario, livro, prazo_dias=0)

        emprestimo.id = row["id"]
        emprestimo.data_emprestimo = row["data_emprestimo"]
        emprestimo.data_prevista_devolucao = row["data_prevista_devolucao"]
        emprestimo.data_devolucao = row["data_devolucao"]

        return emprestimo

    @staticmethod
    def buscar_livro_por_id(livro_id, session=None):
        session = session or SessionLocal()

        stmt = select(livros_table).where(
            livros_table.c.id == livro_id
        )

        result = session.execute(stmt).first()

        if not result:
            return None

        row = result._mapping

        livro = Livro(
            autor=row["autor"],
            titulo=row["titulo"],
            editora=row["editora"],
            edicao=row["edicao"],
            ano=row["ano"],
            local=row["local"],
            origem=row["origem"],
            observacao=row["observacao"]
        )

        livro.id = row["id"]

        return livro
        