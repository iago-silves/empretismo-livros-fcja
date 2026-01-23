from app.infra.database import engine, metadata

from app.infra.tables.adm_table import administradores_table
from app.infra.tables.usuario_table import usuarios_table
from app.infra.tables.livro_table import livros_table
from app.infra.tables.emprestimo_table import emprestimos_table

def criar_tabelas():
    metadata.create_all(engine)
    print("Tabelas criadas com sucesso")

if __name__ == "__main__":
    criar_tabelas()
