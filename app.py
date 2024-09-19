from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'AgiotechDominandoOMundo'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from view_login import *
from views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)