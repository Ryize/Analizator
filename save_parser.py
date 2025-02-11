"""Сохранение статей в БД"""

from app import db
from models import Article
from parser import ParsNews


class Save_Parser_BD:
    def __init__(self, articles: list):
        self.articles = articles

    def save_pars(self):
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
