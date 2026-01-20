# tests/test_administrador_service.py
import pytest
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timedelta
from app.infra.database import engine, SessionLocal

Base = declarative_base()

class UsuarioORM(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String, unique=True)
    telefone = Column(String)
    endereco = Column(String)
    bloqueado = Column(Boolean, default=False)


class AdministradorORM(Base):
    __tablename__ = "administradores"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)

    def __init__(self, nome, email, senha_hash):
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.ativo = True

class LivroORM(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    autor = Column(String)
    disponivel = Column(Boolean, default=True)

    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
        self.disponivel = True


class EmprestimoORM(Base):
    __tablename__ = "emprestimos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer)
    livro_id = Column(Integer)
    data_emprestimo = Column(DateTime)
    data_prevista_devolucao = Column(DateTime)
    data_devolucao = Column(DateTime, nullable=True)
    prazo_dias = Column(Integer)
    renovacoes = Column(Integer, default=0)
    exige_presenca_fisica = Column(Boolean, default=False)

    def __init__(self, usuario, livro, prazo_dias):
        self.usuario_id = usuario.id
        self.livro_id = livro.id
        self.usuario = usuario
        self.livro = livro
        self.prazo_dias = prazo_dias
        self.data_emprestimo = datetime.now()
        self.data_prevista_devolucao = self.data_emprestimo + timedelta(days=prazo_dias)
        self.data_devolucao = None
        self.renovacoes = 0
        self.exige_presenca_fisica = False

    def devolucao(self):
        self.data_devolucao = datetime.now()

    def atrasado(self):
        return self.data_prevista_devolucao < datetime.now()
    
    def renovar(self, dias: int):
        self.data_prevista_devolucao += timedelta(days=dias)
        self.renovacoes += 1


import app.models.usuario as usuario_mod
import app.models.administrador as adm_mod
import app.models.livro as livro_mod
import app.models.emprestimo as emprestimo_mod

usuario_mod.Usuario = UsuarioORM
adm_mod.Administrador = AdministradorORM
livro_mod.Livro = LivroORM
emprestimo_mod.Emprestimo = EmprestimoORM

from app.services.administrador_service import AdministradorService

@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine)
    sess = SessionLocal()
    yield sess
    sess.rollback()
    sess.close()
    Base.metadata.drop_all(bind=engine)


def test_cadastrar_administrador_service(session):
    admin = AdministradorService.cadastrar_adm("Admin", "admin@email.com", "123456", session=session)
    assert admin.id is not None
    assert admin.ativo is True


def test_autenticar_admin(session):
    AdministradorService.cadastrar_adm("Admin", "admin@email.com", "123456", session=session)
    admin = AdministradorService.autenticar_adm("admin@email.com", "123456", session=session)
    assert admin is not None


def test_cadastrar_usuario_sucesso(session):
    usuario = AdministradorService.cadastrar_usuario("João", "joao@email.com", "999999", "Rua A, 123", session=session)
    session.commit()  # garante ID
    assert usuario.id is not None
    assert usuario.bloqueado is False

def test_quantidade_emprestimos_ativos(session):
    usuario = AdministradorService.cadastrar_usuario("Alice", "alice@email.com", "111111", "Rua X", session=session)
    livro = LivroORM(titulo="Livro A", autor="Autor A")
    session.add(livro)
    session.commit()

    # Nenhum empréstimo ainda
    qtde = AdministradorService.quantidade_emprestimos_ativos(usuario, session)
    assert qtde == 0

    # Cria um empréstimo
    AdministradorService.autorizar_emprestimo(usuario, livro, 7, session=session)
    qtde = AdministradorService.quantidade_emprestimos_ativos(usuario, session)
    assert qtde == 1


def test_autorizar_emprestimo_limite(session):
    usuario = AdministradorService.cadastrar_usuario("Bob", "bob@email.com", "222222", "Rua Y", session=session)
    livros = [LivroORM(titulo=f"Livro {i}", autor="Autor") for i in range(4)]
    session.add_all(livros)
    session.commit()

    # Autoriza até 3 empréstimos
    for i in range(3):
        AdministradorService.autorizar_emprestimo(usuario, livros[i], 7, session=session)

    with pytest.raises(ValueError) as erro:
        AdministradorService.autorizar_emprestimo(usuario, livros[3], 7, session=session)
    assert "Usuário atingiu o limite" in str(erro.value)


def test_registrar_devolucao_bloqueia_usuario(session):
    usuario = AdministradorService.cadastrar_usuario("Carol", "carol@email.com", "333333", "Rua Z", session=session)
    livro = LivroORM("Livro B", "Autor B")
    session.add(livro)
    session.commit()

    emprestimo = AdministradorService.autorizar_emprestimo(usuario, livro, 1, session=session)
    # Simula atraso
    emprestimo.data_prevista_devolucao = emprestimo.data_emprestimo - timedelta(days=1)
    AdministradorService.registrar_devolucao(emprestimo, session=session)
    assert usuario.bloqueado is True


def test_renovar_emprestimo(session):
    usuario = AdministradorService.cadastrar_usuario("Dan", "dan@email.com", "444444", "Rua W", session=session)
    livro = LivroORM("Livro C", "Autor C")
    session.add(livro)
    session.commit()

    emprestimo = AdministradorService.autorizar_emprestimo(usuario, livro, 7, session=session)
    AdministradorService.renovar_emprestimo(emprestimo, 15, session=session)
    assert emprestimo.renovacoes == 1
    assert emprestimo.data_prevista_devolucao > emprestimo.data_emprestimo
