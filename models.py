"""Модуль с моделями БД"""

from datetime import datetime
from flask_login import UserMixin

from app import db, app, manager


# Создание и описание модели для пользователей
class User(db.Model, UserMixin):
    """
    Класс объекта БД

    Класс для сохранения в БД данных нового зарегистрированного пользователя:
    id клиента, email, имя, пароль для авторизации, подтверждение проверки
    email, дата и время внесения данных в БД;
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(48), unique=True)
    login = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(64))

    # Поле для хранения статуса подтверждения email
    email_confirm = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Создание и описание модели для подтверждения email
class EmailConfirm(db.Model):
    """
    Класс объекта БД

    Класс для сохранения в БД сгенерированного кода для проверки email нового
    зарегистрированного пользователя;
    """
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    code = db.Column(db.String(33), unique=True, nullable=False)


# Создание модели для хранения статьи
class Article(db.Model):
    """
    Класс объекта БД

    Класс для сохранения в БД заголовков новостей;
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Создание модели для хранения информации по курсу золота
class GoldBD(db.Model):
    """
    Класс объекта БД

    Класс для сохранения в БД курсов золота;
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Создание БД, добавить всё
with app.app_context():
    db.create_all()


# Загрузка пользователя из БД
@manager.user_loader
def load_user(user_id: int) -> int:
    """
        Выгрузка из БД

        Загрузка пользователя из БД;

        Args:
            user_id: int (первый параметр)

        Returns:
            int: id пользователя
    """
    return User.query.get(user_id)
