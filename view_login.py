from app import app, login_manager
from forms import LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, redirect, url_for, flash, session
from models import Usuarios

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

@app.route('/')
def inicio():
    return redirect(url_for('login'))

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
            return "<h1>Usuário logado!</h1>"
    
    return render_template('login.html', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    return redirect(url_for('login'))
