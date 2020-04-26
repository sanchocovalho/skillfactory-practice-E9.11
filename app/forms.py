from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.form import Form
from wtforms.fields.html5 import EmailField, DateTimeField
from wtforms.validators import DataRequired, required, Length, Email, ValidationError
from .models import User

class LoginForm(FlaskForm):
    login_username = StringField('Логин', validators=[DataRequired(), Length(min=5, max=48)])
    login_password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5, max=32)])

class SignupForm(FlaskForm):
    signup_username = StringField('Логин', validators=[DataRequired(), Length(min=5, max=48)])
    signup_password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5, max=32)])
    signup_email = EmailField('Email', validators=[DataRequired(), Email('')])

class UserForm(FlaskForm):
    firstname = StringField('Имя', validators=[Length(min=0, max=48)])
    lastname = StringField('Фамилия', validators=[Length(min=0, max=48)])
    password1 = PasswordField('Пароль1', validators=[Length(min=0, max=32)])
    password2 = PasswordField('Пароль2', validators=[Length(min=0, max=32)])
    email = EmailField('Email', validators=[DataRequired(), Email('')])

class EventForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(min=1, max=64)])
    description = TextAreaField('Описание')
    start_time = StringField('Начало события', validators=[DataRequired()])
    end_time = StringField('Конец события', validators=[DataRequired()])

class AdminLoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=5, max=48)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5, max=32)])

    def validate_login(self, field):
        user = self.get_user()
        if not user:
            raise ValidationError('Такого логина не существует!')
        if not user.check_password(self.password.data):
            raise ValidationError('Неверный пароль!')

    def get_user(self):
        return User.query.filter_by(username=self.login.data).first()

class AdminSignupForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=5, max=48)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5, max=32)])
    email = StringField('Email', validators=[DataRequired(), Email('')])

    def validate_login(self, field):
        if User.query.filter_by(username=self.login.data).count() > 0:
            raise ValidationError('Такой логин уже существует!')