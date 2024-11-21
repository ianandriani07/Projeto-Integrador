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

@app.route('/criar-formulario', methods=['POST'])
def criar_formulario():
    
    try:
        data = request.json
        
        if 'titulo' not in data or not data['titulo']:
            return jsonify({"erro": "O campo 'titulo' é obrigatório."}), 400
        
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
        
@app.route('/criar-pergunta/', methods=['POST'])
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
            ordem = data['ordem'] if 'ordem' in data else get_max_ordem(),
            nome_variavel = nome_variavel
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