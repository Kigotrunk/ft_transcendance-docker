FROM python:3.12-alpine

EXPOSE 8000

WORKDIR /app

COPY requirements.txt .

RUN apk update && apk upgrade && \
    apk add --no-cache \
    build-base \
    sdl2 \
    libffi-dev \
    openssl-dev \
    bzip2-dev \
    zlib-dev \
    readline-dev \
    sqlite-dev \
    python3-dev \
    postgresql-dev \
    postgresql-client \
    jpeg-dev \
    freetype-dev \
    sdl2-dev \
    sdl2_image \
    sdl2_mixer \
    sdl2_ttf \
    tzdata && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

RUN ls -l /app/ && cat /app/entrypoint.sh

ENV DJANGO_SETTINGS_MODULE=new.settings

ENTRYPOINT ["/app/entrypoint.sh"]



CMD ["sh", "-c", "python3 manage.py runserver 0.0.0.0:8000"]
