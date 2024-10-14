from app import app, login_manager, db
from flask import render_template, redirect, url_for, flash, session

@app.route('/')
def inicio():
    return redirect(url_for('login'))

@app.route('/hub', methods=['GET', 'POST'])
def hub():
    return render_template('hub.html')