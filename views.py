from app import app, login_manager, db
from flask import render_template, redirect, url_for, flash, session, jsonify, request, json
from models import *
from helpers import *

@app.route('/')
def inicio():
    return redirect(url_for('login'))

@app.route('/hub', methods=['GET', 'POST'])
def hub():
    return render_template('hub.html')

@app.route('/new-user', methods=['GET'])
def new_user():
    return render_template('new_user.html')

@app.route('/<int:id_formulario>/form', methods=['GET'])
def project(id_formulario):
    
    formulario = Formularios.query.get(id_formulario)
    
    if not formulario:
        return redirect(url_for('hub'))
    
    return render_template('form.html', id_formulario=id_formulario)

@app.route('/criar-formulario', methods=['POST'])
def criar_formulario():
    
    try:
        data = request.json
        
        if 'titulo' not in data or not data['titulo']:
            return jsonify({"status": False, "erro": "O campo 'titulo' é obrigatório."}), 400
        
        titulo = data['titulo']
        if not verificar_titulo_formulario_existente(titulo):
            return jsonify({
                "status": False,
                "erro": "titulo de formulário já existente."
            }), 400
        
        formulario = Formularios(
            titulo=data['titulo'],
            descricao=data.get('descricao'),  # Opcional
            ativo=data.get('ativo', True),   # Default: True
            formula=data.get('formula')     # Opcional
        )

        db.session.add(formulario)
        db.session.commit()
        
        return jsonify({
            "status": True,
            "mensagem": "Formulário criado com sucesso!"
        }), 201
    
    except Exception as e:
        return jsonify({
            "status": False,
            "erro": str(e)
        }), 500
        
@app.route('/formularios')
def listar_formularios():
    
    try:   
        formularios = Formularios.query.all()
        resultado = []
        
        for formulario in formularios:
            resultado.append(
                {
                    "id": formulario.id,
                    "titulo": formulario.titulo,
                    "descricao": formulario.descricao,
                    "data_criacao": formulario.data_criacao.strftime('%Y-%m-%dT%H:%M:%S'),
                    "ativo": formulario.ativo,
                    "formula": formulario.formula
                }
            )
        
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify(
            {
                "status": False,
                "erro": str(e)
            }
        ), 500
        
@app.route('/formulario/<int:id_formulario>')
def listar_formulario(id_formulario):
    try:
        formulario = Formularios.query.get(id_formulario)
        
        if not formulario:
            return jsonify({"status": False, "erro": "Formulário não encontrado."}), 404
        
        resultado = {
            "id": formulario.id,
            "titulo": formulario.titulo,
            "descricao": formulario.descricao,
            "data_criacao": formulario.data_criacao.strftime('%Y-%m-%dT%H:%M:%S'),
            "ativo": formulario.ativo,
            "formula": formulario.formula
        }

        # Retornar o JSON do formulário
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify(
            {
                "status": False,
                "erro": str(e)       
            }
        ), 500
        
@app.route('/criar-pergunta', methods=['POST'])
def criar_perguntas():
    try:
        data = request.json
        
        campos = ['id_formulario', 'texto', 'tipo', 'nome_variavel']
        campos_faltando = [campo for campo in campos if campo not in data or data[campo] is None]
        
        if campos_faltando:
            return jsonify({
                "status": False,
                "erro": f"Os seguintes campos estão faltando ou nulos: {', '.join(campos_faltando)}"
            }), 400
        
        
        id_formulario = data['id_formulario']
        if not verificar_id_formulario(id_formulario):
            return jsonify({
                "status": False,
                "erro": "id_formulario inexistente."
            }), 400
            
            
        tipo = data['tipo']
        id_tipo = get_id_tipos_pergunta(tipo)
        if id_tipo == 0:
            return jsonify({
                "status": False,
                "erro": "tipo inexistente."
        }), 400
            
        formula = data.get('formula', None)
        if formula:
            try:
                formula = json.dumps(formula)  # Converte dicionário para JSON
            except Exception as e:
                return jsonify({
                    "status": False,
                    "erro": f"Erro ao processar fórmula: {str(e)}"
                }), 400
        
        nome_variavel = data['nome_variavel']
        if not verificar_nome_variavel_pergunta(nome_variavel):
            return jsonify({
                "status": False,
                "erro": "nome_variavel já existente."
            })
            
        pergunta = Perguntas(
            id_formulario = id_formulario,
            texto = data['texto'],
            id_tipo = id_tipo,
            ordem = data['ordem'] if 'ordem' in data else get_max_ordem()+1,
            nome_variavel = nome_variavel,
            formula=formula
        )
        
        db.session.add(pergunta)
        db.session.commit()
        
        return jsonify(
            {
                "status": True,
                "mensagem": "Pergunta criada com sucesso!"
            }
        ), 201
        
    except Exception as e:
        return jsonify({
            "status": False,
            "erro": str(e)
        }), 500
        
