from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.pessoa import Pessoa

class Administrador(Pessoa):
    def __init__(self, nome, email, senha_hash, criado_em=None, ultimo_login=None):
        self.id = None
        super().__init__(nome, email)
        self.senha_hash = senha_hash
        self.ativo = True
        self.criado_em = criado_em or datetime.utcnow()
        self.ultimo_login = ultimo_login

    @classmethod
    def criar(cls, nome, email, senha):
        senha_hash = generate_password_hash(senha)
        return cls(nome, email, senha_hash)

    def verificar_senha(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

    def registrar_login(self):
        self.ultimo_login = datetime.utcnow()

    def desativar(self):
        self.ativo = False

    def ativar(self):
        self.ativo = True

    @property
    def tipo(self):
        return "administrador"
