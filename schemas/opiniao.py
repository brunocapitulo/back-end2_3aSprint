from pydantic import BaseModel
from typing import Optional, List

from model.opiniao import Opiniao

class OpiniaoSchema(BaseModel):
    """ Define as variváveis de uma tarefa
    """
    nome: str
    idade: int
    comentario: str

class OpiniaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da pessoa
    """
    nome: str = "Bruno de Souza"

class ListagemOpiniaoSchema(BaseModel):
    """ Define como uma listagem de comentários será retornada.
    """
    produtos:List[OpiniaoSchema]

def apresenta_opiniao(opinioes: List[Opiniao]):
    """ Retorna uma representação do comentário
    """
    result = []
    for opiniao in opinioes:
        result.append({
            "nome": opiniao.nome,
            "comentario": opiniao.comentario,
            "idade": opiniao.idade,
        })

    return {"opinioes": result}

class OpiniaoViewSchema(BaseModel):
    """ Define como um comentário será retornado
    """
    id: int = 1
    nome: str = "Bruno de Souza"
    comentario: str = "Estou adorando a plataforma nova da loja!"
    idade: int = 25

class OpiniaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str