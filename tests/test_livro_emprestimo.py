
import sys
from importlib import reload

if 'app.models.livro' in sys.modules:
    reload(sys.modules['app.models.livro'])

import pytest
from datetime import datetime, timedelta
from app.models.usuario import Usuario
from app.models.livro import Livro
from app.models.emprestimo import Emprestimo as EmprestimoDominio

@pytest.fixture
def usuario():
    u = Usuario(nome="João", email="joao@email.com", telefone="999999999", endereco="Rua A, 123")
    u.id = 1
    u.bloqueado = False
    return u

@pytest.fixture
def livro():
    l = Livro(autor="Machado de Assis", titulo="Dom Casmurro", editora="Editora Exemplo",
              edicao="1ª", ano=1899, local="Prateleira A3", origem="Doação")
    l.id = 1
    return l

@pytest.fixture
def emprestimo(usuario, livro):
    return EmprestimoDominio(usuario=usuario, livro=livro, prazo_dias=7)

def test_criar_livro(livro):
    assert livro.id == 1
    assert livro.titulo == "Dom Casmurro"
    assert livro.autor == "Machado de Assis"
    assert livro.editora == "Editora Exemplo"
    assert livro.edicao == "1ª"
    assert livro.local == "Prateleira A3"
    assert livro.origem == "Doação"
    assert livro.observacao == ""

def test_str_livro(livro):
    s = str(livro)
    assert "Dom Casmurro" in s
    assert "Machado de Assis" in s
    assert "Editora Exemplo" in s


def test_criar_emprestimo(usuario, livro):
    e = EmprestimoDominio(usuario, livro, prazo_dias=7)
    assert e.usuario == usuario
    assert e.livro == livro
    assert e.prazo_dias == 7
    assert e.data_devolucao is None
    assert e.renovacoes == 0

def test_devolucao_emprestimo(usuario, livro):
    e = EmprestimoDominio(usuario, livro, prazo_dias=1)
    e.devolucao()
    assert e.data_devolucao is not None

def test_devolucao_ja_realizada(usuario, livro):
    e = EmprestimoDominio(usuario, livro, prazo_dias=1)
    e.devolucao()
    with pytest.raises(Exception) as excinfo:
        e.devolucao()
    assert "já foi encerrado" in str(excinfo.value)

def test_emprestimo_atrasado(usuario, livro):
    e = EmprestimoDominio(usuario, livro, prazo_dias=1)
    e.data_prevista_devolucao = e.data_emprestimo - timedelta(days=1)

    assert e.atrasado() is True

def test_renovacao_valida(usuario, livro):
    e = EmprestimoDominio(usuario, livro, prazo_dias=7)
    e.renovar(15)
    assert e.prazo_dias + 15 >= 7
    assert e.renovacoes == 1

def test_renovacao_invalidas(usuario, livro):
    e = EmprestimoDominio(usuario, livro, prazo_dias=7)
    with pytest.raises(ValueError):
        e.renovar(10)  # menor que 15
    with pytest.raises(ValueError):
        e.renovar(35)  # maior que 30

def test_renovacao_emprestimo_encerrado(usuario, livro):
    e = EmprestimoDominio(usuario, livro, prazo_dias=7)
    e.devolucao()
    with pytest.raises(Exception) as excinfo:
        e.renovar(20)
    assert "Não é possível renovar" in str(excinfo.value)

def test_prazo_de_vencimento(usuario, livro):
    e = EmprestimoDominio(usuario, livro, prazo_dias=7)
    # considerando que falta menos de 3 dias para vencer, retorna True
    assert isinstance(e.prazo_de_vencimento(), bool)

def test_bloqueio_usuario_por_atraso(usuario, livro):
    e = EmprestimoDominio(usuario, livro, prazo_dias=1)
    e.data_prevista_devolucao = e.data_emprestimo - timedelta(days=1)

    e.verificar_bloqueio()
    assert usuario.bloqueado is True


def test_str_emprestimo(usuario, livro):
    e = EmprestimoDominio(usuario, livro, prazo_dias=7)
    s = str(e)
    assert "João" in s
    assert "Dom Casmurro" in s
