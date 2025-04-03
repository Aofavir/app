import datetime

from flask import Flask
from flask_login import LoginManager

from data import db_session

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init("db/blogs.db")

login_manager = LoginManager()
login_manager.init_app(app)