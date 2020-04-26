import sys
from getpass import getpass
from flask_script import Command
from email_validator import validate_email, EmailNotValidError
from .models import User

class CreateSuperUser(Command):
    def __init__(self, db):
        super(CreateSuperUser, self).__init__()
        self.db = db

    def run(self):
        print("Форма создания аккаунта администратора")
        try:
            while True:
                username = input("Введите логин администратора (не менее 5 символов): ")
                if len(username) < 5:
                    print('Пароль слишком короткий!')
                    continue
                elif len(username) > 48:
                    print('Пароль слишком длинный!')
                    continue
                elif User.query.filter_by(username=username).count() > 0:
                        print('Такой аккаунт уже существует!')
                        continue
                else:
                    break
            while True:
                superuser_password1 = getpass("Введите пароль администратора (не менее 5 символов): ")
                if len(superuser_password1) < 5:
                    print('Пароль слишком короткий!')
                    continue
                elif len(superuser_password1) > 32:
                    print('Пароль слишком длинный!')
                    continue
                superuser_password2 = getpass("Повторите пароль администратора (не менее 5 символов): ")
                if len(superuser_password2) < 5:
                    print('Пароль слишком короткий!')
                    continue
                elif len(superuser_password2) > 32:
                    print('Пароль слишком длинный!')
                    continue
                elif superuser_password1 != superuser_password2:
                    print('Пароли не совпали! Пробуйте ещё.')
                    continue
                else:
                    break
            while True:
                superuser_email = input("Введите email администратора: ")
                if len(superuser_email) > 64:
                    print('Email слишком длинный!')
                    continue
                is_valid = False
                try:
                    valid = validate_email(superuser_email)
                    superuser_email = valid['email']
                    is_valid = True
                except EmailNotValidError as e:
                    pass
                if not is_valid:
                    print('Что-то непохоже на email!')
                    continue
                else:
                    break
            admin = User()
            admin.username = username
            admin.set_password(superuser_password1)
            admin.email = superuser_email
            admin.is_superuser = True
            self.db.session.add(admin)
            self.db.session.commit()
            print("Аккаунт администратора создан.")
        except:
            print("Невозможно создать аккаунт администратора.")
            print("Возможно необходимо применить миграции к БД.")
        return 0