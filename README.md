# Запуск бекенда в режиме разработки локально.

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
