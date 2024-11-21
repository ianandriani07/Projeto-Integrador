import bcrypt
from sqlalchemy import func

def check_password_hash(stored_hash, provided_password):
    stored_hash_bytes = stored_hash.encode('utf-8')
    provided_password_bytes = provided_password.encode('utf-8')

    return bcrypt.checkpw(provided_password_bytes, stored_hash_bytes)

def generate_bcrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def get_id_tipos_pergunta(tipo):
    from models import TiposPerguntas
    tipo = TiposPerguntas.query.filter_by(descricao=tipo).first()
    
    if tipo:
        id_tipo = tipo.id
        return id_tipo
    return 0

def get_max_ordem():
    from models import Perguntas
    maior_ordem = Perguntas.query.with_entities(func.max(Perguntas.ordem)).scalar()
    
    if maior_ordem is None:
        return 0
    return maior_ordem

def verificar_id_formulario(id_formulario):
    from models import Formularios
    formulario = Formularios.query.get(id_formulario)
    
    if formulario:
        return True
    return False

def verificar_nome_variavel_pergunta(nome_variavel):
    from models import Perguntas
    perguntas = Perguntas.query.filter_by(nome_variavel=nome_variavel).first()
    
    if not perguntas:
        return True
    return False