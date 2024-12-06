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

    def get_id(self):
        return self.IdUsuario


class Formularios(db.Model):
    __tablename__ = 'formularios'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    ativo = db.Column(db.Boolean, default=True)
    formula = db.Column(db.Text)

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
    nome_variavel = db.Column(db.String(50), nullable=False)
    formula = db.Column(db.Text, nullable=True)

    opcoes = db.relationship('Opcoes', backref='pergunta', cascade='all, delete-orphan')


class Opcoes(db.Model):
    __tablename__ = 'opcoes'
    id = db.Column(db.Integer, primary_key=True)
    id_pergunta = db.Column(db.Integer, db.ForeignKey('perguntas.id', ondelete="CASCADE"), nullable=False)
    texto = db.Column(db.String(255), nullable=False)
    ordem = db.Column(db.Integer)
    pontuacao = db.Column(db.Integer, nullable=False, default=0)


class NumeroResposta(db.Model):
    __tablename__ = 'NumeroResposta'
    IdNumeroResposta = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Renomeie o backref para algo como 'respostas_rel'
    respostas = db.relationship('Respostas', backref='numero_resposta_rel', cascade='all, delete-orphan')
    
class Respostas(db.Model):
    __tablename__ = 'Respostas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_variavel = db.Column(db.String(255), nullable=False)
    valor_resposta = db.Column(db.Text, nullable=True)
    numero_resposta = db.Column(db.Integer, db.ForeignKey('NumeroResposta.IdNumeroResposta', ondelete="CASCADE"))


class RespostasPerguntas(db.Model):
    __tablename__ = 'respostas_perguntas'
    id = db.Column(db.Integer, primary_key=True)
    id_resposta = db.Column(db.Integer, db.ForeignKey('Respostas.id', ondelete="CASCADE"), nullable=False)
    id_pergunta = db.Column(db.Integer, db.ForeignKey('perguntas.id', ondelete="NO ACTION"), nullable=False)
    resposta_texto = db.Column(db.Text, nullable=True)  # Para perguntas objetivas
    id_opcao = db.Column(db.Integer, db.ForeignKey('opcoes.id'), nullable=True)  # Para perguntas de múltipla escolha

    opcao = db.relationship('Opcoes', backref='respostas_perguntas')