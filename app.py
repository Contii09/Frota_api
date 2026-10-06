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
import random


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

def gerar_codigo(tipo='nenhum', contagem=0):
    lista_codigo = []
    lista=["1","2","3","4","5","6","7","8","9","0"]
    for i in range(contagem):
        lista_codigo.append(random.choice(lista))
    variavel = "".join(lista_codigo)
    if tipo.upper() == 'NENHUM':
        return 'error'
    elif tipo.upper() == 'PM':
        return "PM-"+variavel
    elif tipo.upper() == 'VTR':
        return "VTR-"+variavel


@app.route('/get_policiais', methods=['GET'])
def get_policiais():
    """
      **API para Consulta de Policiais**

      ### Endpoint:
      GET /get_policiais

      ### Parametros de Entrada:
      Não possui parâmetros de entrada.

      ### Respostas (JSON):
      * **200 OK:** Lista de policiais retornada com sucesso.
        ```json
        [
            {
                "id_policial": 1,
                "nome": "string",
                "email": "string",
                "senha": "string",
                "cargo_patente": "string",
                "matricula": "string"
            }
        ]
        ```
    """
    db = db_session()
    try:
        sql_p = select(Policial)
        result_policia = db.execute(sql_p).scalars()
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
    """
      **API para Consulta de Viaturas**

      ### Endpoint:
      GET /get_viaturas

      ### Parametros de Entrada:
      Não possui parâmetros de entrada.

      ### Respostas (JSON):
      * **200 OK:** Lista de policiais retornada com sucesso.
        ```json
        [
            {
                "id_viatura": 1,
                "placa": string,
                "ano": self.ano,
                "km_atual": string,
                "prefixo": string,
                "modelo": string,
                "status_atual": string,
            }
        ]
        ```
    """
    try:
        sql_v = select(Viatura)
        result_viatura = db_session.execute(sql_v).scalars()
        lista_v = []
        for v in result_viatura:
            lista_v.append(v.serialize())
        return jsonify(lista_v), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()

@app.route('/get_responsaveis', methods=['GET'])
def get_responsaveis():
    """
      **API para Consulta de Responsaveis**

      ### Endpoint:
      GET /get_responssveis

      ### Parametros de Entrada:
      Não possui parâmetros de entrada.

      ### Respostas (JSON):
      * **200 OK:** Lista de responsaveis retornada com sucesso.
        ```json
        [
            {
                "id_responsavel": 1,
                "nome": "string",
                "email": "string",
                "senha": "string",
                "cargo_funcao": "string",
            }
        ]
        ```
    """
    try:
        sql_r = select(Responsavel)
        result_responsavel = db_session.execute(sql_r).scalars()
        lista_r = []
        for r in result_responsavel:
            lista_r.append(r.serialize())
        return jsonify(lista_r), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()

@app.route('/get_itens', methods=['GET'])
def get_itens():
    """
      **API para Consulta de Itens**

      ### Endpoint:
      GET /get_itens

      ### Parametros de Entrada:
      Não possui parâmetros de entrada.

      ### Respostas (JSON):
      * **200 OK:** Lista de itens retornada com sucesso.
        ```json
        [
            {
                "id_item": 1,
                "nome_item": "string",
                "descricao": "string",
                "categoria_falha": "string",
                "valor_unitario": "string"
            }
        ]
        ```
    """
    try:
        sql_i = select(Itens_Manutencao)
        result_itens = db_session.execute(sql_i).scalars()
        lista_i = []
        print('result_flamingo',result_itens)
        for i in result_itens:
            print(i.serialize())
            lista_i.append(i.serialize())
        return jsonify(lista_i), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()

@app.route('/get_checklist', methods=['GET'])
def get_checklist():
    """
      **API para Consulta de Checklist**

      ### Endpoint:
      GET /get_checklist

      ### Parametros de Entrada:
      Não possui parâmetros de entrada.

      ### Respostas (JSON):
      * **200 OK:** Lista de checklist retornada com sucesso.
        ```json
        [
            {
                "id_checklist": 1,
                "viatura_id": "integre",
                "policial_id": "integre",
                "data_hora": "string",
                "nivel_oleo": "string",
                "status_pneu": "string",
                "km_abertura": "string",
                "relatorio_problema": "string",
            }
        ]
        ```
    """
    try:
        checklist_banco = select(Checklist_Turno)
        result_checklist = db_session.execute(checklist_banco).scalars().all()
        lista_c = []
        if not result_checklist:
            print(result_checklist)
            return jsonify({"msg": "Error"}), 400
        print('flamingo',result_checklist)
        for c in result_checklist:
            lista_c.append(c.serialize())
        return jsonify(lista_c), 200
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()

@app.route('/get_ordem', methods=['GET'])
def get_ordem():
    """
      **API para Consulta de Ordem**

      ### Endpoint:
      GET /get_ordem

      ### Parametros de Entrada:
      Não possui parâmetros de entrada.

      ### Respostas (JSON):
      * **200 OK:** Lista de ordens retornada com sucesso.
        ```json
        [
            {
                "id_ordem": 1,
                "viatura_id": "string",
                "responsavel_id": "string",
                "data_abertura": "string",
                "data_fechamento": "string",
                "tipo_manutencao": "string",
                "status_os": "string",
                "custo_total": "string",
            }
        ]
        ```
    """
    try:
        sql_o = select(Ordem_Servico)
        result_ordem = db_session.execute(sql_o).scalars()
        lista_o = []
        for o in result_ordem:
            lista_o.append(o.serialize())
        return jsonify(lista_o), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()

@app.route('/get_ordem_itens', methods=['GET'])
def get_ordem_itens():
    """
      **API para Consulta de Ordem de Itens**

      ### Endpoint:
      GET /get_ordem_itens

      ### Parametros de Entrada:
      Não possui parâmetros de entrada.

      ### Respostas (JSON):
      * **200 OK:** Lista de ordens de itens retornada com sucesso.
        ```json
        [
            {
                "id_lista": 1,
                "os_id": "string",
                "item_id": "string",
            }
        ]
        ```
    """
    try:
        sql_oi = select(Ordem_Itens)
        result_ordem_itens = db_session.execute(sql_oi).scalars()
        lista_oi = []
        for oi in result_ordem_itens:
            lista_oi.append(oi.serialize())
        return jsonify(lista_oi), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()





