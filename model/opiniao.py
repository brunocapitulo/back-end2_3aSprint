from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship

from model import Base

class Opiniao(Base):
    __tablename__ = 'opiniao'

    id = Column("pk_opiniao", Integer, primary_key = True)
    nome = Column(String(130), unique = False)
    idade = Column(Integer, unique = False)
    comentario = Column(String(300), unique = False)

    def __init__(self, nome:str, idade: int, comentario: str):
        self.nome = nome
        self.idade = idade
        self.comentario = comentario

"""
nome: nome da pessoa
idade: idade da pessoa
comentario: opinião/comentário da pessoa sobre a loja
"""
