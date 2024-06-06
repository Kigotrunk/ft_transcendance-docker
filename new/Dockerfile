# FROM debian:buster

# RUN apt update -y && apt upgrade -y
# RUN apt install build-essential libssl-dev libffi-dev libpq-dev python-dev -y
# RUN apt install -y wget build-essential libssl-dev libffi-dev libsqlite3-dev zlib1g-dev -y
# #RUN apt install python3.11 python3-pip -y
# #RUN python3 -m pip install --upgrade pip
# RUN cd /usr/src && wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz
# RUN cd /usr/src && tar xzf Python-3.11.0.tgz
# RUN cd /usr/src/Python-3.11.0 && ./configure --enable-optimizations && make altinstall

# WORKDIR ./app
# COPY . ./app
# #RUN python3 -m pip install requests Pillow django daphne django-cors-headers django-allauth djangorestframework djangorestframework-simplejwt psycopg2-binary channels

# RUN python3.11 -m ensurepip
# RUN python3.11 -m pip install --upgrade pip
# RUN python3.11 -m pip install -r ./app/requirement.txt
# RUN python3.11 -m pip install react
# EXPOSE 8000




FROM alpine:3.20

WORKDIR ./app
COPY . ./app

RUN apk update && apk upgrade
RUN apk add --no-cache alpine-sdk build-base sdl2 libffi-dev openssl-dev bzip2-dev zlib-dev readline-dev sqlite-dev python3-dev py3-pip postgresql-dev python3 gcc musl-dev linux-headers jpeg-dev freetype-dev sdl2-dev sdl2_image sdl2_mixer sdl2_ttf
RUN pip3 install --break-system-packages --no-cache-dir -r app/requirement.txt

RUN chmod +x ./app/setup.sh
CMD ["sh", "./app/setup.sh"]
