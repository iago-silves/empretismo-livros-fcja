class Livro:
    def __init__(self, autor: str, titulo: str, editora: str, edicao: str, ano: str, origem: str, observacao: str = ""):
        self.autor = autor
        self.titulo = titulo
        self.editora = editora
        self.edicao = edicao
        self.ano = ano
        self.origem = origem
        self.observacao = observacao
    
    def __str__(self):
        return f"{self.titulo}; {self.autor} ({self.ano})"
