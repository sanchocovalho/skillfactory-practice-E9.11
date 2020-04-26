from flask import Flask
from config import Config
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__)
app.config.from_object(Config)
CSRFProtect(app)
db = SQLAlchemy(app)
Migrate(app, db)

from app.admin import init_babel, init_login_manager, init_admin
init_babel()
init_login_manager()
init_admin()

@app.template_filter('datetime')
def format_datetime(value, format="%d-%m-%Y %H:%M"):
    if value is None:
        return ""
    return value.strftime(format)

@app.template_filter('truncatechars')
def truncatechars(text, chars=500):
    if text is None:
        return ""
    if len(text) <= chars:
        return text
    else:
        return text[:chars] + "..."

from app import routes, models, forms
