FROM langchain/langchain:0.1.0

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./backend/requirements.txt requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y \
    &&  apt install netcat-traditional \
    && pip install --no-cache-dir --upgrade -r requirements.txt \
    && playwright install-deps \
    && playwright install \
    && ruwordnet download

COPY ./backend /app

COPY ./deploy/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

ENTRYPOINT ["/start.sh"]