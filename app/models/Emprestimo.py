from datetime import datetime, timedelta
from app.models.usuario import Usuario
from app.models.livro import Livro

class Emprestimo:
    def __init__(self, usuario: Usuario, livro: Livro, prazo_dias: int):
        if usuario.bloqueado:
            raise Exception("Usuario bloqueado, não é possível realizar outro empréstimo.")
        self.usuario = usuario
        self.livro = livro
        self.data_emprestimo = datetime.now()
        self.prazo_dias = prazo_dias 
        self.data_prevista_devolucao = self.data_emprestimo + timedelta(days=prazo_dias)
        self.data_devolucao = None
        self.renovacoes = 0
    
    def devolucao(self):
        if self.data_devolucao is not None:
            raise Exception("Este empréstimo foi encerrado.")
        
        self.data_devolucao = datetime.now()

        if self.atrasado():
            self.usuario.bloqueado = True

    def renovar(self, dias: int):
        if self.data_devolucao is not None:
            raise Exception("Não é possível renovar um emprétimo encerrado.")
        
        if dias < 15 or dias > 30:
            raise ValueError("O prazo de renovação deve ser entre 15 e 30 dias.")
        
        self.data_prevista_devolucao += timedelta(days=dias)
        self.renovacoes += 1

    def atrasado(self) -> bool:
        if self.data_devolucao is not None:
            return self.data_devolucao > self.data_prevista_devolucao
        
        return datetime.now() > self.data_prevista_devolucao
    
    def prazo_de_vencimento(self, dias: int = 3) -> bool:
        if self.data_devolucao is not None:
            return False
        
        return datetime.now() >= self.data_prevista_devolucao - timedelta(days=dias)
    
    def __str__(self):
        return (f"Livro: {self.livro.titulo} | " f"Usuário: {self.usuario.nome} | " 
                f"Devolução prevista: {self.data_prevista_devolucao.strftime('%d/%m/%Y')}") # perguntar a Karcia
    
