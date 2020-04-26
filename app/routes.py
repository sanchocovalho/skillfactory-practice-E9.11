from datetime import datetime
from flask import render_template, request, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from .models import User, Event
from .forms import LoginForm, SignupForm, UserForm, EventForm

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    if not current_user.is_authenticated:
        loginform = LoginForm()
        signupform = SignupForm()
        return render_template('index.html', loginform=loginform, form=signupform)
    else:
        events = Event.query.all()
        return render_template('index.html', events=events)

@app.route("/login", methods=["GET", "POST"])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()
        if request.method == "POST":
            if form.validate_on_submit():
                user = User.query.filter_by(username=form.login_username.data).first()
                if user and user.check_password(form.login_password.data):
                    login_user(user, remember=True)
                else:
                    flash('Неверный логин или пароль!')
            else:
                flash('Введены некорректные данные!')
    return redirect('/')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if not current_user.is_authenticated:
        form = SignupForm()
        if request.method == "POST":
            if form.validate_on_submit():
                user = User.query.filter_by(username=form.signup_username.data).first()
                if not user:
                    user = User()
                    user.username = form.signup_username.data
                    user.email = form.signup_email.data
                    user.set_password(form.signup_password.data)
                    db.session.add(user)
                    db.session.commit()
                    flash('Вы успешно зарегистрированы!')
                else:
                    flash('Пользователь с таким именем уже существует!')  
            else:
                flash('Введены некорректные данные!')
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/user/<int:id>', methods=["GET", "POST"])
@login_required
def update_user(id):
    user = User.query.get(id)
    if current_user.username == user.username: 
        form = UserForm()
        if request.method == "POST":
            if form.validate_on_submit():
                user.email = form.email.data
                if form.firstname.data:
                    user.firstname = form.firstname.data
                if form.lastname.data:
                    user.lastname = form.lastname.data
                if form.password1.data:
                    if form.password1.data == form.password2.data:
                        user.set_password(form.password1.data)
                        db.session.add(user)
                        db.session.commit()
                        return redirect('/')
                    else:
                        flash('Пороли не совпадают!')
                else:
                    db.session.add(user)
                    db.session.commit()
                    return redirect('/')
            else:
                flash('Введены некорректные данные!')    
        return render_template('update_user.html', user=user, form=form)
    return redirect('/')

@app.route('/event/<int:id>')
@login_required
def event_detail(id):
    event = Event.query.get(id)
    return render_template('event_detail.html', event=event)

@app.route('/create_event', methods=["GET", "POST"])
@login_required
def create_event():
    form = EventForm()
    if request.method == "POST":
        if form.validate_on_submit():
            event = Event()
            event.title = form.title.data
            event.description = form.description.data
            event.author = current_user.username
            try:
                event.start_time = datetime.strptime(form.start_time.data, '%d-%m-%Y %H:%M')
                event.end_time = datetime.strptime(form.end_time.data, '%d-%m-%Y %H:%M')
            except:
                flash('Введены некорректные значения даты!')
            else:
                db.session.add(event)
                db.session.commit()
                return redirect(f'/event/{event.id}')
        else:
            flash('Введены некорректные данные!')
    return render_template('create_event.html', form=form)

@app.route('/update_event/<int:id>', methods=['GET', 'POST'])
@login_required
def update_event(id):
    event = Event.query.get(id)
    if current_user.username == event.author:
        form = EventForm()
        if request.method == "POST":
            if form.validate_on_submit():
                event.title = form.title.data
                event.description = form.description.data
                try:
                    event.start_time = datetime.strptime(form.start_time.data, '%d-%m-%Y %H:%M')
                    event.end_time = datetime.strptime(form.end_time.data, '%d-%m-%Y %H:%M')
                except:
                    flash('Введены некорректные значения даты!')
                else:
                    db.session.add(event)
                    db.session.commit()
                    return redirect(f'/event/{event.id}')
            else:
                flash('Введены некорректные данные!')       
        return render_template ('update_event.html', event=event, form=form)
    return redirect('/')

@app.route('/delete_event/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_event(id):
    event = Event.query.get(id)
    if current_user.username == event.author:
        if request.method == "POST":
            db.session.delete(event)
            db.session.commit()
            return redirect('/')
        form = EventForm()
        return render_template ('delete_event.html', event=event, form=form)
    return redirect('/')