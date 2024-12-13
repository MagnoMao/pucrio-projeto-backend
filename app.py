from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Usuario, Livro
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
usuario_tag = Tag(name="Usuário", description="Adição, visualização e remoção de usuários na base")
livro_tag = Tag(name="Livro", description="Adição, visualização e remoção de livros na base")


@app.post('/usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """Adiciona um novo Usuario à base de dados

    Retorna uma representação dos usuários.
    """
    usuario = Usuario(
        nome=form.nome,
        idade=form.idade)
    #logger.debug(f"Adicionando o usuário de nome: '{usuario.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando usuário
        session.add(usuario)
        # efetivando o comando de adição de novo item na tabela
        session.commit()        
        #logger.debug(f"Adicionado usuário de nome: '{usuario.nome}'")
        return apresenta_usuario(usuario), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Usuario de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar usuário '{usuario.nome}', {error_msg}")
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar usuário '{usuario.nome}', {error_msg}")
        return {"mensagem": error_msg}, 400


@app.get('/usuarios', tags=[usuario_tag],
         responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})
def get_usuarios():
    """Faz a busca por todos os Usuarios cadastrados

    Retorna uma representação da listagem de usuários.
    """
    logger.debug(f"Coletando usuários ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuarios = session.query(Usuario).all()

    if not usuarios:
        # se não há usuarios cadastrados
        return {"usuários": "Não há usuários cadastrados"}, 200
    else:
        logger.debug(f"%d usuários encontrados" % len(usuarios))
        # retorna a representação de usuario
        print(usuarios)
        return apresenta_usuarios(usuarios), 200


@app.get('/usuario', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def get_usuario(query: UsuarioBuscaSchema):
    """Faz a busca por um Usuario a partir do nome

    Retorna uma representação dos usuários.
    """
    usuario_nome = query.nome
    logger.debug(f"Coletando dados sobre usuário #{usuario_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuario = session.query(Usuario).filter(Usuario.nome == usuario_nome).first()
    if not usuario:
        # se o usuário não foi encontrado
        error_msg = "Usuário não encontrado na base :/"
        logger.warning(f"Erro ao buscar usuário '{usuario_nome}', {error_msg}")
        return {"mensagem": error_msg}, 404
    else:
        logger.debug(f"Usuario encontrado: '{usuario.nome}'")
        # retorna a representação de usuário
        return apresenta_usuario(usuario), 200


@app.delete('/usuario', tags=[usuario_tag],
            responses={"200": UsuarioDelSchema, "404": ErrorSchema})
def del_usuario(query: UsuarioBuscaSchema):
    """Deleta um usuário a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    usuario_nome = unquote(unquote(query.nome))
    print(usuario_nome)
    logger.debug(f"Deletando dados sobre usuário #{usuario_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Usuario).filter(Usuario.nome == usuario_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado usuário #{usuario_nome}")
        return {"mensagem": "Usuário removido", "nome": usuario_nome}, 200
    else:
        # se o usuário não foi encontrado
        error_msg = "Usuario não encontrado na base :/"
        logger.warning(f"Erro ao deletar usuário #'{usuario_nome}', {error_msg}")
        return {"mensagem": error_msg}, 404

@app.delete('/usuarios', tags=[usuario_tag],
            responses={"200": UsuariosDelSchema,"400": ErrorSchema, "500": ErrorSchema})
def del_usuarios():
    """Deleta TODOS os usuários da base de dados, use com cuidado !!!"""
    session = Session()

    try:
        usuarios = session.query(Usuario)
        if(not usuarios.first()):
            logger.warning("Erro ao deletar todos os usuários, a base de usuários já está vazia")
            return {"mensagem": "A base de usuários já está vazia"}, 500
        usuarios.delete()
        session.commit()
        logger.debug("Todos os usuários foram deletados")
        return {"message": "Todos os usuários foram deletados com sucesso"}, 200
    except Exception as e:
        logger.debug("Algo deu errado")
        logger.debug(e)
        return {"mensagem": "Algo deu errado"}, 500
    

#-------------------------------------------------------------------------------------------------

@app.post('/livro', tags=[livro_tag],
          responses={"200": LivroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_livro(form: LivroSchema):
    """Adiciona um novo Livro à base de dados

    Retorna uma representação dos livros.
    """
    livro = Livro(
        nome=form.nome,
        autor=form.autor,
        editora = form.editora
        )
    logger.debug(f"Adicionando o livro de nome: '{livro.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando livro
        session.add(livro)
        # efetivando o chamando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado o livro de nome: '{livro.nome}'")
        return apresenta_livro(livro), 200        
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        error_msg = e
        logger.warning(f"Erro ao adicionar livro '{livro.nome}', {error_msg}")
        print()
        return {"mensagem": error_msg}, 400


@app.get('/livros', tags=[livro_tag],
         responses={"200": ListagemLivrosSchema, "404": ErrorSchema})
def get_livros():
    """Faz a busca por todos os Livros cadastrados

    Retorna uma representação da listagem de livros.
    """
    logger.debug(f"Coletando livros ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    livros = session.query(Livro).all()

    if not livros:
        # se não há livros cadastrados
        return {"livros": "Não há livros cadatrados"}, 200
    else:
        logger.debug(f"%d livros encontrados" % len(livros))
        # retorna a representação de livro
        return apresenta_livros(livros), 200


@app.get('/livro', tags=[livro_tag],
         responses={"200": LivroViewSchema, "404": ErrorSchema})
def get_livro(query: LivroBuscaSchema):
    """Faz a busca por livros a partir do nome

    Retorna uma representação dos livros.
    """
    livro_nome = query.nome
    logger.debug(f"Coletando dados sobre livro #{livro_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    livros = session.query(Livro).filter(Livro.nome == livro_nome).all()

    if livros:
        logger.debug(f"Livros encontrados: '{apresenta_livros(livros)}'")
        # retorna a representação de livro
        return apresenta_livros(livros), 200
    else:
        # se o livro não foi encontrado
        error_msg = "Livro não encontrado na base :/"
        logger.warning(f"Erro ao buscar livro '{livro_nome}', {error_msg}")
        return {"mensagem": error_msg}, 404
        


@app.delete('/livro', tags=[livro_tag],
            responses={"200": LivroDelSchema, "404": ErrorSchema})
def del_livro(query: LivroBuscaIdSchema):
    """Deleta um livro a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    livro_id = query.id
    # criando conexão com a base
    session = Session()
    livro = session.query(Livro).filter(Livro.id == livro_id)
    # fazendo a remoção

    if livro:
        # retorna a representação da mensagem de confirmação
        obj_livro = livro.first()
        logger.debug(f"Deletandoo livro de id#{obj_livro.id}\nnome:{obj_livro.nome}")
        livro.delete()
        session.commit()
        return {"mensagem": "Livro removido", "id": obj_livro.id ,"nome": obj_livro.nome}, 200
    else:
        # se o livro não foi encontrado
        error_msg = "Livro não encontrado na base :/"
        logger.warning(f"Erro ao deletar livro #'{livro.id}\nnome: {livro.nome}', {error_msg}")
        return {"mensagem": error_msg}, 404

@app.delete('/livros', tags=[livro_tag],
            responses={"200": LivrosDelSchema,"400": ErrorSchema, "500": ErrorSchema})
def del_livros():
    """Deleta TODOS os livros da base de dados, use com cuidado !!!"""
    session = Session()

    try:
        livros = session.query(Livro)
        if(not livros.first()):
            logger.warning("Erro ao deletar todos os livros, a base de livros já está vazia")
            return {"mensagem": "A base de livros já está vazia"}, 400
        livros.delete()
        session.commit()
        logger.debug("Todos os livros foram deletados")
        return {"message": "Todos os livros foram deletados com sucesso"}, 200
    except Exception as e:
        logger.debug("Algo deu errado")
        logger.debug(e)
        return {"mensagem": "Algo deu errado"}, 500

@app.put('/livro', tags=[livro_tag],
            responses={"200": LivroEmprestadoSchema,"404": ErrorSchema, "500": ErrorSchema})
def empresta_livro(query: LivroEmprestaSchema):
    """Empresta um livro da biblioteca a um usuário"""
    try:
        session = Session()
        livro = session.query(Livro).filter(Livro.id == query.livro_id).first()
        if(not livro): return {"mensagem": f"livro de id #{query.livro_id} não encontrado"}, 404
        
        #Essa linha acaba por garantir a integridade referencial pois a coluna emprestado_para_id é FK
        # da PK "id" de "Usuario", e não é possível inserir um id que não tenha sido encontrado na tabela "Usuario"
        usuario = session.query(Usuario).filter(Usuario.nome == query.usuario_nome).first()
        if(not usuario): return {"mensagem": f"Usuário de nome {query.usuario_nome} não encontrado"}, 404
        
        livro.emprestado_para_id = usuario.id
        session.add(livro)
        session.commit()
        str = f"O livro de id: {livro.id}, {livro.nome}, foi emprestado para {usuario.nome}"
        return {"mensagem": str}, 200
    except Exception as e:
        str = "Erro não identificado: " + e
        return {"mensagem": str}, 500

@app.put('/livroDevolve', tags=[livro_tag],
            responses={"200": LivroDevolvidoSchema,"404": ErrorSchema, "500": ErrorSchema})
def devolve_livro(query: LivroDevolveSchema):
    """Devolve um livro emprestado à biblioteca"""
    try:
        livro_id = query.id
        session = Session()
        livro = session.query(Livro).filter(Livro.id == livro_id).first()
        if(not livro): return {"mensagem": f"livro de id #{livro_id} não encontrado"}, 404
        if(livro.emprestado_para_id == None): return {"mensagem": f"livro de id #{livro_id} não estava emprestado"}, 404

        livro.emprestado_para_id = None
        session.add(livro)
        session.commit()
        str = f"O livro de id: {livro.id}, {livro.nome}, foi devolvido."
        return {"mensagem": str}, 200
    except Exception as e:
        str = "Erro não identificado: " + e
        return {"mensagem": str}, 500
    