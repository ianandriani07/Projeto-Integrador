from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[InputRequired()])
    password = PasswordField("Senha", validators=[InputRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Usuário", validators=[InputRequired()], render_kw={"placeholder": "Usuário"})
    password = PasswordField("Senha", validators=[InputRequired()], render_kw={"placeholder": "Senha"})
    submit = SubmitField("Register")