"""Сохранение статей в БД"""

from app import db
from models import Article, GoldBD


class SaveParserBD:
    """
    Класс SaveParserBD

    Класс для сохранения в БД Article;
    """
    def __init__(self, articles: list):
        self.articles = articles

    def save_pars(self):

        # Сохраняет статьи в БД
        for article in self.articles:
            # Проверяем, не добавлена ли эта статья ранее в БД
            if Article.query.filter_by(title=article).first():
                continue

            # Если статья не добавлена ранее, то:
            # Создаем новую запись в таблице Article с указанным заголовком
            article_db = Article(title=article)
            # Добавляем статью в БД
            db.session.add(article_db)
            # прошу не обращать внимания на этот принт при ревью
            print(f'Сохраняем статью в БД: {article}')
        # Сохраняем изменения в БД
        db.session.commit()


class SaveGoldBD:
    """
    Класс SaveParserBD

    Класс для сохранения в БД GoldBD;
    """
    def __init__(self, info_list: list):
        self.info_list = info_list

    def save_pars(self):
        # Сохраняет статьи в БД
        for data in self.info_list:
            # Проверяем, не добавлена ли эта статья ранее в БД
            if GoldBD.query.filter_by(title=data).first():
                continue

            # Если информация не добавлена ранее, то:
            # Создаем новую запись в таблице GoldBD
            data_db = GoldBD(title=data)
            # Добавляем статью в БД
            db.session.add(data_db)
            # прошу не обращать внимания на этот принт при ревью
            print(f'Сохраняем информацию о золоте в БД: {data}')
        # Сохраняем изменения в БД
        db.session.commit()
