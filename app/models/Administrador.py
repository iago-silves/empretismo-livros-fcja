from werkzeug.security import generate_password_hash, check_password_hash
from pessoa import Pessoa

class Administrador(Pessoa):
    def __init__(self, nome: str, email: str, senha: str):
        super().__init__(nome, email)
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

    def tipo(self):
        return "administrador"
