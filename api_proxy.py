from openai import OpenAI

from config import RAPID_API_KEY
from models import Article


class RequestProxyAPI:
    def request_to_proxy_api(self, data: list):
        all_articles = Article.query.all()
        text_request = ('Дай прогноз на изменение курса криптовалюты на'
                        'основании новостей представленных ниже. Напиши вывод'
                        'примерно на 30 строк, с описанием в цифрах насколько'
                        'изменится курс криптовалюты и почему.'
                        'Вот данные новости:')
        for article in all_articles:
            text_request = text_request + article.title + '\n'

        client = OpenAI(
            api_key=RAPID_API_KEY,
            base_url="https://api.proxyapi.ru/deepseek/chat/completions",
        )

        chat_completion = client.chat.completions.create(
            model="DeepSeek-V3",
            messages=[{"role": "user", "content": text_request}]
        )
        return chat_completion
