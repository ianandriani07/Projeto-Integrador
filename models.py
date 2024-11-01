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

class Coordenadores(db.Model):
    __tablename__ = 'Coordenadores'
    ID = db.Column(db.Integer, primary_key=True)
    IdUsuario = db.Column(db.Integer, db.ForeignKey('Usuarios.IdUsuario', ondelete="CASCADE"), nullable=False)
    Nome = db.Column(db.String(100), nullable=False)

    usuario = db.relationship('Usuarios', backref=db.backref('coordenador', uselist=False))

class Alunos(db.Model):
    __tablename__ = 'Alunos'
    ID = db.Column(db.Integer, primary_key=True)
    IdUsuario = db.Column(db.Integer, db.ForeignKey('Usuarios.IdUsuario', ondelete="CASCADE"), nullable=False)
    Nome = db.Column(db.String(100), nullable=False)

    usuario = db.relationship('Usuarios', backref=db.backref('aluno', uselist=False))

class Projetos(db.Model):
    __tablename__ = 'Projetos'
    ID = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(100), nullable=False)
    Descricao = db.Column(db.Text)
    CoordenadorID = db.Column(db.Integer, db.ForeignKey('Coordenadores.ID', ondelete="SET NULL"))

    coordenador = db.relationship('Coordenadores', backref='projetos')

class Formularios(db.Model):
    __tablename__ = 'Formularios'
    ID = db.Column(db.Integer, primary_key=True)
    ProjetoID = db.Column(db.Integer, db.ForeignKey('Projetos.ID', ondelete="CASCADE"), nullable=False)
    CoordenadorID = db.Column(db.Integer, db.ForeignKey('Coordenadores.ID', ondelete="SET NULL"))
    Nome = db.Column(db.String(100), nullable=False)
    Descricao = db.Column(db.Text)
    Formula = db.Column(db.Text)

    projeto = db.relationship('Projetos', backref='formularios')
    coordenador = db.relationship('Coordenadores', backref='formularios')

class Perguntas(db.Model):
    __tablename__ = 'Perguntas'
    ID = db.Column(db.Integer, primary_key=True)
    Tipo = db.Column(db.String(50), nullable=False)
    Texto = db.Column(db.Text, nullable=False)
    VariavelAssociacao = db.Column(db.String(50))
    Formula = db.Column(db.Text)

class FormularioPerguntas(db.Model):
    __tablename__ = 'FormularioPerguntas'
    ID = db.Column(db.Integer, primary_key=True)
    FormularioID = db.Column(db.Integer, db.ForeignKey('Formularios.ID', ondelete="CASCADE"), nullable=False)
    PerguntaID = db.Column(db.Integer, db.ForeignKey('Perguntas.ID', ondelete="CASCADE"), nullable=False)

    formulario = db.relationship('Formularios', backref='perguntas_associadas')
    pergunta = db.relationship('Perguntas', backref='formularios_associados')

class OpcaoPergunta(db.Model):
    __tablename__ = 'OpcaoPergunta'
    ID = db.Column(db.Integer, primary_key=True)
    PerguntaID = db.Column(db.Integer, db.ForeignKey('Perguntas.ID', ondelete="CASCADE"), nullable=False)
    OpcaoTexto = db.Column(db.String(50), nullable=False)
    ValorNumerico = db.Column(db.Integer, nullable=False)

    pergunta = db.relationship('Perguntas', backref='opcoes')

class TiposReducao(db.Model):
    __tablename__ = 'TiposReducao'
    ID = db.Column(db.Integer, primary_key=True)
    Descricao = db.Column(db.String(50), nullable=False)

class Pacientes(db.Model):
    __tablename__ = 'Pacientes'
    ID = db.Column(db.Integer, primary_key=True)
    IdentificadorUnico = db.Column(db.String(50), unique=True, nullable=False)

class Respostas(db.Model):
    __tablename__ = 'Respostas'
    ID = db.Column(db.Integer, primary_key=True)
    PerguntaID = db.Column(db.Integer, db.ForeignKey('Perguntas.ID', ondelete="CASCADE"), nullable=False)
    PacienteID = db.Column(db.Integer, db.ForeignKey('Pacientes.ID', ondelete="CASCADE"), nullable=False)
    RespostaTexto = db.Column(db.Text)
    RespostaNumerica = db.Column(db.Integer)
    RespostaOpcao = db.Column(db.Integer, db.ForeignKey('OpcaoPergunta.ID'))
    ValorCalculado = db.Column(db.Float)

    pergunta = db.relationship('Perguntas', backref='respostas')
    paciente = db.relationship('Pacientes', backref='respostas')
    opcao = db.relationship('OpcaoPergunta', backref='respostas')

class AlunoProjeto(db.Model):
    __tablename__ = 'AlunoProjeto'
    ID = db.Column(db.Integer, primary_key=True)
    ProjetoID = db.Column(db.Integer, db.ForeignKey('Projetos.ID', ondelete="CASCADE"), nullable=False)
    AlunoID = db.Column(db.Integer, db.ForeignKey('Alunos.ID', ondelete="CASCADE"), nullable=False)
    DataAssociacao = db.Column(db.Date, default=db.func.current_date())
    StatusParticipacao = db.Column(db.String(50), default='Ativo')

    projeto = db.relationship('Projetos', backref='alunos')
    aluno = db.relationship('Alunos', backref='projetos')