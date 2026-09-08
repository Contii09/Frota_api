from datetime import timedelta, datetime
from flask import Flask, jsonify, request
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from models import Policial, db_session, Viatura, Checklist_Turno, Responsavel, Itens_Manutencao, Ordem_Itens, \
    Ordem_Servico
import os
from dotenv import load_dotenv
# gera token
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from functools import wraps

load_dotenv()

app = Flask(__name__)
# definir a senha, em produção colocar em local seguro
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
jwt = JWTManager(app)

# previne gargalo "too many connections"
"""
    ### @app.teardown_appcontext (O Zelador)
    ### Para que serve: 
    Fechar conexões de banco de dados, limpar memória temporária, fechar arquivos abertos. 
    Ele evita o temido Memory Leak (Vazamento de Memória).
    ### Curiosidade: 
    Como estamos usando o Flask-SQLAlchemy, você nunca precisará escrever esse comando na mão para o banco de dados. 
    A biblioteca já injeta um teardown_appcontext invisível no seu app que faz db.session.remove() automaticamente.
    """


@app.route('/get_policiais', methods=['GET'])
def get_policiais():
    try:
        sql_p = select(Policial)
        result_policia = db_session.execute(sql_p).all()
        if not result_policia:
            return jsonify({'msg': "Valores não encontrados"}), 400
        lista_p = []
        for p in result_policia:
            lista_p.append(p.serialize())
        return jsonify(lista_p), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()


@app.route('/get_viaturas', methods=['GET'])
def get_viaturas():
    try:
        sql_v = select(Viatura)
        result_viatura = db_session.execute(sql_v).all()
        if not result_viatura:
            return jsonify({'msg': "Valores não encontrados"}), 400
        lista_p = []
        for p in result_viatura:
            lista_p.append(p.serialize())
        return jsonify(lista_p), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()


@app.route('/get_responsaveis', methods=['GET'])
def get_responsaveis():
    try:
        sql_v = select(Viatura)
        result_responsavel = db_session.execute(sql_v).all()
        if not result_responsavel:
            return jsonify({'msg': "Valores não encontrados"}), 400
        lista_p = []
        for p in result_responsavel:
            lista_p.append(p.serialize())
        return jsonify(lista_p), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()


@app.route('/get_itens', methods=['GET'])
def get_itens():
    try:
        sql_v = select(Itens_Manutencao)
        result_itens = db_session.execute(sql_v).all()
        if not result_itens:
            return jsonify({'msg': "Valores não encontrados"}), 400
        lista_p = []
        for p in result_itens:
            lista_p.append(p.serialize())
        return jsonify(lista_p), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()


@app.route('/get_checklist', methods=['GET'])
def get_checklist():
    try:
        sql_v = select(Checklist_Turno)
        result_checklist = db_session.execute(sql_v).all()
        if not result_checklist:
            return jsonify({'msg': "Valores não encontrados"}), 400
        lista_p = []
        for p in result_checklist:
            lista_p.append(p.serialize())
        return jsonify(lista_p), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()


@app.route('/get_ordem', methods=['GET'])
def get_ordem():
    try:
        sql_v = select(Ordem_Servico)
        result_ordem = db_session.execute(sql_v).all()
        if not result_ordem:
            return jsonify({'msg': "Valores não encontrados"}), 400
        lista_p = []
        for p in result_ordem:
            lista_p.append(p.serialize())
        return jsonify(lista_p), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()


@app.route('/get_ordem_itens', methods=['GET'])
def get_ordem_itens():
    try:
        sql_v = select(Ordem_Itens)
        result_ordem_itens = db_session.execute(sql_v).all()
        if not result_ordem_itens:
            return jsonify({'msg': "Valores não encontrados"}), 400
        lista_p = []
        for p in result_ordem_itens:
            lista_p.append(p.serialize())
        return jsonify(lista_p), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()


@app.route('/post_policial', methods=['POST'])
def post_policial():
    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    cargo_patente = dados.get('cargo_patente')
    matricula = dados.get('matricula')

    if not nome or not email or not senha or not cargo_patente or matricula:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:
        sql_p = select(Policial).where(Policial.email == email)
        result_policia = db_session.execute(sql_p).scalar()

        if result_policia:
            return jsonify({'msg': "Usuário já existe"}), 400

        new_p = Policial(name=nome, email=email, cargo_patente=cargo_patente, matricula=matricula)
        new_p.set_senha_hash(senha)
        db_session.add(new_p)
        db_session.commit()

        info = {
            "msg": "Usuário criado com sucesso",
            "user_id": new_p.id_policial
        }

        return jsonify(info), 201
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()


