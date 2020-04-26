from flask_admin import Admin, AdminIndexView, expose, helpers
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_babelex import Babel
from flask import session, url_for, request, redirect
from app import app, db
from .models import User, Event
from .forms import AdminLoginForm, AdminSignupForm

def init_babel():
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        if request.args.get('lang'):
            session['lang'] = request.args.get('lang')
        return session.get('lang', 'ru')

def init_login_manager():
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

class AdminView(AdminIndexView):

    @expose('/')
    def admin_index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        elif current_user.is_authenticated and not current_user.is_superuser:
            return redirect('/')
        return super(AdminView, self).index()  

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = AdminLoginForm(request.form)
        if form.validate_on_submit():
            user = form.get_user()
            login_user(user)
        if current_user.is_authenticated and not current_user.is_superuser:
            return redirect('/')
        elif current_user.is_authenticated and current_user.is_superuser:
            return redirect(url_for('.admin_index'))
        link = '<p>Если Вы ещё не зарегистрированы, то вам стоит <a href="' + url_for('.signup_view') + '">зарегистрироваться</a>.</p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(AdminView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def signup_view(self):
        form = AdminSignupForm(request.form)
        if form.validate_on_submit():
            user = User()
            user.username = form.login.data
            user.set_password(form.password.data)
            user.email = form.email.data
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('.admin_index'))
        link = '<p>Если Вы уже зарегистрированы, то Вы можете <a href="' + url_for('.login_view') + '">войти</a>.</p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(AdminView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.admin_index'))

def init_admin():
    admin = Admin(app, 'Админка', index_view=AdminView(), base_template='admin.html', template_mode='bootstrap3')
    admin.add_view(MyModelView(User, db.session, name='Пользователи'))
    admin.add_view(MyModelView(Event, db.session, name='События'))