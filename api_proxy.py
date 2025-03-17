from openai import OpenAI
from config import RAPID_API_KEY


class RequestProxyAPI:
    """
    Класс для работы с ProxyAPI

    Класс для обработки запроса на прогноз изменение курса биткойна,
    помощью GPT чата, на основании полученных новостей;
    """

    def __init__(self):
        self.description = (
            'Ты профессиональный бизнес аналитик. Сделай общий вывод '
            'исходя из предоставленных ниже новостей на прогноз изменение '
            'курса криптовалюты биткойн. Напиши вывод'
            'примерно на 100 слов, с описанием насколько изменится курс'
            'криптовалюты и почему.\n')

    def request_to_proxy_api(self, data: list):
        user_request = 'Вот эти новости:'
        for article in data:
            user_request = user_request + article + '\n'
        client = OpenAI(
            api_key=RAPID_API_KEY,
            base_url="https://api.proxyapi.ru/openai/v1",
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.description},
                {"role": "user", "content": user_request}
            ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content


