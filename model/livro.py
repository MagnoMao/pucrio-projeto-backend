from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Livro(Base):
    __tablename__ = 'livro'

    id = Column(Integer, primary_key=True)
    
    # nome não será unique para permitir múltiplas cópias do mesmo livro
    nome = Column(String(140))
    autor = Column(String(140))
    editora = Column(String(140))
    emprestado_para_id = Column(ForeignKey("usuario.id"))

    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, autor:str, editora:str, emprestado_para_id: int = None,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Livro

        Arguments:
            nome: nome do livro.
            autor: nome do autor do livro
            editora: nome da editora do livro
            emprestado_para_id: id do usuário para quem o livro foi emprestado
            data_insercao: data de quando o livro foi inserido à base
        """
        self.nome = nome
        self.autor = autor
        self.editora = editora

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
