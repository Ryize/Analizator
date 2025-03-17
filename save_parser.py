"""Сохранение статей в БД"""

from app import db
from models import Article, GoldBD


class SaveParserBD:
    def __init__(self, articles: list):
        self.articles = articles

    def save_pars(self):
        # """Очищаем БД"""
        # Article.query.delete()  # Очищаем таблицу Article
        # db.session.commit()  # Сохраняем изменения в БД

        """Сохраняет статьи в БД"""
        for article in self.articles:
            # Проверяем, не добавлена ли эта статья ранее в БД
            if Article.query.filter_by(title=article).first():
                continue

            # Если статья не добавлена ранее, то добавляем ее в БД
            print(f'Сохраняем статью в БД: {article}')
            # Создаем новую запись в таблице Article с указанным заголовком
            article_db = Article(title=article)
            # Добавляем статью в БД
            db.session.add(article_db)
        # Сохраняем изменения в БД
        db.session.commit()


class SaveGoldBD:
    def __init__(self, info_list: list):
        self.info_list = info_list

    def save_pars(self):
        # """Очищаем БД"""
        # Article.query.delete()  # Очищаем таблицу Article
        # db.session.commit()  # Сохраняем изменения в БД

        """Сохраняет статьи в БД"""
        for data in self.info_list:
            # Проверяем, не добавлена ли эта статья ранее в БД
            if GoldBD.query.filter_by(title=data).first():
                continue

            # Если информация не добавлена ранее, то добавляем ее в БД
            print(f'Сохраняем информацию о золоте в БД: {data}')
            # Создаем новую запись в таблице GoldBD
            data_db = GoldBD(title=data)
            # Добавляем статью в БД
            db.session.add(data_db)
        # Сохраняем изменения в БД
        db.session.commit()