@app.route('/post_policial', methods=['POST'])
def post_policial():
    """
        **API para Cadastro de Policial**

        ### Endpoint:
        POST /post_policial

        ### Parâmetros de Entrada (JSON):
        ```json
        {
            "nome": "string (obrigatorio) - Nome do policial",
            "email": "string (obrigatorio) - Endereço de e-mail do policial",
            "senha": "string (obrigatorio) - Senha para acesso ao sistema",
            "cargo_patente": "string (obrigatorio) - Cargo de acesso do policial"
        }
        ```

        ### Respostas (JSON):
        * **200 Created:** Policial registrada com sucesso.
          ```json
          {
              "msg": "Policial criado com sucesso",
              "id": policial.id_policial
          }
          ```
        * **400 Bad Request:** Ausencia de campos obrigatorios ou policial ja cadastrada.
          ```json
          {
              "msg": "Valor não Encontrado"
          }
          ```
        * **500 Internal Server Error:** Falha operacional no banco de dados.
          ```json
          {
              "msg": "[Descricao do Erro]"
          }
          ```
        """
    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    cargo_patente = dados.get('cargo_patente')
    matricula = gerar_codigo('pm',5)

    if not nome or not email or not senha or not cargo_patente or not matricula:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:
        sql_p = select(Policial).where(Policial.email == email)
        result_policia = db_session.execute(sql_p).scalar()

        if result_policia:
            return jsonify({'msg': "Este policial já existe"}), 400

        new_p = Policial(nome=nome, email=email, cargo_patente=cargo_patente, matricula=matricula)
        new_p.set_senha_hash(senha)
        db_session.add(new_p)
        db_session.commit()

        info = {
            "msg": "Policial criado com sucesso",
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
    """
        **API para Cadastro de Viaturas**

        ### Endpoint:
        POST /post_viatura

        ### Parâmetros de Entrada (JSON):
        ```json
        {
            "placa": "string (obrigatorio) - Placa identificadora da viatura",
            "ano": "integer/string (obrigatorio) - Ano de fabricação do veículo",
            "km_atual": "number (obrigatorio) - Quilometragem atual da viatura",
            "modelo": "string (obrigatorio) - Modelo do veículo",
            "status_atual": "string (opcional) - Status de operação da viatura"
        }
        ```

        ### Respostas (JSON):
        * **200 Created:** Policial registrada com sucesso.
          ```json
          {
            "msg": "Viatura criado com sucesso",
            "user_id": new_v.id_viatura
          }
          ```
        * **400 Bad Request:** Ausencia de campos obrigatorios ou policial ja cadastrada.
          ```json
          {
               "msg": "Dados não encontrados"
          }
          ```
        * **500 Internal Server Error:** Falha operacional no banco de dados.
          ```json
          {
               "msg": "[Descricao do Erro]"
          }
          ```
        """
    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    placa = dados.get('placa')
    ano = dados.get('ano')
    km_atual = dados.get('km_atual')
    prefixo = gerar_codigo('vtr',4)
    modelo = dados.get('modelo')
    status_atual = dados.get('status_atual')

    if not placa or not ano or not km_atual or not prefixo or not modelo:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:
        sql_p = select(Viatura).where(Viatura.placa == placa)
        result_viatura = db_session.execute(sql_p).scalar()

        if result_viatura:
            return jsonify({'msg': "Esta viatura já existe"}), 400

        new_v = Viatura(placa=placa, ano=ano, km_atual=km_atual, prefixo=prefixo, modelo=modelo,
                        status_atual=status_atual)
        db_session.add(new_v)
        db_session.commit()

        info = {
            "msg": "Viatura criado com sucesso",
            "user_id": new_v.id_viatura
        }

        return jsonify(info), 201
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()

@app.route('/post_responsavel', methods=['POST'])
def post_responsavel():
    """
        **API para Cadastro de Responsavel**

        ### Endpoint:
        POST /post_policial

        ### Parâmetros de Entrada (JSON):
        ```json
        {
             "nome": "string (obrigatorio) - Nome do responsável",
            "email": "string (obrigatorio) - Endereço de e-mail do responsável",
            "senha": "string (obrigatorio) - Senha para acesso ao sistema",
            "cargo_funcao": "string (obrigatorio) - Cargo ou função do responsável"
        }
        ```

        ### Respostas (JSON):
        * **200 Created:** Responsavel registrada com sucesso.
          ```json
          {
              "msg": "Responsavel criado com sucesso",
              "user_id": new_p.id_responsavel
          }
          ```
        * **400 Bad Request:** Ausencia de campos obrigatorios ou responsavel ja cadastrada.
          ```json
          {
              "msg": "Valor não Encontrado"
          }
          ```
        * **500 Internal Server Error:** Falha operacional no banco de dados.
          ```json
          {
              "msg": "[Descricao do Erro]"
          }
          ```
        """

    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    cargo_funcao = dados.get('cargo_funcao')

    if not nome or not email or not senha or not cargo_funcao:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:
        sql_p = select(Responsavel).where(Responsavel.email == email)
        result_responsavel = db_session.execute(sql_p).scalar()

        if result_responsavel:
            return jsonify({'msg': "Este responsavel já existe"}), 400

        new_p = Responsavel(nome=nome, email=email, cargo_funcao=cargo_funcao)
        new_p.set_senha_hash(senha)
        db_session.add(new_p)
        db_session.commit()

        info = {
            "msg": "Responsavel criado com sucesso",
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
    """
        **API para Cadastro de Itens de Manutençao**

        ### Endpoint:
        POST /post_itens_manutencao

        ### Parâmetros de Entrada (JSON):
        ```json
        {
            "nome_item": "string (obrigatorio) - Nome do item de manutenção",
            "descricao": "string (obrigatorio) - Descrição detalhada do item",
            "categoria_falha": "string (obrigatorio) - Categoria da falha associada",
            "valor_unitario": "number (obrigatorio) - Valor unitário do item"
        }
        ```

        ### Respostas (JSON):
        * **200 Created:** Itens de manutenção registrado com sucesso.
          ```json
          {
               "msg": "Item de manutenção criado com sucesso",
                "user_id": new_p.id_item
          }
          ```
        * **400 Bad Request:** Ausencia de campos obrigatorios ou itens ja cadastrada.
          ```json
          {
              "msg": "Valor não Encontrado"
          }
          ```
        * **500 Internal Server Error:** Falha operacional no banco de dados.
          ```json
          {
              "msg": "[Descricao do Erro]"
          }
          ```
        """
    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    nome_item = dados.get('nome_item')
    descricao = dados.get('descricao')
    categoria_falha = dados.get('categoria_falha')
    valor_unitario = dados.get('valor_unitario')

    if not nome_item or not descricao or not categoria_falha or not valor_unitario:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:
        new_p = Itens_Manutencao(nome_item=nome_item, descricao=descricao, categoria_falha=categoria_falha, valor_unitario=valor_unitario )
        db_session.add(new_p)
        db_session.commit()
        info = {
            "msg": "Item de manutenção criado com sucesso",
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
    """
        **API para Cadastro de Checklists**

        ### Endpoint:
        POST /post_checklist

        ### Parâmetros de Entrada (JSON):
        ```json
        {
            "viatura_id": "integer (obrigatorio) - ID identificador da viatura",
            "policial_id": "integer (obrigatorio) - ID identificador do policial",
            "nivel_oleo": "string (obrigatorio) - Estado ou nível do óleo do motor",
            "status_pneu": "string (obrigatorio) - Estado de conservação dos pneus",
            "km_abertura": "number (obrigatorio) - Quilometragem no momento da abertura do turno",
            "relatorio_problema": "string (obrigatorio) - Relato descritivo de problemas encontrados
        }
        ```

        ### Respostas (JSON):
        * **200 Created:** Checklist registrada com sucesso.
          ```json
          {
            "msg": "Checklist criado com sucesso",
            "user_id": new_p.id_checklist
          }
          ```
        * **400 Bad Request:** Ausencia de campos obrigatorios ou checklist ja cadastrada.
          ```json
          {
              "msg": "Valor não Encontrado"
          }
          ```
        * **500 Internal Server Error:** Falha operacional no banco de dados.
          ```json
          {
              "msg": "[Descricao do Erro]"
          }
          ```
        """
    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    viatura_id = dados.get('viatura_id')
    policial_id = dados.get('policial_id')
    nivel_oleo = dados.get('nivel_oleo')
    status_pneu = dados.get('status_pneu')
    km_abertura = dados.get('km_abertura')
    relatorio_problema = dados.get('relatorio_problema')

    if not nivel_oleo or not viatura_id or not policial_id or not status_pneu or not km_abertura or not relatorio_problema:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:
        new_p = Checklist_Turno(viatura_id=viatura_id, policial_id=policial_id, nivel_oleo=nivel_oleo, status_pneu=status_pneu, km_abertura=km_abertura, relatorio_problema=relatorio_problema)
        db_session.add(new_p)
        db_session.commit()

        info = {
            "msg": "Checklist criado com sucesso",
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
    """
        **API para Cadastro de Ordem de Serviço**

        ### Endpoint:
        POST /post_ordem_servico

        ### Parâmetros de Entrada (JSON):
        ```json
        {
            "viatura_id": "integer (obrigatorio) - ID identificador da viatura",
            "responsavel_id": "integer (obrigatorio) - ID identificador do responsável",
            "tipo_manutencao": "string (obrigatorio) - Tipo de manutenção (ex: Preventiva, Corretiva)",
            "status_os": "string (obrigatorio) - Status inicial da ordem de serviço",
            "custo_total": "number (obrigatorio) - Custo total estimado ou inicial do serviço"
        }
        ```

        ### Respostas (JSON):
        * **200 Created:** Ordem registrada com sucesso.
          ```json
          {
               "msg": "Ordem de serviço criado com sucesso",
                "user_id": new_p.id_ordem
          }
          ```
        * **400 Bad Request:** Ausencia de campos obrigatorios ou Ordem ja cadastrada.
          ```json
          {
              "msg": "Valor não Encontrado"
          }
          ```
        * **500 Internal Server Error:** Falha operacional no banco de dados.
          ```json
          {
              "msg": "[Descricao do Erro]"
          }
          ```
        """
    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    viatura_id = dados.get('viatura_id')
    responsavel_id = dados.get('responsavel_id')
    tipo_manutencao = dados.get('tipo_manutencao')
    status_os = dados.get('status_os')
    custo_total = dados.get('custo_total')

    if not viatura_id or not responsavel_id or not  tipo_manutencao or not status_os or not custo_total:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:
        new_p = Ordem_Servico(viatura_id=viatura_id, responsavel_id=responsavel_id, tipo_manutencao=tipo_manutencao, status_os=status_os, custo_total=custo_total)
        db_session.add(new_p)
        db_session.commit()

        info = {
            "msg": "Ordem de serviço criado com sucesso",
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
    """
        **API para Cadastro de Policial**

        ### Endpoint:
        POST /post_policial

        ### Parâmetros de Entrada (JSON):
        ```json
        {
            "os_id": "integer (obrigatorio) - ID da ordem de serviço",
            "item_id": "integer (obrigatorio) - ID do item de manutenção"
        }
        ```

        ### Respostas (JSON):
        * **200 Created:** Ordem registrada com sucesso.
          ```json
          {
            "msg": "Ordem de itens criado com sucesso",
            "user_id": new_p.id_lista
          }
          ```
        * **400 Bad Request:** Ausencia de campos obrigatorios ou policial ja cadastrada.
          ```json
          {
              "msg": "Valor não Encontrado"
          }
          ```
        * **500 Internal Server Error:** Falha operacional no banco de dados.
          ```json
          {
              "msg": "[Descricao do Erro]"
          }
          ```
        """
    dados = request.get_json()
    if not dados:
        return jsonify({'msg': "Dados não encontrados"}), 400
    os_id = dados.get('os_id')
    item_id = dados.get('item_id')

    if not os_id or not item_id:
        return jsonify({'msg': "Credenciais invalidas"}), 400

    try:

        new_p = Ordem_Itens(os_id=os_id, item_id=item_id)
        db_session.add(new_p)
        db_session.commit()

        info = {
            "msg": "Ordem de itens criado com sucesso",
            "user_id": new_p.id_lista
        }

        return jsonify(info), 201
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.remove()





@app.route('/put_policial/<var_id>', methods=['PUT'])
def put_policial(var_id):
    """
    **API para Atualização de Dados do Policial**

    ### Endpoint:
    PUT /put_policial/{var_id}

    ### Parâmetros de Path:
    * `var_id`: inteiro (obrigatório) - Identificador único do policial que será atualizado.

    ### Parâmetros de Entrada (JSON):
    ```json
    {
        "nome": "string (obrigatório) - Nome atualizado do policial",
        "email": "string (obrigatório) - Novo endereço de e-mail do policial",
        "senha": "string (obrigatório) - Nova senha para acesso ao sistema",
        "cargo_patente": "string (obrigatório) - Novo cargo ou patente do policial",
        "matricula": "string/inteiro (obrigatório) - Número de matrícula do policial"
    }
    ```

    ### Respostas (JSON):
    * **200 OK:** Dados do policial atualizados com sucesso.
      ```json
      {
          "msg": "Policial updated successfully",
          "id": [id_do_policial]
      }
      ```
    * **400 Bad Request:** Policial não encontrado no sistema ou ausência de campos obrigatórios no JSON enviado.
      ```json
      {
          "msg": "Policial não encontrado"
      }
      ```
      *ou se faltarem dados:*
      ```json
      {
          "msg": "Campos obrigatórios ausentes"
      }
      ```
    * **500 Internal Server Error:** Falha operacional no banco de dados.
      ```json
      {
          "msg": "[Descrição do Erro]"
      }
      ```
    """
    editar = select(Policial).where(Policial.id_policial == int(var_id))
    result = db_session.execute(editar).scalar_one_or_none()

    if not result:
        return jsonify({"msg": "Policial não encontrado"}), 400

    if request.method == 'PUT':
        dados = request.get_json()
        nome = dados.get('nome')
        email = dados.get('email')
        senha = dados.get('senha')
        cargo_patente = dados.get('cargo_patente')
        matricula = dados.get('matricula')


        if not nome or not email or not senha or not matricula or not cargo_patente:
            return jsonify({'msg': "Credenciais invalidas"}), 400

        try:
            result.nome = nome
            result.email = email
            result.senha = senha
            result.cargo_patente = cargo_patente
            result.matricula = matricula
            db_session.commit()
            return jsonify({"msg": "Policial atualizado com sucesso!"}), 200

        except Exception as e:
            db_session.rollback()
            print(f'Error: {e}')
            return jsonify({'msg': str(e)}), 500
        finally:
            db_session.close()

@app.route('/put_viatura/<var_id>', methods=['PUT'])
def put_viatura(var_id):
    '''
        **API para Atualização de Dados da Viatura**

    ### Endpoint:
    PUT /put_viatura/{var_id}

    ### Parâmetros de Path:
    * `var_id`: inteiro (obrigatório) - Identificador único da viatura que será atualizada.

    ### Parâmetros de Entrada (JSON):
    ```json
    {
        "placa": "string (obrigatório) - Placa atualizada da viatura",
        "ano": "inteiro/string (obrigatório) - Ano de fabricação ou modelo",
        "km_atual": "inteiro/float (obrigatório) - Quilometragem atualizada do veículo",
        "prefixo": "string (obrigatório) - Prefixo de identificação da viatura",
        "modelo": "string (obrigatório) - Modelo do veículo",
        "status_atual": "string (obrigatório) - Estado atual da viatura (ex: ativa, manutenção)"
    }
    ```

    ### Respostas (JSON):
    * **200 OK:** Dados da viatura atualizados com sucesso.
      ```json
      {
          "msg": "Viatura atualizado com sucesso!"
      }
      ```
    * **400 Bad Request:** Viatura não encontrada ou ausência de campos obrigatórios no JSON enviado.
      ```json
      {
          "msg": "Viatura não encontrado"
      }
      ```
      *ou se faltarem dados (validação de credenciais):*
      ```json
      {
          "msg": "Credenciais invalidas"
      }
      ```
    * **500 Internal Server Error:** Falha operacional ou erro ao tentar salvar no banco de dados.
      ```json
      {
          "msg": "[Descrição do Erro Técnico]"
      }
      ```
    '''
    editar = select(Viatura).where(Viatura.id_viatura == int(var_id))
    result = db_session.execute(editar).scalar_one_or_none()

    if not result:
        return jsonify({"msg": "Viatura não encontrado"}), 400

    if request.method == 'PUT':
        dados = request.get_json()
        placa = dados.get('placa')
        ano = dados.get('ano')
        km_atual = dados.get('km_atual')
        prefixo = dados.get('prefixo')
        modelo = dados.get('modelo')
        status_atual = dados.get('status_atual')

        if not placa or not ano or not km_atual or not prefixo or not modelo or not status_atual:
            return jsonify({'msg': "Credenciais invalidas"}), 400

        try:
            result.placa = placa
            result.ano = ano
            result.km_atual = km_atual
            result.prefixo = prefixo
            result.modelo = modelo
            result.status_atual = status_atual
            db_session.commit()
            return jsonify({"msg": "Viatura atualizado com sucesso!"}), 200

        except Exception as e:
            db_session.rollback()
            print(f'Error: {e}')
            return jsonify({'msg': str(e)}), 500
        finally:
            db_session.close()

@app.route('/put_responsavel/<var_id>', methods=['PUT'])
def put_responsavel(var_id):
    '''
    **API para Atualização de Dados do Responsável**

    ### Endpoint:
    PUT /put_responsavel/{var_id}

    ### Parâmetros de Path:
    * `var_id`: inteiro (obrigatório) - Identificador único do responsável que será atualizado.

    ### Parâmetros de Entrada (JSON):
    ```json
    {
        "nome": "string (obrigatório) - Nome atualizado do responsável",
        "email": "string (obrigatório) - Novo endereço de e-mail do responsável",
        "senha": "string (obrigatório) - Nova senha para acesso ao sistema",
        "cargo_funcao": "string (obrigatório) - Novo cargo ou função do responsável"
    }
    ```

    ### Respostas (JSON):
    * **200 OK:** Dados do responsável atualizados com sucesso.
      ```json
      {
          "msg": "Responsavel atualizado com sucesso!"
      }
      ```
    * **400 Bad Request:** Responsável não encontrado ou ausência de campos obrigatórios no JSON enviado.
      ```json
      {
          "msg": "Responsavel não encontrado"
      }
      ```
      *ou se faltarem dados (validação de credenciais):*
      ```json
      {
          "msg": "Credenciais invalidas"
      }
      ```
    * **500 Internal Server Error:** Falha operacional ou erro ao tentar salvar no banco de dados.
      ```json
      {
          "msg": "[Descrição do Erro Técnico]"
      }
      ```
    '''
    editar = select(Responsavel).where(Responsavel.id_responsavel == int(var_id))
    result = db_session.execute(editar).scalar_one_or_none()

    if not result:
        return jsonify({"msg": "Responsavel não encontrado"}), 400

    if request.method == 'PUT':
        dados = request.get_json()
        nome = dados.get('nome')
        email = dados.get('email')
        senha = dados.get('senha')
        cargo_funcao = dados.get('cargo_funcao')

        if not nome or not email or not senha or not cargo_funcao:
            return jsonify({'msg': "Credenciais invalidas"}), 400

        try:
            result.nome = nome
            result.email = email
            result.senha = senha
            result.cargo_funcao = cargo_funcao
            db_session.commit()
            return jsonify({"msg": "Responsavel atualizado com sucesso!"}), 200

        except Exception as e:
            db_session.rollback()
            print(f'Error: {e}')
            return jsonify({'msg': str(e)}), 500
        finally:
            db_session.close()

@app.route('/put_itens_manutencao/<var_id>', methods=['PUT'])
def put_itens_manutencao(var_id):
    '''
    **API para Atualização de Item de Manutenção**

    ### Endpoint:
    PUT /put_itens_manutencao/{var_id}

    ### Parâmetros de Path:
    * `var_id`: inteiro (obrigatório) - Identificador único do item de manutenção que será atualizado.

    ### Parâmetros de Entrada (JSON):
    ```json
    {
        "nome_item": "string (obrigatório) - Nome ou título do item de manutenção",
        "descricao": "string (obrigatório) - Descrição detalhada do item ou do serviço",
        "categoria_falha": "string (obrigatório) - Categoria ou classificação da falha/manutenção",
        "valor_unitario": "float/inteiro (obrigatório) - Valor unitário do item ou peça"
    }
    ```

    ### Respostas (JSON):
    * **200 OK:** Item de manutenção atualizado com sucesso.
      ```json
      {
          "msg": "Item de manutenção atualizado com sucesso!"
      }
      ```
    * **400 Bad Request:** Item não encontrado ou ausência de dados obrigatórios no JSON enviado.
      ```json
      {
          "msg": "Itens de manutenção não encontrados"
      }
      ```
      *ou se faltarem dados (validação de credenciais):*
      ```json
      {
          "msg": "Credenciais invalidas"
      }
      ```
    * **500 Internal Server Error:** Falha operacional ou erro ao tentar salvar no banco de dados.
      ```json
      {
          "msg": "[Descrição do Erro Técnico]"
      }
      ```
    '''
    editar = select(Itens_Manutencao).where(Itens_Manutencao.id_item == int(var_id))
    result = db_session.execute(editar).scalar_one_or_none()

    if not result:
        return jsonify({"msg": "Itens de manutenção não encontrados"}), 400

    if request.method == 'PUT':
        dados = request.get_json()
        nome_item = dados.get('nome_item')
        descricao = dados.get('descricao')
        categoria_falha = dados.get('categoria_falha')
        valor_unitario = dados.get('valor_unitario')

        if not nome_item or not descricao or not categoria_falha or not valor_unitario:
            return jsonify({'msg': "Credenciais invalidas"}), 400

        try:
            result.nome_item = nome_item
            result.descricao = descricao
            result.categoria_falha = categoria_falha
            result.valor_unitario = valor_unitario
            db_session.commit()
            return jsonify({"msg": "Item de manutenção atualizado com sucesso!"}), 200

        except Exception as e:
            db_session.rollback()
            print(f'Error: {e}')
            return jsonify({'msg': str(e)}), 500
        finally:
            db_session.close()

@app.route('/put_checklist_turno/<var_id>', methods=['PUT'])
def put_checklist_turno(var_id):
    '''
        **API para Atualização de Checklist de Turno**

        ### Endpoint:
        PUT /put_checklist_turno/{var_id}

        ### Parâmetros de Path:
        * `var_id`: inteiro (obrigatório) - Identificador único do checklist de turno que será atualizado.

        ### Parâmetros de Entrada (JSON):
        ```json
        {
            "viatura_id": "inteiro (obrigatório) - Identificador (ID) da viatura associada",
            "policial_id": "inteiro (obrigatório) - Identificador (ID) do policial que realizou o checklist",
            "nivel_oleo": "string (obrigatório) - Estado do nível de óleo (ex: regular, baixo)",
            "status_pneu": "string (obrigatório) - Estado de conservação dos pneus",
            "km_abertura": "inteiro/float (obrigatório) - Quilometragem do veículo na abertura do turno",
            "relatorio_problema": "string (obrigatório) - Descrição de avarias ou problemas identificados"
        }
        ```

        ### Respostas (JSON):
        * **200 OK:** Checklist de turno atualizado com sucesso.
          ```json
          {
              "msg": "Checklist atualizado com sucesso!"
          }
          ```
        * **400 Bad Request:** Checklist não encontrado ou ausência de parâmetros obrigatórios no JSON enviado.
          ```json
          {
              "msg": "Checklist não encontrados"
          }
          ```
          *ou se faltarem dados (validação de credenciais):*
          ```json
          {
              "msg": "Credenciais invalidas"
          }
          ```
        * **500 Internal Server Error:** Falha operacional ou erro ao tentar salvar no banco de dados.
          ```json
          {
              "msg": "[Descrição do Erro Técnico]"
          }
          ```

    '''

    editar = select(Checklist_Turno).where(Checklist_Turno.id_checklist == int(var_id))
    result = db_session.execute(editar).scalar_one_or_none()
    if not result:
        return jsonify({"msg": "Checklist não encontrados"}), 400

    if request.method == 'PUT':
        dados = request.get_json()
        viatura_id = dados.get('viatura_id')
        policial_id = dados.get('policial_id')
        nivel_oleo = dados.get('nivel_oleo')
        status_pneu = dados.get('status_pneu')
        km_abertura = dados.get('km_abertura')
        relatorio_problema = dados.get('relatorio_problema')

        if not viatura_id or not policial_id or not nivel_oleo or not status_pneu or not km_abertura or not relatorio_problema:
            return jsonify({'msg': "Credenciais invalidas"}), 400

        try:
            result.viatura_id = viatura_id
            result.policial_id = policial_id
            result.nivel_oleo = nivel_oleo
            result.status_pneu = status_pneu
            result.km_abertura = km_abertura
            result.relatorio_problema = relatorio_problema

            db_session.commit()
            return jsonify({"msg": "Checklist atualizado com sucesso!"}), 200

        except Exception as e:
            db_session.rollback()
            print(f'Error: {e}')
            return jsonify({'msg': str(e)}), 500
        finally:
            db_session.close()


@app.route('/put_ordem_servico/<var_id>', methods=['PUT'])
def put_ordem_servico(var_id):
    '''
        **API para Atualização de Ordem de Serviço (OS)**

        ### Endpoint:
        PUT /put_ordem_servico/{var_id}

        ### Parâmetros de Path:
        * `var_id`: inteiro (obrigatório) - Identificador único da ordem de serviço que será atualizada.

        ### Parâmetros de Entrada (JSON):
        ```json
        {
            "viatura_id": "inteiro (obrigatório) - Identificador (ID) da viatura associada",
            "responsavel_id": "inteiro (obrigatório) - Identificador (ID) do responsável pela OS",
            "tipo_manutencao": "string (obrigatório) - Tipo de manutenção (ex: corretiva, preventiva)",
            "status_os": "string (obrigatório) - Status atual da ordem (ex: aberta, em andamento, concluída)",
            "custo_total": "float/inteiro (obrigatório) - Valor total do custo da manutenção"
        }
        ```

        ### Respostas (JSON):
        * **200 OK:** Ordem de serviço atualizada com sucesso.
          ```json
          {
              "msg": "Ordem de serivço atualizado com sucesso!"
          }
          ```
        * **400 Bad Request:** Ordem de serviço não encontrada ou ausência de campos obrigatórios no JSON enviado.
          ```json
          {
              "msg": "Ordem de serviço não encontrados"
          }
          ```
          *ou se faltarem dados (validação de credenciais):*
          ```json
          {
              "msg": "Credenciais invalidas"
          }
          ```
        * **500 Internal Server Error:** Falha operacional ou erro ao tentar salvar no banco de dados.
          ```json
          {
              "msg": "[Descrição do Erro Técnico]"
          }
          ```
    '''

    editar = select(Ordem_Servico).where(Ordem_Servico.id_ordem == int(var_id))
    result = db_session.execute(editar).scalar_one_or_none()

    if not result:
        return jsonify({"msg": "Ordem de serviço não encontrados"}), 400

    if request.method == 'PUT':
        dados = request.get_json()
        viatura_id = dados.get('viatura_id')
        responsavel_id = dados.get('responsavel_id')
        tipo_manutencao = dados.get('tipo_manutencao')
        status_os = dados.get('status_os')
        custo_total = dados.get('custo_total')
        print('asd',tipo_manutencao)
        if not viatura_id or not responsavel_id or not tipo_manutencao or not status_os or not custo_total:
            return jsonify({'msg': "Credenciais invalidas"}), 400

        try:
            result.viatura_id = viatura_id
            result.responsavel_id = responsavel_id
            result.tipo_manutencao = tipo_manutencao
            result.status_os = status_os
            result.custo_total = custo_total
            db_session.commit()
            return jsonify({"msg": "Ordem de serivço atualizado com sucesso!"}), 200

        except Exception as e:
            db_session.rollback()
            print(f'Error: {e}')
            return jsonify({'msg': str(e)}), 500
        finally:
            db_session.close()


@app.route('/put_ordem_itens/<var_id>', methods=['PUT'])
def put_ordem_itens(var_id):
    '''
        **API para Atualização de Vínculo de Itens na Ordem de Serviço**

        ### Endpoint:
        PUT /put_ordem_itens/{var_id}

        ### Parâmetros de Path:
        * `var_id`: inteiro (obrigatório) - Identificador único do registro de vínculo (`id_lista`) que será atualizado.

        ### Parâmetros de Entrada (JSON):
        ```json
        {
            "os_id": "inteiro (obrigatório) - Identificador (ID) da ordem de serviço associada",
            "item_id": "inteiro (obrigatório) - Identificador (ID) do item de manutenção associado"
        }
        ```

        ### Respostas (JSON):
        * **200 OK:** Vínculo de itens atualizado com sucesso.
          ```json
          {
              "msg": "Ordem de itens atualizado com sucesso!"
          }
          ```
        * **400 Bad Request:** Registro de vínculo não encontrado ou ausência de dados obrigatórios no JSON enviado.
          ```json
          {
              "msg": "Ordem de itens não encontrados"
          }
          ```
          *ou se faltarem dados (validação de credenciais):*
          ```json
          {
              "msg": "Credenciais invalidas"
          }
          ```
        * **500 Internal Server Error:** Falha operacional ou erro ao tentar salvar as alterações no banco de dados.
          ```json
          {
              "msg": "[Descrição do Erro Técnico]"
          }
          ```
    '''
    editar = select(Ordem_Itens).where(Ordem_Itens.id_lista == int(var_id))
    result = db_session.execute(editar).scalar_one_or_none()

    if not result:
        return jsonify({"msg": "Ordem de itens não encontrados"}), 400

    if request.method == 'PUT':
        dados = request.get_json()
        os_id = dados.get('os_id')
        item_id = dados.get('item_id')

        if not os_id or not item_id:
            return jsonify({'msg': "Credenciais invalidas"}), 400

        try:
            result.os_id = os_id
            result.item_id = item_id
            db_session.commit()
            return jsonify({"msg": "Ordem de itens atualizado com sucesso!"}), 200

        except Exception as e:
            db_session.rollback()
            print(f'Error: {e}')
            return jsonify({'msg': str(e)}), 500
        finally:
            db_session.close()






@app.route('/delete_policial/<var_id>', methods=['DELETE'])
def delete_policial(var_id):
    """
    **API para Remoção de Policial**

    ### Endpoint:
    DELETE /delete_policial/{id}

    ### Parâmetros de Path:
    * `id`: inteiro (obrigatório) - Identificador único do policial que será removido.

    ### Respostas (JSON):
    * **200 OK:** Policial removido com sucesso.
      ```json
      {
          "msg": "Policial removido com sucesso",
          "id": policial.id_policial
      }
      ```
    * **400 Bad Request:** Requisição inválida ou erro na sintaxe dos parâmetros.
      ```json
      {
          "msg": "Valor não Encontrado"
      }
      ```
    * **404 Not Found:** Policial com o ID fornecido não foi encontrado no sistema.
      ```json
      {
          "msg": "Policial não encontrado"
      }
      ```
    * **500 Internal Server Error:** Falha operacional no banco de dados.
      ```json
      {
          "msg": "[Descricao do Erro]"
      }
      ```
    """

    sql_p = select(Policial).where(Policial.id_policial == int(var_id))
    result = db_session.execute(sql_p).scalar_one_or_none()
    if not result:
        return jsonify({"msg": "Policial não encontrado"}), 400

    try:
        db_session.delete(result)
        db_session.commit()
        return jsonify({"msg": "Policial deletado com sucesso!"}), 200

    except Exception as e:
        print(f'Error: {e}')
        db_session.rollback()
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.close()

@app.route('/delete_viatura/<var_id>', methods=['DELETE'])
def delete_viatura(var_id):
    """
            **API para Remoção de Viatura**

        ### Endpoint:
        DELETE /delete_viatura/{var_id}

        ### Parâmetros de Path:
        * `var_id`: inteiro (obrigatório) - Identificador único da viatura que será removida.

        ### Respostas (JSON):
        * **200 OK:** Viatura removida com sucesso.
          ```json
          {
              "msg": "Viatura deletada com sucesso!"
          }
          ```
        * **400 Bad Request:** Viatura com o ID fornecido não foi encontrada no sistema.
          ```json
          {
              "msg": "Viatura não encontrada"
          }
          ```
        * **500 Internal Server Error:** Falha operacional ou erro ao tentar deletar do banco de dados.
          ```json
          {
              "msg": "[Descrição do Erro Técnico]"
          }
          ```
    """
    delete = select(Viatura).where(Viatura.id_viatura == int(var_id))
    result = db_session.execute(delete).scalar_one_or_none()
    if not result:
        return jsonify({"msg": "Viatura não encontrada"}), 400

    try:
        db_session.delete(result)
        db_session.commit()
        return jsonify({"msg": "Viatura deletada com sucesso!"}), 200

    except Exception as e:
        print(f'Error: {e}')
        db_session.rollback()
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.close()

@app.route('/delete_responsavel/<var_id>', methods=['DELETE'])
def delete_responsavel(var_id):
    """
    **API para Remoção de Responsável**

    ### Endpoint:
    DELETE /delete_responsavel/{var_id}

    ### Parâmetros de Path:
    * `var_id`: inteiro (obrigatório) - Identificador único do responsável que será removido.

    ### Respostas (JSON):
    * **200 OK:** Responsável removido com sucesso.
      ```json
      {
          "msg": "Responsavel deletado com sucesso!"
      }
      ```
    * **400 Bad Request:** Responsável com o ID fornecido não foi encontrado no sistema.
      ```json
      {
          "msg": "Responsavel não encontrado"
      }
      ```
    * **500 Internal Server Error:** Falha operacional ou erro ao tentar deletar do banco de dados.
      ```json
      {
          "msg": "[Descrição do Erro Técnico]"
      }
      ```
    """
    delete = select(Responsavel).where(Responsavel.id_responsavel == int(var_id))
    result = db_session.execute(delete).scalar_one_or_none()
    if not result:
        return jsonify({"msg": "Responsavel não encontrado"}), 400

    try:
        db_session.delete(result)
        db_session.commit()
        return jsonify({"msg": "Responsavel deletado com sucesso!"}), 200

    except Exception as e:
        print(f'Error: {e}')
        db_session.rollback()
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.close()

@app.route('/delete_itens_manutencao/<var_id>', methods=['DELETE'])
def delete_itens_manutencao(var_id):
    """
    **API para Remoção de Itens de Manutenção**

    ### Endpoint:
    DELETE /delete_itens_manutencao/{var_id}

    ### Parâmetros de Path:
    * `var_id`: inteiro (obrigatório) - Identificador único do item de manutenção que será removido.

    ### Respostas (JSON):
    * **200 OK:** Item de manutenção removido com sucesso.
      ```json
      {
          "msg": "Itens_Manutencao deletado com sucesso!"
      }
      ```
    * **400 Bad Request:** Item com o ID fornecido não foi encontrado no sistema.
      ```json
      {
          "msg": "Itens_Manutencao não encontrado"
      }
      ```
    * **500 Internal Server Error:** Falha operacional ou erro ao tentar deletar do banco de dados.
      ```json
      {
          "msg": "[Descrição do Erro Técnico]"
      }
    ```
    """
    delete = select(Itens_Manutencao).where(Itens_Manutencao.id_item == int(var_id))
    result = db_session.execute(delete).scalar_one_or_none()
    if not result:
        return jsonify({"msg": "Itens_Manutencao não encontrado"}), 400

    try:
        db_session.delete(result)
        db_session.commit()
        return jsonify({"msg": "Itens_Manutencao deletado com sucesso!"}), 200

    except Exception as e:
        print(f'Error: {e}')
        db_session.rollback()
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.close()

@app.route('/delete_checklist_turno/<var_id>', methods=['DELETE'])
def delete_checklist_turno(var_id):
    """
    **API para Remoção de Checklist de Turno**

    ### Endpoint:
    DELETE /delete_checklist_turno/{var_id}

    ### Parâmetros de Path:
    * `var_id`: inteiro (obrigatório) - Identificador único do checklist de turno que será removido.

    ### Respostas (JSON):
    * **200 OK:** Checklist de turno removido com sucesso.
      ```json
      {
          "msg": "Checklist deletado com sucesso!"
      }
      ```
    * **400 Bad Request:** Checklist com o ID fornecido não foi encontrado no sistema.
      ```json
      {
          "msg": "Checklist não encontrado"
      }
      ```
    * **500 Internal Server Error:** Falha operacional ou erro ao tentar deletar do banco de dados.
      ```json
      {
          "msg": "[Descrição do Erro Técnico]"
      }
      ```
    """
    delete = select(Checklist_Turno).where(Checklist_Turno.id_checklist == int(var_id))
    result = db_session.execute(delete).scalar_one_or_none()
    if not result:
        return jsonify({"msg": "Checklist não encontrado"}), 400

    try:
        db_session.delete(result)
        db_session.commit()
        return jsonify({"msg": "Checklist deletado com sucesso!"}), 200

    except Exception as e:
        print(f'Error: {e}')
        db_session.rollback()
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.close()

@app.route('/delete_ordem_servico/<var_id>', methods=['DELETE'])
def delete_ordem_servico(var_id):
    """
    **API para Remoção de Policial**

    ### Endpoint:
    DELETE /delete_policial/{id}

    ### Parâmetros de Path:
    * `id`: inteiro (obrigatório) - Identificador único do policial que será removido.

    ### Respostas (JSON):
    * **200 OK:** Policial removido com sucesso.
      ```json
      {
          "msg": "Policial removido com sucesso",
          "id": policial.id_policial
      }
      ```
    * **400 Bad Request:** Requisição inválida ou erro na sintaxe dos parâmetros.
      ```json
      {
          "msg": "Valor não Encontrado"
      }
      ```
    * **404 Not Found:** Policial com o ID fornecido não foi encontrado no sistema.
      ```json
      {
          "msg": "Policial não encontrado"
      }
      ```
    * **500 Internal Server Error:** Falha operacional no banco de dados.
      ```json
      {
          "msg": "[Descricao do Erro]"
      }
      ```
    """
    delete = select(Ordem_Servico).where(Ordem_Servico.id_ordem == int(var_id))
    result = db_session.execute(delete).scalar_one_or_none()
    if not result:
        return jsonify({"msg": "Ordem de serviço não encontrada"}), 400

    try:
        db_session.delete(result)
        db_session.commit()
        return jsonify({"msg": "Ordem de serviço deletada com sucesso!"}), 200

    except Exception as e:
        print(f'Error: {e}')
        db_session.rollback()
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.close()

@app.route('/delete_ordem_itens<var_id>', methods=['DELETE'])
def delete_ordem_itens(var_id):
    """
    **API para Remoção de Ordem de Serviço (OS)**

    ### Endpoint:
    DELETE /delete_ordem_servico/{var_id}

    ### Parâmetros de Path:
    * `var_id`: inteiro (obrigatório) - Identificador único da ordem de serviço que será removida.

    ### Respostas (JSON):
    * **200 OK:** Ordem de serviço removida com sucesso.
      ```json
      {
          "msg": "Ordem de serviço deletada com sucesso!"
      }
      ```
    * **400 Bad Request:** Ordem de serviço com o ID fornecido não foi encontrada no sistema.
      ```json
      {
          "msg": "Ordem de serviço não encontrada"
      }
      ```
    * **500 Internal Server Error:** Falha operacional ou erro ao tentar deletar do banco de dados.
      ```json
      {
          "msg": "[Descrição do Erro Técnico]"
      }
      ```
    """
    delete = select(Ordem_Itens).where(Ordem_Itens.id_lista == int(var_id))
    result = db_session.execute(delete).scalar_one_or_none()
    if not result:
        return jsonify({"msg": "Ordens de itens não encontrado"}), 400

    try:
        db_session.delete(result)
        db_session.commit()
        return jsonify({"msg": "Ordens de itens deletado com sucesso!"}), 200

    except Exception as e:
        print(f'Error: {e}')
        db_session.rollback()
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.close()







@app.route('/pesquisar_policial', methods=['POST'])
def pesquisar_policial():
    """
    **API para Pesquisa de Policial**

    ### Endpoint:
    POST /pesquisar_policial

    ### Parâmetros de Entrada (JSON):
    ```json
    {
        "matricula": "string (obrigatório) - Número da matrícula funcional (o sistema adicionará o prefixo 'PM-')"
    }
    ```

    ### Respostas (JSON):
    * **200 OK:** Lista contendo os dados dos policiais encontrados para a matrícula informada.
      ```json
      [
          {
              "id_policial": 1,
              "nome": "Nome completo do policial",
              "email": "Email institucional ou pessoal",
              "cargo_patente": "Cargo ou patente atual",
              "matricula": "PM-XXXXX"
          }
      ]
      ```
    * **400 Bad Request:** Matrícula não fornecida no corpo da requisição.
      ```json
      {
          "msg": "Nenhum policial encontrado"
      }
      ```
    * **500 Internal Server Error:** Falha operacional ou erro ao tentar consultar o banco de dados.
      ```json
      {
          "msg": "[Descrição do Erro Técnico]"
      }
      ```

    """
    dados = request.get_json()
    matricula = dados.get('matricula')
    if not matricula:
        return jsonify({"msg": "Nenhum policial encontrado"}), 400
    try:
        busca = select(Policial).where(Policial.matricula == f"PM-{matricula}")
        rastreio = db_session.execute(busca).scalars().all()
        lista = []
        for r in rastreio:
            lista.append(r.serialize())
        return jsonify(lista), 200
    except Exception as e:
        print(f'Error: {e}')
        db_session.rollback()
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.close()

@app.route('/pesquisar_viatura', methods=['POST'])
def pesquisar_viatura():
    """
       **API para Pesquisa de Viatura**

        ### Endpoint:
        POST /pesquisar_viatura

        ### Parâmetros de Entrada (JSON):
        ```json
        {
            "prefixo": "string (obrigatório) - Prefixo de identificação da viatura (o sistema adicionará o prefixo 'VTR-')"
        }
        ```

        ### Respostas (JSON):
        * **200 OK:** Lista contendo os dados das viaturas encontradas para o prefixo informado.
          ```json
          [
              {
                  "id_viatura": 1,
                  "placa": "string - Placa de identificação do veículo",
                  "ano": "inteiro - Ano de fabricação ou modelo",
                  "km_atual": "inteiro/float - Quilometragem atualizada do veículo",
                  "prefixo": "string - VTR-XXXX",
                  "modelo": "string - Modelo do veículo",
                  "status_atual": "string - Estado operacional atual da viatura"
              }
          ]
          ```
        * **400 Bad Request:** Prefixo não fornecido no corpo da requisição.
          ```json
          {
              "msg": "Nenhuma viatura encontrado"
          }
          ```
        * **500 Internal Server Error:** Falha operacional ou erro ao tentar consultar o banco de dados.
          ```json
          {
              "msg": "[Descrição do Erro Técnico]"
          }
          ```
    """
    dados = request.get_json()
    prefixo = dados.get('prefixo')
    if not prefixo:
        return jsonify({"msg": "Nenhuma viatura encontrado"}), 400

    try:
        busca = select(Viatura).where(Viatura.prefixo ==  f"VTR-{prefixo}")
        rastreio = db_session.execute(busca).scalars().all()
        lista = []
        for r in rastreio:
            lista.append(r.serialize())

        db_session.commit()
        return jsonify(lista), 200

    except Exception as e:
        print(f'Error: {e}')
        db_session.rollback()
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.close()

@app.route('/pesquisar_responsavel', methods=['POST'])
def pesquisar_responsavel():
    """
            **API para Pesquisa de Responsável**

        ### Endpoint:
        POST /pesquisar_responsavel

        ### Parâmetros de Entrada (JSON):
        ```json
        {
            "email": "string (obrigatório) - Endereço de e-mail institucional ou pessoal do responsável"
        }
        ```

        ### Respostas (JSON):
        * **200 OK:** Lista contendo os dados dos responsáveis encontrados para o e-mail informado.
          ```json
          [
              {
                  "id_responsavel": 1,
                  "nome": "Nome completo do responsável",
                  "email": "Email institucional ou pessoal",
                  "cargo_funcao": "Cargo ou função do responsável"
              }
          ]
          ```
        * **400 Bad Request:** E-mail não fornecido no corpo da requisição.
          ```json
          {
              "msg": "Nenhum rsponsavel encontrado"
          }
          ```
        * **500 Internal Server Error:** Falha operacional ou erro ao tentar consultar o banco de dados.
          ```json
          {
              "msg": "[Descrição do Erro Técnico]"
          }
          ```
    """
    dados = request.get_json()
    email = dados.get('email')
    if not email:
        return jsonify({"msg": "Nenhum rsponsavel encontrado"}), 400

    try:
        busca = select(Responsavel).where(Responsavel.email == email)
        rastreio = db_session.execute(busca).scalars().all()
        lista = []
        for r in rastreio:
            lista.append(r.serialize())

        db_session.commit()
        return jsonify(lista), 200

    except Exception as e:
        print(f'Error: {e}')
        db_session.rollback()
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.close()

@app.route('/pesquisar_itens_manutencao', methods=['POST'])
def pesquisar_itens_manutencao():
    """
            **API para Pesquisa de Itens de Manutenção**

        ### Endpoint:
        POST /pesquisar_itens_manutencao

        ### Parâmetros de Entrada (JSON):
        ```json
        {
            "nome_item": "string (obrigatório) - Nome ou denominação exata do item de manutenção"
        }
        ```

        ### Respostas (JSON):
        * **200 OK:** Lista contendo os dados dos itens de manutenção encontrados para o nome informado.
          ```json
          [
              {
                  "id_item": 1,
                  "nome_item": "Nome ou denominação do item de manutenção",
                  "descricao": "Detalhes ou descrição técnica do item",
                  "categoria_falha": "Categoria ou classificação da falha vinculada",
                  "valor_unitario": 0.0
              }
          ]
          ```
        * **400 Bad Request:** Nome do item não fornecido no corpo da requisição.
          ```json
          {
              "msg": "Nenhum item encontrado"
          }
          ```
        * **500 Internal Server Error:** Falha operacional ou erro ao tentar consultar o banco de dados.
          ```json
          {
              "msg": "[Descrição do Erro Técnico]"
          }
    """
    dados = request.get_json()
    nome_item = dados.get('nome_item')
    print('nome_item', nome_item)
    if not nome_item:
        return jsonify({"msg": "Nenhum item encontrado"}), 400

    try:
        busca = select(Itens_Manutencao).where(Itens_Manutencao.nome_item == nome_item)
        rastreio = db_session.execute(busca).scalars().all()
        lista = []
        for r in rastreio:
            print(r.nome_item, r.id_item)
            print(r.serialize())

            lista.append(r.serialize())

        db_session.commit()
        return jsonify(lista), 200

    except Exception as e:
        print(f'Error: {e}')
        db_session.rollback()
        return jsonify({'msg': str(e)}), 500
    finally:
        db_session.close()


if __name__ == '__main__':
    app.run(debug=True,port=5005,host='0.0.0.0')