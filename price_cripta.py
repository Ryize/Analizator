"""Текущие курсы криптовалют, график и новости"""

import requests
import matplotlib.pyplot as plt
import io, base64
from bs4 import BeautifulSoup
from textblob import TextBlob



def get_crypto_news():
    url = "https://www.block-chain24.com/news?ysclid=m6ony52ur9108910355"  # Замените на реальный новостной сайт
    # Для использования API требуется зарегистрироваться и получить ключи
    # response = requests.get(url, params={"key_1": "value_1", "key_N": "value_N"}, verify=False)
    response = requests.get(url).text
    soup = BeautifulSoup(response, "lxml")
    page = soup.find_all('div', class_='row-cards__item card card_style-5')

    news = []
    for article in page:
        title = article.find('div', class_='card__title').text.strip()
        link = "https://www.block-chain24.com" + article.find("a")["href"]
        if title and link:
            # sentiment = analyze_sentiment(title)
            news.append(
                {"title": title, "link": link})  #, "sentiment": sentiment})
    return news


# Анализ тональности новости
def analyze_sentiment(text):
    sentiment = TextBlob(
        text).sentiment.polarity  # От -1 (негатив) до 1 (позитив)
    return sentiment


# Получение данных о криптовалюте (пример с Binance)
def get_crypto_prices():
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url)
    data = response.json()
    return {item['symbol']: float(item['price']) for item in data if
            'USDT' in item['symbol']}


# Построение графика
# def generate_plot(prices):
#     fig, ax = plt.subplots()
#     ax.plot(list(prices.keys()), list(prices.values()), marker='o')
#     # plt.xticks(rotation=90)
#     plt.title("Стоимость в USDT")
#     # plt.xlabel("криптовалюта")
#     # plt.ylabel("стоимость в доллар сша")
#
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)
#     encoded_img = base64.b64encode(buf.read()).decode('utf-8')
#     return encoded_img