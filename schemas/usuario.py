from pydantic import BaseModel
from typing import Optional, List
from model.usuario import Usuario


class UsuarioSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser representado
    """
    nome: str = "John Doe"
    idade: Optional[int] = 21



class UsuarioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do usuário.
    """
    nome: str = "Teste"


class ListagemUsuariosSchema(BaseModel):
    """ Define como uma listagem de usuários será retornada.
    """
    usuarios:List[UsuarioSchema]


def apresenta_usuarios(usuarios: List[Usuario]):
    """ Retorna uma representação dos usuários seguindo o schema definido em
        UsuarioViewSchema.
    """
    result = []
    for usuario in usuarios:
        result.append({
            "nome": usuario.nome,
            "idade": usuario.idade
        })

    return {"usuarios": result}


class UsuarioViewSchema(BaseModel):
    """ Define como um usuário será retornado
    """
    id: int = 1
    nome: str = "John Doe"
    idade: Optional[int] = 21


class UsuarioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    nome: str

class UsuariosDelSchema(BaseModel):
    """Retorna a estrutura da mensagem quando todos os usuários forem deletados"""
    message: str

def apresenta_usuario(usuario: Usuario):
    """ Retorna uma representação do usuário seguindo o schema definido em
        UsuarioViewSchema.
    """
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "idade": usuario.idade,
    }
