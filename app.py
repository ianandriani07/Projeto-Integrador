from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os
from webpack_boilerplate.config import setup_jinja2_ext


app = Flask(__name__, static_folder="static/build", static_url_path="/static/")
app.config.from_object(Config)
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = "AgiotechDominandoOMundo"

app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config.update(
    {
        "WEBPACK_LOADER": {
            "MANIFEST_FILE": "./static/build/manifest.json",
        }
    }
)
setup_jinja2_ext(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

from view_login import *
from views import *


@app.cli.command("webpack_init")
def webpack_init():
    from cookiecutter.main import cookiecutter
    import webpack_boilerplate

    pkg_path = os.path.dirname(webpack_boilerplate.__file__)
    cookiecutter(pkg_path, directory="frontend_template")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
