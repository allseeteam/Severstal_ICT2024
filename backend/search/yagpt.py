import requests
from bs4 import BeautifulSoup
from search.text import normalize_string


def make_prompt_by_html(html_content: str):
    root = BeautifulSoup(html_content)
    text = normalize_string(root.text)
    prompt = f"""Представь, что ты ассистент продуктового аналитика. Я передам тебе текст с аналитического сайта, напиши краткий отчет от 3 до 5 пунктов. Данные:
    {text}
    """
    return prompt


def make_req_data(query, model_id):
    folderid = 'b1gjpg4fsjcau2oceikv'
    # model_id = 'yandexgpt'
    uri = f'gpt://{folderid}/{model_id}/latest'
    return {
        "modelUri": uri,
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": 1024
        },
        "messages": [
            {
                "role": "user",
                "text": query
            }
        ]
    }


def ask_yagpt(query, api_key, model_id):
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    folderid = 'b1gjpg4fsjcau2oceikv'
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Api-Key {api_key}',
        'x-folder-id': folderid
    }
    data = make_req_data(query, model_id)
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise ValueError(
            f'YandexGPT API status code {response.status_code}\n\nContent: {response.content.decode("utf-8")}')
    return parse_yagpt_answer(response.json())[0]


def parse_yagpt_answer(content: dict):
    return list(map(lambda x: x['message']['text'], content['result']['alternatives']))
