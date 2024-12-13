from pydantic import BaseModel
from typing import Optional, List
from model.livro import Livro
from model.usuario import Usuario
from model import Session


class LivroSchema(BaseModel):
    """ Define como um novo livro a ser inserido deve ser representado
    """
    nome: str = "O Senhor dos Anéis"
    autor: str = "J.R.R.TOLKIEN"
    editora: str = "Martins Fontes"



class LivroBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do livro.
    """
    nome: str = "Teste"

class LivroBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do livro.
    """
    id: int = 1


class ListagemLivrosSchema(BaseModel):
    """ Define como uma listagem de livros será retornada.
    """
    livros:List[LivroSchema]

class LivroViewSchema(BaseModel):
    """ Define como um livro será retornado
    """
    id: int = 1
    nome: str = "O Senhor dos anéis"
    autor: str = "J.R.R.Tolkien"
    editora: str = "Martins Fontes"
    emprestado_para: str


class LivroDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    nome: str

class LivrosDelSchema(BaseModel):
    """Retorna a estrutura da mensagem quando todos os livros forem deletados"""
    message: str

class LivroEmprestadoSchema(BaseModel):
    """Retorna a estrutura da mensagem quando um livro for emprestado"""
    message: str

class LivroEmprestaSchema(BaseModel):
    """Define a estrutura para emprestar um livro"""
    livro_id: int = 1
    usuario_nome: str = "John Doe"

class LivroDevolvidoSchema(BaseModel):
    """Retorna a estrutura da mensagem quando um livro for devolvido"""

class LivroDevolveSchema(BaseModel):
    """Define a estrutura para devolver um livro"""
    id: int = 1

def emprestado_usuario_id_para_nome(usuario_id: int):    
    """ Converte o id associado a um usuário para o nome dele
    """
    session = Session()
    emprestado_nome = None
    # Se o livro está emprestado para alguém, busca o nome relacionado a esse ID
    if usuario_id : emprestado_nome = session.query(Usuario).filter(Usuario.id == usuario_id).first().nome
    return emprestado_nome

def apresenta_livro(livro: Livro):
    """ Retorna uma representação do livro seguindo o schema definido em
        LivroViewSchema.
    """    
    return {
        "id": livro.id,
        "nome": livro.nome, 
        "autor": livro.autor,
        "editora": livro.editora,
        "emprestado_para": emprestado_usuario_id_para_nome(livro.emprestado_para_id)
    }

def apresenta_livros(livros: List[Livro]):
    """ Retorna uma representação dos livros seguindo o schema definido em
        LivroViewSchema.
    """    
    result = []
    for livro in livros:   
        result.append({
            "id": livro.id,
            "nome": livro.nome,
            "autor": livro.autor,
            "editora": livro.editora,
            "emprestado_para": emprestado_usuario_id_para_nome(livro.emprestado_para_id)
        })

    return {"livros": result}


