from app import db
from flask_login import UserMixin
from helpers import check_password_hash

class Usuarios(db.Model, UserMixin):
    __tablename__ = 'Usuarios'
    IdUsuario = db.Column(db.Integer, primary_key=True)
    Usuario = db.Column(db.String(255), nullable=False)
    Senha = db.Column(db.String(255), nullable=False)
    
    def verify_password(self, password):
        return check_password_hash(self.Senha, password)

    # Flask-Login espera que get_id retorne o identificador do usuário
    def get_id(self):
        return self.IdUsuario

class Formularios(db.Model):
    __tablename__ = 'formularios'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    ativo = db.Column(db.Boolean, default=True)
    formula = db.Column(db.Text)  # Campo adicionado para armazenar a fórmula do formulário

    perguntas = db.relationship('Perguntas', backref='formulario', cascade='all, delete-orphan')

class TiposPerguntas(db.Model):
    __tablename__ = 'tipos_perguntas'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), nullable=False)

    perguntas = db.relationship('Perguntas', backref='tipo')


class Perguntas(db.Model):
    __tablename__ = 'perguntas'
    id = db.Column(db.Integer, primary_key=True)
    id_formulario = db.Column(db.Integer, db.ForeignKey('formularios.id', ondelete="CASCADE"), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipos_perguntas.id'), nullable=False)
    ordem = db.Column(db.Integer)
    obrigatoria = db.Column(db.Boolean, default=False)
    nome_variavel = db.Column(db.String(50), nullable=False)  # Novo campo adicionado

    opcoes = db.relationship('Opcoes', backref='pergunta', cascade='all, delete-orphan')

class Opcoes(db.Model):
    __tablename__ = 'opcoes'
    id = db.Column(db.Integer, primary_key=True)
    id_pergunta = db.Column(db.Integer, db.ForeignKey('perguntas.id', ondelete="CASCADE"), nullable=False)
    texto = db.Column(db.String(255), nullable=False)
    ordem = db.Column(db.Integer)


class Respostas(db.Model):
    __tablename__ = 'respostas'
    id = db.Column(db.Integer, primary_key=True)
    id_formulario = db.Column(db.Integer, db.ForeignKey('formularios.id', ondelete="CASCADE"), nullable=False)
    id_usuario = db.Column(db.Integer)  # Campo opcional para rastrear quem respondeu
    data_resposta = db.Column(db.DateTime, default=db.func.current_timestamp())

    respostas_perguntas = db.relationship('RespostasPerguntas', backref='resposta', cascade='all, delete-orphan')


class RespostasPerguntas(db.Model):
    __tablename__ = 'respostas_perguntas'
    id = db.Column(db.Integer, primary_key=True)
    id_resposta = db.Column(db.Integer, db.ForeignKey('respostas.id', ondelete="CASCADE"), nullable=False)
    id_pergunta = db.Column(db.Integer, db.ForeignKey('perguntas.id', ondelete="NO ACTION"), nullable=False)
    resposta_texto = db.Column(db.Text)  # Para perguntas objetivas
    id_opcao = db.Column(db.Integer, db.ForeignKey('opcoes.id'))  # Para perguntas de múltipla escolha

    opcao = db.relationship('Opcoes', backref='respostas_perguntas')