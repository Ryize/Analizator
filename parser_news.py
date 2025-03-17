"""Парсеры новостей"""

from abc import ABC, abstractmethod

from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


# Абстрактный класс
class Parser(ABC):
    """
    Абстрактный класс всех парсеров

    """

    # Абстрактный метод
    @abstractmethod
    def pars(self):
        pass


# Парсер www.block-chain24.com
class ParsBlock_Chain24(Parser):
    """
    Класс объекта Parser

    Класс для парсинга заголовков новостей;
    """
    def __init__(self):
        self.url_block_chain24 = "https://www.block-chain24.com/news?ysclid=m6ony52ur9108910355"

    def pars(self):
        html = requests.get(self.url_block_chain24).text
        soup = BeautifulSoup(html, 'lxml')
        page = soup.find_all('div', class_='row-cards__item card card_style-5')

        lst_news = []
        for i in page:
            link = i.find('a', href=True)
            if link is None:
                continue

            # links = 'https://www.block-chain24.com' + link['href']
            title = i.find('div', class_='card__title').text.strip()
            # news = i.find('div', class_='card__description').text.strip()

            lst_news.append(title)

        return lst_news


# Парсер www.ria.ru
class ParsRia_ru(Parser):
    """
    Класс объекта Parser

    Класс для парсинга заголовков новостей;
    """
    def __init__(self):
        # self.url_ria_ru = "https://ria.ru/economy/"
        self.url_ria_ru = 'https://ria.ru/economy+world/?ysclid=m6qcyuk5g7415845054'

    def pars(self):
        html = requests.get(self.url_ria_ru).text
        soup = BeautifulSoup(html, 'lxml')
        page = soup.find_all('div', class_='list-item__content')

        lst_news = []
        for i in page:
            link = i.find('a', href=True)
            if link is None:
                continue

            # links = 'https://ria.ru' + link['href']
            title = i.find('a', class_='list-item__title color-font-hover-only').text.strip()

            lst_news.append(title)

        return lst_news


# Парсер www.kommersant.ru
class ParsKommersant_ru(Parser):
    """
    Класс объекта Parser

    Класс для парсинга заголовков новостей;
    """
    def __init__(self):
        self.url_kommersant_ru = "https://www.kommersant.ru/theme/1984"

    def pars(self):
        html = requests.get(self.url_kommersant_ru).text
        soup = BeautifulSoup(html, 'lxml')
        page = soup.find_all('h2', class_='uho__name rubric_lenta__item_name')

        lst_news = []
        for i in page:
            link = i.find('a', href=True)
            if link is None:
                continue

            # links = 'https://www.kommersant.ru/' + link['href']
            title = i.find('span', class_='vam').text.strip()

            lst_news.append(title)

        return lst_news


# Парсер binance.com
class ParsBinance(Parser):
    """
    Класс объекта Parser

    Класс для парсинга заголовков новостей;
    """
    def __init__(self):
        self.url_binance = "https://www.binance.com/ru/square/news/all"

    def pars(self):
        driver = webdriver.Chrome()
        driver.get(self.url_binance)
        sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        page = soup.find_all('h3', class_='css-yxpvu')

        ls_news = []
        for i in page:
            title = i.text.strip()
            ls_news.append(title)

        driver.close()

        return ls_news


class ParsForklog(Parser):
    """
    Класс объекта Parser

    Класс для парсинга заголовков новостей;
    """
    def __init__(self):
        self.url = "https://forklog.com/news"

    def pars(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'lxml')
        page = soup.find_all('div', class_='text_blk')

        lst_news = []
        for i in page:
            title = i.find('p').text.strip()

            lst_news.append(title)

        return lst_news
