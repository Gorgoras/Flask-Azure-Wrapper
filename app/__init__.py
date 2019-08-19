from flask import Flask, session
from config import Config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from app.forms import LoginForm
import os

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
bootstrap = Bootstrap(app=app)
app.secret_key = os.urandom(24)

from app import routes