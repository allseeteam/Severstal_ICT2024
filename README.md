# Стек технологий

1. Бекенд:
   - Python/Django
   - PostgreSQL
   - Celery/RabbitMQ
   - Docker, docker-compose
2. Поиск и обработка данных:
   - Python/Pandas
   - BeautifulSoup
   - LangChain
   - Pdfplumber - парсинг PDF
   - Yandex Search API
   - Yandex GPT API
   - Youtube API - поиск и получение субтитров
   - RuWordNet, PyMorphy3 - свой поиск

3. Frontend
   - Typescript, React
   - Plotly

# Запуск на сервере

1. Скачать репозитарий

   ```
   git@github.com:allseeteam/Severstal_ICT2024.git
   ```

2. Установка переменных окружения:

- Переименовать файл .env.example в .env
- При необходимости внести изменения

3. Отредактировать файл init-letsencrypt.sh

- Вставить название домена, для которого создается ssl сертификат
- Вставить валидный email администратора

4. Запустить файл init-letsencrypt.sh

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

1. Скачиваем RuWordNet для синонимов

```
ruwordnet download
```

2. Подгружаем csv-файлик с индексом на продовую тачку
3. Запускаем индексацию из файла

```
python manage.py index_csv_file file.csv
```

4. Генерируем ресурс поискового движка

```
python manage.py generate_search.py search.pkl
```
