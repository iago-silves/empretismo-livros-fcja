from datetime import datetime, timedelta
from app.models.usuario import Usuario
from app.models.livro import Livro

class Emprestimo:
    def __init__(self, usuario: Usuario, livro: Livro, prazo_dias: int):
        if usuario.bloqueado:
            raise Exception("Usuario bloqueado, não é possível realizar empréstimos.")
        
        if prazo_dias < 1:
            raise ValueError("O prazo do empréstimo deve ser maior que zero.")

        self.usuario = usuario
        self.livro = livro
        self.data_emprestimo = datetime.now()
        self.prazo_dias = prazo_dias 
        self.data_prevista_devolucao = self.data_emprestimo + timedelta(days=prazo_dias)
        self.data_devolucao = None
        self.renovacoes = 0
        self.exige_presenca_fisica = False
    
    def devolucao(self):
        if self.data_devolucao is not None:
            raise Exception("Este empréstimo já foi encerrado.")
        
        self.data_devolucao = datetime.now()
        self.livro.disponivel = True

        if self.atrasado():
            self.usuario.bloqueado = True

    def renovar(self, dias: int):
        if self.data_devolucao is not None:
            raise Exception("Não é possível renovar um emprétimo encerrado.")
        
        if self.atrasado():
            raise Exception("Não é possível renovar um empréstimo em atraso.")
        
        if dias < 15 or dias > 30:
            raise ValueError("O prazo de renovação deve ser entre 15 e 30 dias.")
        
        nova_data_prevista = self.data_prevista_devolucao + timedelta(days=dias)
        prazo_total = (nova_data_prevista - self.data_emprestimo).days

        if prazo_total > 30:
            self.exige_presenca_fisica = True

        self.data_prevista_devolucao = nova_data_prevista 
        self.renovacoes += 1

    def atrasado(self) -> bool:
        if self.data_devolucao is not None:
            return self.data_devolucao > self.data_prevista_devolucao
        
        return datetime.now() > self.data_prevista_devolucao
    
    def verificar_bloqueio(self):
        if self.atrasado():
            self.usuario.bloqueado = True

    
    def prazo_de_vencimento(self, dias: int = 3) -> bool:
        if self.data_devolucao is not None:
            return False
        
        return datetime.now() >= self.data_prevista_devolucao - timedelta(days=dias)
    
    def __str__(self) -> str:
        return (f"Usuário: {self.usuario.nome} | "
                f"Título: {self.livro.titulo} | " 
                f"Autor: {self.livro.autor} | "
                f"Edição: {self.livro.edicao} | "
                f"Editora: {self.livro.editora} | "
                f"Local: {self.livro.local} | "
                f"Origem: {self.livro.origem} | "
                f"Observação: {self.livro.observacao}"
                f"Devolução prevista: {self.data_prevista_devolucao.strftime('%d/%m/%Y')}")
    
