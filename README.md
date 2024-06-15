# Запуск бекенда в режиме разработки локально

Создание и активация виртуального окружения:

```
python -m venv venv
. venv/bin/activate
```

Установка переменных окружения:

- Переименовать файл .env.example в .env
- При необходимости внести изменения

Создание контейнеров БД

```
sudo docker compose -f docker-compose-dev.yml up -d
```

Установка зависимостей:

Для работы LangChain на Linux:

```
sudo apt-get install libwoff1 libwebpdemux2 libenchant-2-2  libsecret-1-0  libhyphen0 libegl1 lib evdev2 libgles2 
```

Python зависимости

```
cd backend
pip install -r requirements.txt

```

ДАЛЕЕ ВСЕ КОМАНДЫ ТАКЖЕ ВЫПОЛНЯЕМ ИЗ ПАПКИ BACKEND

Установка миграций:

```
python manage.py migrate
```

Создание админа:

```
python manage.py createsuperuser
```

Запуск сервера разработчика:

```
python manage.py runserver
```

Установка playwright (движок для хрома или что)

```
playwright install
```

Запуск парсинга первоначальной БД страниц

- Необходимо внести список ссылок в файл: backend/accounts/management/commands/start_urls.py

- Запустить парсинг:

```
python manage.py init_data
```

Выгрузка страниц в CSV:

```
python manage.py model2csv accounts.WebPage > pages.csv
```

# Поиск

## Как завести в продакшн

0. Скачиваем RuWordNet для синонимов

```
ruwordnet download
```

1. Подгружаем csv-файлик с индексом на продовую тачку
2. Запускаем индексацию из файла

```
python manage.py index_csv_file file.csv
```

3. Генерируем ресурс поискового движка

```
python manage.py generate_search.py search.pkl
```

TODO: перенести название файлика в конфиг

4. Можно запускать, все заработает по эндпоинту `/api/v1/search/?q=банк`

# PDF

[https://camelot-py.readthedocs.io/en/master/user/install-deps.html](https://camelot-py.readthedocs.io/en/master/user/install-deps.html)

```bash
apt install ghostscript python3-tk
```
