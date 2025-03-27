"""Модуль с роутами"""

import random
import string

from flask import render_template, request, redirect, url_for, send_file
from flask.wrappers import Response
from flask_login import logout_user, login_required, login_user

from api_proxy import RequestProxyAPI
from app import app, db
from gruph_cripta import get_crypto_data, gruph_crypto_price
from mail import send_email
from models import User, EmailConfirm, Article, GoldBD
from parser_gold import ParsGold

from parser_news import all_source_news_lst
from price_cripta import get_crypto_prices, get_crypto_news
from save_parser import SaveParserBD, SaveGoldBD


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
    if not user_confirm:
        return redirect(url_for('register'))
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
    # авторизуем пользователя
    login_user(user)
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
# Функция регистрации нового пользователя
def register() -> Response or str:

    """
    Страница регистрации

    Пользователь переходит на страницу регистрации, вводит данные,
    нажимает кнопку "Регистрация", и если данные корректны,
    регистрируется новый пользователь в БД;

    Returns:
    str: шаблон страницы 500.html или register.html
    """

    # Если это POST-запрос, значит была нажата кнопка "Регистрация"
    if request.method == 'GET':
        return render_template('register.html')
    # Получаем данные из формы регистрации
    email = request.form.get('email')
    username = request.form.get('login')
    password = request.form.get('password')
    print(email, username, password)

    # Проверяем длину логина и пароля
    if not (3 < len(username) < 20) or not (4 < len(password) < 32):
        print('Неверный формат данных при регистрации!')
        return redirect(url_for('register'))

    # Создаем нового пользователя
    user = User(email=email, login=username, password=password)
    # Создаем код подтверждения email, состоящий
    # из 32 символов (латинских букв и цифр)
    code = ''.join(
        [random.choice(string.ascii_letters + string.digits)
         for _ in range(32)])
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
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
# Функция авторизации пользователя
def login() -> Response or str:
    """
    Страница авторизации
    Пользователь авторизуется, далее проверяет почту и пароль,
    если есть перенаправляет на главную страницу, если нет направляет на
    страницу регистрации;

    Пользователь авторизуется, далее проверяет почту и пароль,
    если есть перенаправляет на главную страницу, если нет направляет на
    страницу регистрации;

    Returns:
        str: шаблон страницы index.html или register
    """
    # Проверка наличия введённых данных авторизации
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('password')

    # Чтение данных
    user = User.query.filter_by(email=email, password=password).first()

    # Проверка наличия пользователя в БД и наличие соответствующих
    # паролей
    if user and user.email_confirm:
        print(f'Успешная авторизация! {user.email}, {user.password}')
        # Выполняем логинизацию (авторизацию) пользователя
        login_user(user)
        # В случае успешной авторизации перенаправляем на главную
        # страницу
        return redirect(url_for('index'))
    # Если данные неверны, выводим сообщение "Ошибка авторизации"
    print('Ошибка авторизации!')
    # Если данные неверны, перенаправляем на страницу регистрации
    return render_template('login.html')


# Обработчик главной страницы, показывает список всех пользователей
# и возвращает страницу с формой отправки сообщений
@app.route('/index', methods=['GET'])
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


@app.route('/download')
@login_required
def download_file() -> Response:
    """
    Переходим по роуту скачаем файл

    Авторизованный пользователь переходит по роуту
    и скачивает pdf файл с графиком

    Returns:
        str: pdf файл с графиком
    """
    return send_file('Figures.pdf', as_attachment=True)


@app.route('/cripta', methods=['GET', 'POST'])
@login_required
# Функция для перехода на страницу крипта
def cripta() -> str:
    """
    Страница с информацией о Крипте

    Авторизованный пользователь переходит на страницу крипта
    cripta.html и получает информацию

    Returns:
        str: шаблон страницы cripta.html
    """
    # Очищаем таблицу БД - Article
    Article.query.delete()
    # Сохраняем изменения в БД
    db.session.commit()

    # парсим все новости из полиморфного контейнера (из файла parser_news.py)
    for source_news in all_source_news_lst:
        get_news = source_news.pars()
        SaveParserBD(get_news).save_pars()

    # собираем данные с формы на странице (выбор криптовалюты)
    if request.method == 'POST':
        crypto = request.form.get('content')
        crypto_data = get_crypto_data(crypto)
        gruph_crypto_price(crypto_data, crypto)

    # получаем список цен на криптовалюту (файл price_cripta.py)
    prices = get_crypto_prices()
    # получение новостей с сайта www.block-chain24 (файл price_cripta.py)
    news = get_crypto_news()

    # с помощью класса RequestProxyAPI из файла api_proxy, и его метода
    # request_to_proxy_api, передаем для обработки в чат GPT заголовки
    # новостей (news), формируем ответ в переменной gpt_answer
    gpt_answer = RequestProxyAPI().request_to_proxy_api(news)

    # вывод на экран новостей с сайта www.block-chain24, для проверки
    # осознано оставил этот принт, прошу не обращать на него внимания при ревью
    for article in news:
        print(article, ';')

    # возвращаем страницу cripta.html с переменными с данными
    return render_template('cripta.html',
                           prices=prices,
                           news=news,
                           gpt_answer=gpt_answer)


@app.route('/gold', methods=['GET', 'POST'])
@login_required
# Функция для перехода на страницу /gold
def gold() -> str:
    """
    Страница с информацией о Золоте

    Авторизованный пользователь переходит на страницу крипта
    gold.html и получает информацию

    Returns:
        str: шаблон страницы gold.html
    """

    GoldBD.query.delete()  # Очищаем таблицу БД GoldBD
    db.session.commit()  # Сохраняем изменения в БД

    # создаем объект класса ParsGold
    pars_gold = ParsGold()
    # сохраняем в переменную результат метода .pars() созданного объекта класса
    new_data_pars_gold = pars_gold.pars()
    # создаем объект класса SaveGoldBD
    save_new_data_pars_gold = SaveGoldBD(new_data_pars_gold)
    # сохраняем данные в БД через метод .save_pars() созданного объекта класса;
    save_new_data_pars_gold.save_pars()

    data_about_gold = GoldBD.query.all()

    return render_template('gold.html', data=data_about_gold)


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
    # вывод на экран информационного сообщения
    print('Вы успешно разлогинились!')
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