@app.route('/post_viatura', methods=['POST'])
def post_viatura():
    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    placa = dados.get('placa')
    ano = dados.get('ano')
    km_atual = dados.get('km_atual')
    prefixo = dados.get('prefixo')
    modelo = dados.get('modelo')
    status_atual = dados.get('status_atual')

    if not placa or not ano or not km_atual or not prefixo or not modelo or status_atual:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:
        sql_p = select(Viatura).where(Viatura.placa == placa)
        result_viatura = db_session.execute(sql_p).scalar()

        if result_viatura:
            return jsonify({'msg': "Usuário já existe"}), 400

        new_p = Viatura(placa=placa, ano=ano, km_atual=km_atual, prefixo=prefixo, modelo=modelo,
                        status_atual=status_atual)
        db_session.add(new_p)
        db_session.commit()

        info = {
            "msg": "Usuário criado com sucesso",
            "user_id": new_p.id_viatura
        }

        return jsonify(info), 201
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()


@app.route('/post_responsavel', methods=['POST'])
def post_responsavel():
    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    cargo_funcao = dados.get('cargo_funcao')

    if not nome or not email or not senha or cargo_funcao:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:
        sql_p = select(Responsavel).where(Responsavel.email == email)
        result_responsavel = db_session.execute(sql_p).scalar()

        if result_responsavel:
            return jsonify({'msg': "Usuário já existe"}), 400

        new_p = Responsavel(nome=nome, email=email, cargo_funcao=cargo_funcao)
        new_p.set_senha_hash(senha)
        db_session.add(new_p)
        db_session.commit()

        info = {
            "msg": "Usuário criado com sucesso",
            "user_id": new_p.id_responsavel
        }

        return jsonify(info), 201
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()



@app.route('/post_itens_manutencao', methods=['POST'])
def post_itens_manutencao():
    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    nome_item = dados.get('nome-item')
    descricao = dados.get('descricao')
    categoria_falha = dados.get('categoria_falha')
    valor_unitario = dados.get('valor_unitario')

    if not nome_item or not descricao or not categoria_falha or valor_unitario:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:
        new_p = Itens_Manutencao(nome_item=nome_item, descricao=descricao, categoria_falha=categoria_falha, valor_unitario=valor_unitario )
        db_session.add(new_p)
        db_session.add(new_p)
        db_session.commit()

        info = {
            "msg": "Usuário criado com sucesso",
            "user_id": new_p.id_item
        }

        return jsonify(info), 201
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()



@app.route('/post_checklist', methods=['POST'])
def post_checklist():
    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    viatura_id = dados.get('viatura_id')
    policial_id = dados.get('policial_id')
    nivel_oleo = dados.get('nivel_oleo')
    status_pneu = dados.get('status_pneu')
    km_abertura = dados.get('km_abertura')
    relatorio_problema = dados.get('relatorio_problema')

    if not nivel_oleo or not viatura_id or not policial_id or not status_pneu or not km_abertura or relatorio_problema:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:
        new_p = Checklist_Turno(viatura_id=viatura_id, policial_id=policial_id, nivel_oleo=nivel_oleo, status_pneu=status_pneu, km_abertura=km_abertura, relatorio_problema=relatorio_problema)
        db_session.add(new_p)
        db_session.commit()

        info = {
            "msg": "Usuário criado com sucesso",
            "user_id": new_p.id_checklist
        }

        return jsonify(info), 201
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()



@app.route('/post_ordem_servico', methods=['POST'])
def post_ordem_servico():
    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    viatura_id = dados.get('viatura_id')
    responsavel_id = dados.get('responsavel_id')
    data_abertura = dados.get('data_abertura')
    tipo_manutencao = dados.get('tipo_manutencao')
    status_os = dados.get('status_os')
    custo_total = dados.get('curso_total')

    if not viatura_id or not responsavel_id or not data_abertura or not tipo_manutencao or not status_os or custo_total:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:
        new_p = Ordem_Servico(viatura_id=viatura_id, responsavel_id=responsavel_id, data_abertura=data_abertura, tipo_manutencao=tipo_manutencao, status_os=status_os, custo_total=custo_total)
        db_session.add(new_p)
        db_session.commit()

        info = {
            "msg": "Usuário criado com sucesso",
            "user_id": new_p.id_ordem
        }

        return jsonify(info), 201
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()


@app.route('/post_ordem_itens', methods=['POST'])
def post_ordem_itens():
    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    os_id = dados.get('os_id')
    item_id = dados.get('item_id')

    if not os_id or item_id:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:

        new_p = Ordem_Itens(os_id, item_id)
        db_session.add(new_p)
        db_session.commit()

        info = {
            "msg": "Usuário criado com sucesso",
            "user_id": new_p.id_lista
        }

        return jsonify(info), 201
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()




