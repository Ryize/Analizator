import string
import random

from flask import render_template, request, redirect, url_for, session, flash, make_response
from flask_login import logout_user, login_required, login_user, current_user
from flask.wrappers import Response

from mail import send_email
from app import app, db
from business_logic.check_fata import check_auth_data
from models import User, EmailConfirm



@app.route('/email-confirm/<code>')
# Функция для подтверждения email
def email_confirm(code: int) -> Response or str:
    """
        Подтверждение email

        Проверяем, существует ли подтверждение в БД
        Если подтверждение существует, то удаляем его из БД
        и меняем статус email_confirm у пользователя в БД
        Если подтверждение не существует,
        то перенаправляем на страницу регистрации;

        Args:
            code: int (код подтверждения)

        Returns:
            str: шаблон страницы 500.html
            Response: перенаправление на страницу register
    """

    # Проверяем, существует ли подтверждение с таким кодом в БД
    user_confirm = EmailConfirm.query.filter_by(code=code).first()
    # Если подтверждение существует, то удаляем его из БД
    # и меняем статус email_confirm у пользователя в БД
    if user_confirm:
        # Ищем пользователя в БД по логину,
        # соответствующему логину в подтверждении
        user = User.query.filter_by(login=user_confirm.login).first()
        # Если пользователь найден, то меняем его статус email_confirm
        # на True
        user.email_confirm = True
        # Добавляем пользователя в БД
        db.session.add(user)
        # Удаляем пользователя из БД
        db.session.delete(user_confirm)
        # Сохраняем изменения в БД
        db.session.commit()
    # Отправляем подтверждение на указанный email
    return redirect(url_for('register'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
# Функция регистрации нового пользователя
def register() -> str:
    """
       Страница регистрации

       Пользователь переходит на страницу регистрации, вводит данные,
       нажимает кнопку "Регистрация", и если данные корректны,
       регистрируется новый пользователь в БД;

       Returns:
           str: шаблон страницы 500.html или register.html
    """

    # Если это POST-запрос, значит была нажата кнопка "Регистрация"
    if request.method == 'POST':
        # Получаем данные из формы регистрации
        email = request.form.get('email')
        username = request.form.get('login')
        password = request.form.get('password')
        print(email, username, password)

        # Проверяем корректность введенных данных
        if check_auth_data(username, password):
            # Создаем нового пользователя
            user = User(email=email, login=username, password=password)
            # Создаем код подтверждения email, состоящий
            # из 32 символов (латинских букв и цифр)
            code = ''.join(
                [random.choice(string.ascii_letters + string.digits)
                 for i in range(32)])
            # Создаем новую запись в таблице EmailConfirm
            # с указанным кодом и логином
            user_confirm = EmailConfirm(login=username, code=code)
            # print(f'Успешная регистрация! {user.email}, {user.password}')

            # Формируем сессии для последующего добавления в БД
            db.session.add(user)
            # Сохранение в базу данных всех сформированных сессий одним
            # комитом
            db.session.add(user_confirm)
            # Сохранение в базу данных всех сформированных сессий одним
            # комитом
            db.session.commit()

            # Отправляем письмо с сылкой для подтверждения почты
            message = (f'Ссылка для подтверждения '
                       f'почты: http://127.0.0.1:5000/email-confirm/'
                       f'{code}')
            # Отправляем письмо c сылкой на сервер
            send_email(message, email, 'Подтверждение почты')
            print(f'Успешная регистрация! {user.email}, {user.password}')
        else:
            print('Неверные данные при регистрации!')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
# Функция авторизации пользователя
def login() -> Response or str:
    """
       Страница авторизации

       Пользователь авторизуется, далее проверяет почту и пароль,
       если есть перенаправляет на главную страницу, если нет направляет на
       страницу регистрации;

       Returns:
           str: шаблон страницы index.html или register
    """

    # if request.method == 'GET':
    #     return render_template('login.html')

    # Проверка наличия введённых данных авторизации
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Чтение данных
        user = User.query.filter_by(email=email, password=password).first()

        # Проверка наличия пользователя в БД и наличие соответствующих
        # паролей
        if user and user.email_confirm:
            print(f'Успешная авторизация! {user.email}, {user.password}')
            # Выполняем логин пользователя
            login_user(user)
            # В случае успешной авторизации перенаправляем на главную
            # страницу
            return redirect(url_for('index'))
        # Если данные неверны, выводим сообщение "Ошибка авторизации"
        print('Ошибка авторизации!')
        # Если данные неверны, перенаправляем на страницу регистрации
        return render_template('register.html',)
        # return redirect(url_for('register'))
    return render_template('login.html')


# Обработчик главной страницы, показывает список всех пользователей
# и возвращает страницу с формой отправки сообщений
@app.route('/index')
@login_required
# Функция главной страницы
def index() -> str:
    """
       Главная страница

       Авторизованный пользователь переходит на главную страницу
       index.html.

       Returns:
           str: шаблон страницы index.html
       """
    return render_template('index.html')


@app.route('/logout')
@login_required
# Функция выхода из учётной записи и перенаправления на страницу регистрации
def logout() -> Response or str:
    """
       Разлогиниться

       Выход из учётной записи и перенаправление на страницу регистрации;

       Returns:
           str: шаблон страницы index.html
           Response: вызывает функцию register
   """

    # Выход из учётной записи и перенаправление на страницу регистрации
    logout_user()
    print('Вы вышли!')
    return redirect(url_for('login'))


# Перенаправляем на страницу регистрации при неправильной авторизации
@app.after_request
# Функция перенаправления на страницу регистрации при неправильной авторизации
def redirect_to_sign(response: Response) -> Response or str:
    """
        Обработка ошибки 401

        Returns:
            Response: вызывает функцию register
            str: шаблон страницы 500.html
    """

    # Если клиент авторизован, перенаправлять его не нужно
    if response.status_code == 401:
        return redirect(url_for('register'))
    return response