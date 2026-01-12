from pessoa import Pessoa

class Usuario(Pessoa):
    def __init__(self, nome: str, email: str, telefone: str, endereco: str):
        super().__init__(nome, email)
        self.telefone = telefone
        self.endereco = endereco
        self.bloqueado = False

    def tipo(self):
        return "usuario"
