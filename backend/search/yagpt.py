import requests


def make_req_data(query):
    folderid = 'b1gjpg4fsjcau2oceikv'
    model = 'yandexgpt'
    uri = f'gpt://{folderid}/{model}/latest'
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


def ask_yagpt(query, api_key):
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    folderid = 'b1gjpg4fsjcau2oceikv'
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Api-Key {api_key}',
        'x-folder-id': folderid
    }
    data = make_req_data(query)
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise ValueError(
            f'YandexGPT API status code {response.status_code}\n\nContent: {response.content.decode("utf-8")}')
    return parse_yagpt_answer(response.json())[0]


def parse_yagpt_answer(content: dict):
    return list(map(lambda x: x['message']['text'], content['result']['alternatives']))