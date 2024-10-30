from app import app, login_manager, db
from flask import render_template, redirect, url_for, flash, session, jsonify, request
from models import *

@app.route('/')
def inicio():
    return redirect(url_for('login'))

@app.route('/hub', methods=['GET', 'POST'])
def hub():
    return render_template('hub.html')

@app.route('/projetos')
def get_projetos():
    
    projetos = Projetos.query.all()

    lista_projetos = []
    
    for item_projeto in projetos:
        
        projeto = {
            "id": item_projeto.ID,
            "nome_projeto": item_projeto.Nome,
            "descricao": item_projeto.Descricao,
            "id_coordenador": item_projeto.CoordenadorID    
        }
        
        lista_projetos.append(projeto)
        
    return jsonify(lista_projetos)

@app.route('/projeto/<int:id_projeto>')
def get_projeto(id_projeto):
    
    busca_projeto = Projetos.query.get(id_projeto)
    
    if busca_projeto:
        projeto = {
            "id": busca_projeto.ID,
            "nome_projeto": busca_projeto.Nome,
            "descricao": busca_projeto.Descricao,
            "id_coordenador": busca_projeto.CoordenadorID
        }
        
        return jsonify(projeto)
    
    return {"status": False, "Erro": "Projeto não encontrado"}


@app.route('/projeto/<int:id_projeto>/formularios')
def get_projeto_formularios(id_projeto):
    
    busca_projeto = Projetos.query.get(id_projeto)
    
    formularios = []
    
    if busca_projeto:
        busca_formularios = Formularios.query.filter_by(ProjetoID=Projetos.ID).all()
        
        for item_formulario in busca_formularios:
            
            formulario = {
                "id": item_formulario.ID,
                "id_coordenador": item_formulario.CoordenadorID,
                "nome_formulario": item_formulario.Nome,
                "descricao": item_formulario.Descricao,
                "formula": item_formulario.Formula
            }
            
            formularios.append(formulario)        
        return jsonify(formularios)
    return {"status": False, "erro": "Projeto não encontrado"}

@app.route('/projeto/<int:id_projeto>/formulario/<int:id_formulario>')
def get_projeto_formulario(id_projeto, id_formulario):
    
    busca_projeto = Projetos.query.get(id_projeto)
    
    if busca_projeto:
        busca_formulario = Formularios.query.filter_by(ID=id_formulario, ProjetoID=Projetos.ID).first()
        
        formulario = {
            "id_coordenador": busca_formulario.CoordenadorID,
            "nome_formulario": busca_formulario.Nome,
            "descricao": busca_formulario.Descricao,
            "formula": busca_formulario.Formula
        }
                    
        return jsonify(formulario)
    return {"status": False, "erro": "Projeto não encontrado"}

@app.route('/formulario/<int:id_formulario>/perguntas')
def get_perguntas_formulario(id_formulario):
     
    resultados = db.session.query(
        Perguntas.ID,
        Perguntas.Tipo,
        Perguntas.Texto,
        Perguntas.VariavelAssociacao
    ).join(FormularioPerguntas, FormularioPerguntas.PerguntaID == Perguntas.ID) \
    .filter(FormularioPerguntas.FormularioID == id_formulario).all()

    if resultados:
        
        perguntas = []
        
        for resultado in resultados:
            pergunta = {
                "id": resultado.ID,
                "tipo": resultado.Tipo,
                "texto": resultado.Texto,
                "variavel_associacao": resultado.VariavelAssociacao
            }
            
            perguntas.append(pergunta)
        return jsonify(perguntas)
    return {"status": False, "erro": "Erro ao encontrar formulario"}

@app.route('/formulario/<int:id_formulario>/pergunta/<int:id_pergunta>')
def get_pergunta_formulario(id_formulario, id_pergunta):
     
    pergunta = db.session.query(
        Perguntas.ID,
        Perguntas.Tipo,
        Perguntas.Texto,
        Perguntas.VariavelAssociacao
    ).join(FormularioPerguntas, FormularioPerguntas.PerguntaID == Perguntas.ID) \
     .filter(FormularioPerguntas.FormularioID == id_formulario, Perguntas.ID == id_pergunta).first()

    if pergunta:
        
        pergunta_data = {
            "ID": pergunta.ID,
            "Tipo": pergunta.Tipo,
            "Texto": pergunta.Texto,
            "VariavelAssociacao": pergunta.VariavelAssociacao
        }

        return jsonify(pergunta_data)
    return {"status": False, "erro": "Pergunta ou formulário não encontrado"}

@app.route('/criar-projeto', methods=['POST'])
def criar_projeto():
    try:
        data = request.get_json()
        
        campos_obrigatorios = ['nome_projeto', 'descricao', 'id_coordenador']

        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({"status": False, "erro": f"Dados inválidos: Campo '{campo}' é obrigatório."}), 400

        novo_projeto = Projetos(
            Nome=data['nome_projeto'],
            Descricao=data['descricao'],
            CoordenadorID=data['id_coordenador']
        )
        
        db.session.add(novo_projeto)
        db.session.commit()
        
        return jsonify({"status": True}), 201  
    
    except Exception as e:
        db.session.rollback()  
        return jsonify({"status": False, "erro": str(e)}), 500
    
@app.route('/criar-formulario', methods=['POST'])
def criar_formulario():
    try:
        data = request.get_json()
        
        campos_obrigatorios = ['nome_formulario', 'descricao', 'id_projeto', 'id_coordenador']
        
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({"status": False, "erro": f"Dados inválidos: Campo '{campo}' é obrigatório."}), 400

        novo_formulario = Formularios(
            Nome=data['nome_formulario'],
            Descricao=data['descricao'],
            ProjetoID=data['id_projeto'],
            CoordenadorID=data['id_coordenador'],
            Formula=data.get('formula')  # Opcional
        )

        db.session.add(novo_formulario)
        db.session.commit()

        return jsonify({"status": True}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": False, "erro": str(e)}), 500
    
@app.route('/criar-pergunta', methods=['POST'])
def criar_perguntas():
    try:
        data = request.get_json()
        
        campos_obrigatorios = ['tipo', 'texto', 'variavel_associacao', 'id_formulario']
        
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({"status": False, "erro": f"Dados inválidos: Campo '{campo}' é obrigatório."}), 400
            
        pesquisa = Formularios.query.get(data['id_formulario'])
        
        if not pesquisa:
            return jsonify({"status": False, "erro": "Formulario não encontrado"})
        
        nova_pergunta = Perguntas(
            Tipo=data['tipo'],
            Texto=data['texto'],
            VariavelAssociacao=data['variavel_associacao']
        )
        
        db.session.add(nova_pergunta)
        db.session.commit()
        
        id_pergunta = nova_pergunta.ID
        
        novo_FormularioPerguntas = FormularioPerguntas(
            FormularioID=data['id_formulario'],
            PerguntaID=id_pergunta
        )
        
        db.session.add(novo_FormularioPerguntas)
        db.session.commit()
        
        return jsonify({"status": True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": False, "erro": str(e)}), 500