@app.route('/perguntas/formulario/<int:id_formulario>')
def listar_perguntas_formulario(id_formulario):
    try:
        # Verifica se o formulário existe
        if not verificar_id_formulario(id_formulario):
            return jsonify({
                "status": False,
                "erro": "O formulário com o ID fornecido não existe."
            }), 404

        # Parâmetros de paginação
        pagina = request.args.get('pagina', 1, type=int)  # Página atual (padrão 1)
        por_pagina = request.args.get('por_pagina', 5, type=int)  # Itens por página (padrão 5)

        # Consulta com order_by para evitar erro no SQL Server
        perguntas_paginated = Perguntas.query.filter_by(id_formulario=id_formulario)\
            .order_by(Perguntas.ordem)\
            .paginate(page=pagina, per_page=por_pagina, error_out=False)

        # Lista de perguntas paginadas
        perguntas = perguntas_paginated.items

        # IDs das perguntas para buscar as opções (apenas para tipos 1 e 4)
        id_perguntas_com_opcoes = [
            pergunta.id for pergunta in perguntas if pergunta.id_tipo in [1, 4]
        ]
        opcoes = Opcoes.query.filter(Opcoes.id_pergunta.in_(id_perguntas_com_opcoes)).order_by(Opcoes.ordem).all()

        # Organiza as opções por id_pergunta
        opcoes_por_pergunta = {}
        for opcao in opcoes:
            if opcao.id_pergunta not in opcoes_por_pergunta:
                opcoes_por_pergunta[opcao.id_pergunta] = []
            opcoes_por_pergunta[opcao.id_pergunta].append(opcao)

        # Monta o resultado paginado
        resultado = []
        for pergunta in perguntas:
            id_pergunta = pergunta.id
            lista_opcoes = []
            tabela_conversao = {}

            # Adicionar opções e tabela de conversão apenas para tipos 1 e 4
            if pergunta.id_tipo in [1, 4]:  # Objetiva ou Múltipla Escolha
                lista_opcoes = [
                    {
                        "id": opcao.id,
                        "texto": opcao.texto,
                        "ordem": opcao.ordem,
                        "pontuacao": opcao.pontuacao
                    }
                    for opcao in opcoes_por_pergunta.get(id_pergunta, [])
                ]
                tabela_conversao = {opcao.texto: opcao.pontuacao for opcao in opcoes_por_pergunta.get(id_pergunta, [])}

            # Carregar fórmula se disponível
            formula = json.loads(pergunta.formula) if pergunta.formula else None

            # Construir a resposta da pergunta
            resultado.append({
                "id": id_pergunta,
                "id_formulario": pergunta.id_formulario,
                "texto": pergunta.texto,
                "tipo": get_descricao_tipo(pergunta.id_tipo),  # Pega a descrição do tipo
                "ordem": pergunta.ordem,
                "obrigatoria": pergunta.obrigatoria,
                "nome_variavel": pergunta.nome_variavel,
                "opcoes": lista_opcoes,  # Lista de opções (vazia para outros tipos)
                "tabela_conversao": tabela_conversao,  # Tabela de conversão (vazia para outros tipos)
                "formula": formula  # Fórmula associada à pergunta (se existir)
            })

        # Retorna o JSON com paginação
        return jsonify({
            "id_formulario": id_formulario,
            "pagina_atual": pagina,
            "total_paginas": perguntas_paginated.pages,
            "total_registros": perguntas_paginated.total,
            "perguntas": resultado
        }), 200

    except Exception as e:
        return jsonify({
            "status": False,
            "erro": str(e)
        }), 500

