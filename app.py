from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError

from model import Session, Opiniao
from schemas.error import ErrorSchema
from schemas.opiniao import OpiniaoSchema, OpiniaoBuscaSchema, ListagemOpiniaoSchema, OpiniaoDelSchema, OpiniaoViewSchema, apresenta_opiniao
from logger import logger

info = Info(title = 'Opiniao de clientes API', version = "1.0.0")
app = OpenAPI(__name__, info = info)
CORS(app)

#agora vamos definir as tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
opiniao_tag = Tag(name = "Adiciona pessoa", description = "Adiciona, visualiza e deleta o comentario de uma pessoa")



@app.get('/', tags = [home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do tipo de documentação
    """
    return redirect('/openapi')



@app.post('/opiniao', tags = [opiniao_tag],
          responses = {"200": OpiniaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_opiniao(form: OpiniaoSchema):
    """Adiciona uma nova pessoa à base de dados

    Retorna uma representação dos comentarios
    """
    opiniao = Opiniao(
        nome = form.nome,
        comentario = form.comentario,
        idade = form.idade)
    logger.debug(f"Adicionando comentario: '{opiniao.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando pesquisa
        session.add(opiniao)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado nome: '{opiniao.nome}'")
        return apresenta_opiniao(opiniao), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Pesquisa de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar pessoa '{opiniao.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar pesquisa '{opiniao.nome}', {error_msg}")
        return {"message": error_msg}, 400
    


@app.get('/opinioes', tags = [opiniao_tag],
         responses = {"200": ListagemOpiniaoSchema, "404": ErrorSchema})
def get_opiniao():
    """Faz a busca por todos os comentarios

    Retorna uma representação da listagem de comentarios
    """
    logger.debug(f"Coletando comentarios")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    opinioes = session.query(Opiniao).all()

    if not opinioes:
        # se não há cadastros
        return {"comentarios": []}, 200
    else:
        logger.debug(f"%d cadastros encontradas" % len(opinioes))
        # retorna a representação de pesquisa
        print(opinioes)
        return apresenta_opiniao(opinioes), 200
    


@app.delete('/opiniao', tags = [opiniao_tag],
            responses = {"200": OpiniaoDelSchema, "404": ErrorSchema})
def del_opiniao(query: OpiniaoBuscaSchema):
    """Deleta um comentario a partir do nome da pessoa informado

    Retorna uma mensagem de confirmação da remoção.
    """
    opiniao_nome = unquote(unquote(query.nome))
    logger.debug(f"Deletando dados sobre cadastro #{opiniao_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Opiniao).filter(Opiniao.nome == opiniao_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado comentario #{opiniao_nome}")
        return {"mesage": "Comentario removido", "id": opiniao_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Comentario não encontrada na base :/"
        logger.warning(f"Erro ao deletar comentario #'{opiniao_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    


@app.put('/opiniao/<string:opiniao_nome>', tags=[opiniao_tag],
         responses={"200": OpiniaoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_opiniao(opiniao_nome: str):
    """Atualiza um comentario existente pelo nome da pessoa

    Retorna uma representação do comentario atualizado.
    """
   
    session = Session()
    opiniao = session.query(Opiniao).filter(Opiniao.nome == opiniao_nome).first()

    if not opiniao:
        
        error_msg = "Comentario não encontrado na base :/"
        logger.warning(f"Comentario não encontrado para atualização: {opiniao_nome}, {error_msg}")
        return {"message": error_msg}, 404

    
    data = request.get_json()
    if "nome" in data:
        opiniao.nome = data["nome"]
    if "email" in data:
        opiniao.email = data["email"]
    if "idade" in data:
        opiniao.idade = data["idade"]

    try:
        
        session.commit()
        logger.debug(f"Comentario atualizado com sucesso: {opiniao_nome}")
        return apresenta_opiniao(opiniao), 200

    except Exception as e:
        
        error_msg = "Não foi possível atualizar o comentario :/"
        logger.warning(f"Erro ao atualizar comentario: {opiniao_nome}, {error_msg}")
        return {"message": error_msg}, 400

