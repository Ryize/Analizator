""" Получение данных (парсинг) о стоимости золота с сайта investzoloto.ru"""

import requests
from bs4 import BeautifulSoup

from parser_news import Parser


class ParsGold(Parser):
    """
    Класс объекта Parser

    Класс для парсинга курса золота;
    """
    def __init__(self):
        self.url = "https://investzoloto.ru/kurs_zoloto/"

    def pars(self):
        lst_news = list()
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'lxml')
        teg_div_innercontent = soup.find("div", id="innercontent")

        teg_b = teg_div_innercontent.find_all("b")
        cb_curs = f'Курс золота Центробанка на сегодня: {teg_b[7].text} за грамм.'  # строка
        lst_news.append(cb_curs)

        teg_li = teg_div_innercontent.find_all("li")  # список!
        for i in teg_li:
            lst_news.append(i.text)

        return lst_news


