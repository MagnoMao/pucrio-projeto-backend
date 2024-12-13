from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union

from model import Base


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    idade = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, idade:int,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Usuario

        Arguments:
            nome: nome do usuário.
            idade: idade do usuário
            data_insercao: data de quando o usuário foi inserido à base
        """
        self.nome = nome
        self.idade = idade

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