@app.route('/criar-opcoes', methods=['POST'])
def criar_opcoes():
    try:
        # Obtém o JSON enviado
        data = request.json

        # Validação inicial dos campos principais
        campos = ['id_pergunta', 'opcoes']
        campos_faltando = [campo for campo in campos if campo not in data or data[campo] is None]

        if campos_faltando:
            return jsonify({
                "status": False,
                "erro": f"Os seguintes campos estão faltando ou nulos: {', '.join(campos_faltando)}"
            }), 400

        id_pergunta = data['id_pergunta']

        # Verifica se o id_pergunta existe
        if not verificar_id_pergunta(id_pergunta):
            return jsonify({
                "status": False,
                "erro": "O campo 'id_pergunta' não corresponde a uma pergunta existente."
            }), 400
        else:
            if verifica_opcoes_perguntas(id_pergunta):
               return jsonify({
                   "status": False,
                   "erro": "Já existem opcoes associadas a essa pergunta."
               }) 

        opcoes = data['opcoes']

        # Valida se há ao menos uma opção
        if not isinstance(opcoes, list) or len(opcoes) < 1:
            return jsonify({
                "status": False,
                "erro": "O campo 'opcoes' deve conter ao menos uma opção."
            }), 400

        # Lista de campos obrigatórios para cada opção
        campos_opcoes = ['texto', 'ordem', 'pontuacao']
        erros_opcoes = []

        # Valida cada opção na lista de opcoes
        for i, opcao in enumerate(opcoes):
            faltando = [campo for campo in campos_opcoes if campo not in opcao or opcao[campo] is None]
            if faltando:
                erros_opcoes.append({
                    "opcao": i + 1,  # Posição da opção (começando de 1 para ser mais intuitivo)
                    "problema": "Campo(s) faltando",
                    "campos_faltando": faltando
                })
            elif not isinstance(opcao.get('pontuacao'), (int, float)):
                erros_opcoes.append({
                    "opcao": i + 1,
                    "problema": "O campo 'pontuacao' deve ser um número inteiro ou float."
                })
            elif not isinstance(opcao.get('ordem'), int):
                erros_opcoes.append({
                    "opcao": i + 1,
                    "problema": "O campo 'ordem' deve ser um número inteiro."
                })

        # Retorna erro se alguma opção estiver inválida
        if erros_opcoes:
            return jsonify({
                "status": False,
                "erro": "Algumas opções têm problemas de validação.",
                "detalhes": erros_opcoes
            }), 400

        # Adiciona as opções ao banco de dados
        for opcao in opcoes:
            nova_opcao = Opcoes(
                id_pergunta=id_pergunta,
                texto=opcao['texto'],
                ordem=opcao['ordem'],
                pontuacao=opcao['pontuacao']
            )
            db.session.add(nova_opcao)

        # Confirma a transação no banco
        db.session.commit()

        # Resposta de sucesso
        return jsonify({
            "status": True,
            "mensagem": "Opções criadas com sucesso!"
        }), 201

    except Exception as e:
        # Rollback em caso de erro para evitar inconsistências no banco
        db.session.rollback()
        return jsonify({
            "status": False,
            "erro": str(e)
        }), 500
        
@app.route('/opcoes/pergunta/<int:id_pergunta>')
def listar_opcoes_perguntas(id_pergunta):
    try:
        if not verificar_id_pergunta(id_pergunta):
            return jsonify({
                "status": False,
                "erro": "A pergunta com o ID fornecido não existe."
            }), 404
        
        opcoes = Opcoes.query.filter_by(id_pergunta=id_pergunta).order_by(Opcoes.ordem).all()
        
        tabela_conversao = {opcao.texto: opcao.pontuacao for opcao in opcoes}
        
        lista_opcoes = [
            {
                "id": opcao.id,
                "texto": opcao.texto,
                "ordem": opcao.ordem,
                "pontuacao": opcao.pontuacao
            } 
            for opcao in opcoes
        ]

        return jsonify({
            "id_pergunta": id_pergunta,
            "tabela_conversao": tabela_conversao,
            "opcoes": lista_opcoes
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": False,
            "erro": str(e)
        }), 500

@app.route('/responder-perguntas', methods=['POST'])
def responder_perguntas():
    try:
        data = request.json
        
        if not isinstance(data, list):
            return jsonify({
                "status": False,
                "erro": "O corpo da requisição deve ser uma lista de objetos contendo 'nome_variavel' e 'resposta'."
            }), 400
        
        respostas_a_salvar = []
        erros = []
        
        for idx, resposta in enumerate(data):
            # Verifica se os campos necessários estão presentes e não nulos
            campos = ['nome_variavel', 'resposta']
            campos_faltando = [campo for campo in campos if campo not in resposta or resposta[campo] is None]
            
            if campos_faltando:
                erros.append({
                    "indice": idx,
                    "erro": f"Os seguintes campos estão faltando ou nulos: {', '.join(campos_faltando)}"
                })
                continue
            
            # Cria a instância da resposta
            respostas_a_salvar.append(Respostas(
                nome_variavel=resposta['nome_variavel'],
                valor_resposta=resposta['resposta']
            ))
        
        # Se houver erros, retorna os detalhes
        if erros:
            return jsonify({
                "status": False,
                "erros": erros
            }), 400
        
        # Salva todas as respostas válidas no banco de dados
        db.session.add_all(respostas_a_salvar)
        db.session.commit()
        
        return jsonify({
            "status": True,
            "mensagem": f"{len(respostas_a_salvar)} respostas cadastradas com sucesso!"
        }), 201
    except Exception as e:
        return jsonify({
            "status": False,
            "erro": f"Ocorreu um erro interno: {str(e)}"
        }), 500
        
@app.route('/respostas', methods=['GET'])
def listar_respostas():
    # Consultando todas as respostas
    respostas = Respostas.query.all()

    # Convertendo para formato JSON
    respostas_json = [
        {"nome_variavel": resposta.nome_variavel, "valor_resposta": resposta.valor_resposta}
        for resposta in respostas
    ]

    return jsonify(respostas_json)