from openai import OpenAI

client = OpenAI(
    api_key="{PROXY_API_KEY}",
    base_url="https://api.proxyapi.ru/openai/v1",
)

chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}]
)