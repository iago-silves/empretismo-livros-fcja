import pytest
from datetime import datetime, timedelta
from app.models.emprestimo import Emprestimo
from app.models.livro import Livro
from app.models.usuario import Usuario

@pytest.fixture
def usuario_padrao():
    usuario = Usuario(
        nome = "Iago Silvestre",
        email = "iago@gmail.com",
        senha = "123456"
    )
    usuario.bloqueado = False
    return usuario

@pytest.fixture
def livro_padrao():
    return Livro(
        autor="J. K. Rowling",
        titulo="Harry Potter",
        editora="Rocco",
        edicao="1ª",
        ano=1997,
        local="Estante C2",
        origem="Compra",
        observacao=""
    )

def test_criar_emprestimo_com_usuario_desbloqueado(usuario_padrao, livro_padrao):
    emprestimo = Emprestimo(
        usuario = usuario_padrao,
        livro = livro_padrao,
        prazo_dias = 7
    )

    assert emprestimo.usuario == usuario_padrao
    assert emprestimo.livro == livro_padrao
    assert emprestimo.data_devolucao is None

def test_nao_permite_emprestimo_para_usuario_bloqueado(livro_padrao):
    usuario = Usuario(
        nome = "Karcia",
        email = "karcia@gmail.com",
        senha = "123"
    )
    usuario.bloqueado = True
    with pytest.raises(Exception):
        Emprestimo(usuario, livro_padrao, prazo_dias = 7)

def test_devolucao_registra_data(usuario_padrao, livro_padrao):
    emprestimo = Emprestimo(usuario_padrao, livro_padrao, prazo_dias=7)
    emprestimo.devolucao()

    assert emprestimo.data_devolucao is not None

def test_usuario_fica_bloqueado_se_devolver_atrasado(usuario_padrao, livro_padrao):
    emprestimo = Emprestimo(usuario_padrao, livro_padrao, prazo_dias=1)

    # força atraso
    emprestimo.data_prevista_devolucao -= timedelta(days=5)
    emprestimo.devolucao()

    assert usuario_padrao.bloqueado is True

def test_renovacao_dentro_do_prazo(usuario_padrao, livro_padrao):
    emprestimo = Emprestimo(usuario_padrao, livro_padrao, prazo_dias=7)

    data_original = emprestimo.data_prevista_devolucao
    emprestimo.renovar(15)

    assert emprestimo.data_prevista_devolucao > data_original

def test_renovacao_com_prazo_invalido(usuario_padrao, livro_padrao):
    emprestimo = Emprestimo(usuario_padrao, livro_padrao, prazo_dias=7)

    with pytest.raises(ValueError):
        emprestimo.renovar(10)

def test_nao_renova_emprestimo_encerrado(usuario_padrao, livro_padrao):
    emprestimo = Emprestimo(usuario_padrao, livro_padrao, prazo_dias=7)
    emprestimo.devolucao()

    with pytest.raises(Exception):
        emprestimo.renovar(15)