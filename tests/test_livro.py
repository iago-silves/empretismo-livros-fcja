import pytest
from app.models.livro import Livro

def test_criar_livro():
    livro = Livro(
        autor = "Machado de Assis",
        titulo = "Dom Casmurro",
        editora = "Editora Exemplo",
        edicao = "1ª",
        ano = 1899,
        local = "Prateleira A3",
        origem = "Doação",
        observacao = "Clássico da literatura"
    )

    assert livro.autor == "Machado de Assis"
    assert livro.titulo == "Dom Casmurro"
    assert livro.editora == "Editora Exemplo"
    assert livro.edicao == "1ª"
    assert livro.ano == 1899
    assert livro.local == "Prateleira A3"
    assert livro.origem == "Doação"
    assert livro.observacao == "Clássico da literatura"
    
def test_str_livro():
    livro = Livro(
        autor="Edu",
        titulo="Olhos Negros",
        editora="Editora Exemplo",
        edicao="2ª",
        ano=2029,
        local="Caixa A5",
        origem="Compra",
        observacao=""
    )

    resultado = str(livro)

    assert "Olhos Negros" in resultado
