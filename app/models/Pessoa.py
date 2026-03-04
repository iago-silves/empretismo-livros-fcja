from abc import ABC, abstractmethod

class Pessoa(ABC):
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email

    
