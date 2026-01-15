class Livro:
    def __init__(self, autor: str, titulo: str, editora: str, edicao: str, ano: int, origem: str, observacao: str = ""):
        self.autor = autor
        self.titulo = titulo
        self.editora = editora
        self.edicao = edicao
        self.ano = ano
        self.origem = origem
        self.observacao = observacao
        self.disponivel = True
    
    def __str__(self):
        return f"{self.titulo}; {self.autor} ({self.ano})" # perguntar à orientadora Karcia qual formato de saída desejado.
