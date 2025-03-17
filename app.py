from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension # pip install flask-debugtoolbar
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_toastr import Toastr

from config import DATABASE_URL, SECRET_KEY

# Создание экземпляра приложения Flask и настройка его основных параметров
# и подключения к базе данных
app = Flask(__name__)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

# Задание секретного ключа для защиты сессий
app.config['SECRET_KEY'] = SECRET_KEY

app.config['TOASTR_POSITION_CLASS'] = 'toast-bottom-left'
app.config['TOASTR_TIMEOUT'] = 3000
app.config['DEBUG_TB_ENABLED'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Инициализация базы данных
db = SQLAlchemy(app)

# Инициализация менеджера логина
manager = LoginManager(app)
toastr = Toastr(app)
toolbar = DebugToolbarExtension(app)
