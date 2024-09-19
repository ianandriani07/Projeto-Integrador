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
