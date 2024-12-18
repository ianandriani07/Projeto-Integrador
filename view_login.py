from app import app, login_manager, db
from forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, redirect, url_for, flash, session, request, json, jsonify
from models import Usuarios
from helpers import generate_bcrypt_password

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return "<h1>Usuário logado</h1>"
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = Usuarios.query.filter_by(Usuario=username).first()
        
        if user and user.verify_password(password):
            
            login_user(user)
            session['user'] = user.Usuario
            print(user.Usuario)
            return redirect(url_for('hub'))         
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    if register.validate_on_submit():
        username = register.username.data
        password = register.password.data
        user = Usuarios.query.filter_by(Usuario=username).first()
        
        if user:
            return "<h1>Usuário já existente</h1>"
        
        
        senha_encriptada = generate_bcrypt_password(password)
        novo_usuario = Usuarios(Usuario=username, Senha=senha_encriptada)
        
        db.session.add(novo_usuario)
        db.session.commit()
        return """<h1>Usuário cadastrado com sucesso!</h1>
                <a href="{{ url_for('login') }}"></a>"""
    return render_template('register.html', form=register)

@app.route('/criar-usuario', methods=['POST'])
def criar_usuario():
    
    try:
        data = request.json
        campos = ['usuario', 'senha']
        campos_faltando = [campo for campo in campos if campo not in data or data[campo] is None]
            
        if campos_faltando:
            return jsonify({
                "status": False,
                "erro": f"Os seguintes campos estão faltando ou nulos: {', '.join(campos_faltando)}"
            }), 400
            
        usuario = data['usuario']
        senha = data['senha']
        
        user = Usuarios.query.filter_by(Usuario=usuario).first()
        
        if user:
            return jsonify({
                "status": False,
                "erro": "Usuário já registrado."
            }), 400
            
        senha_encriptada = generate_bcrypt_password(senha)
        novo_usuario = Usuarios(Usuario=usuario, Senha=senha_encriptada)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        return jsonify({
            "status": True,
            "mensagem": "Usuário criado com sucesso!"
        }), 201
        
    except Exception as e:
        return jsonify({
            "status": False,
            "erro": str(e)
        }), 500
    
@login_required
@app.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    return redirect(url_for('login'))
