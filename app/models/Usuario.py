from app.models.pessoa import Pessoa

class Usuario(Pessoa):
    def __init__(self, nome, email, telefone, endereco, setor, tipo):
        self.id = None
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.setor = setor
        self.tipo = tipo
        self.bloqueado = False

