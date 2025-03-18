Analizator
Сайт для анализа рынка криптовалюты и золота.

Использованные технологии: 
![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
<br>
    

Прежде всего:
Установите Python (если он не установлен)
Скачать Python3


Клонируйте репозиторий и перейдите в установленную папку:

git clone https://github.com/Ryize/Analizator.git

cd Analizator

Установите requirements:
pip3 install -r requirements.txt

Далее вам необходимо создать файл config.py и указать информацию в формате:

# для БД (в данном случае sqlite), у вас может быть любая БД
DATABASE_URI = 'sqlite:///ваши данные'
# ваша почта с которой будет отправляться письмо для проверки email нового пользователя
EMAIL_LOGIN = 'ваша почта'
# Пароль для внешних приложений вашего почтового сервиса (например mail.ru)
EMAIL_PASSWORD = 'ваши данные'
# ключ flask_login LoginManager
SECRET_KEY = "ваши данные"
Тепепрь можно запустить проект командой:

python3 main.py

Описание проекта:
На главной странице вам предоставляется выбрать пункты - Зотоло, с курсами золота на настоящий момент, или пункт - Крипто, в котором, gpt даст вам свой прогноз стоимости биткойна на основе последних новостей.
