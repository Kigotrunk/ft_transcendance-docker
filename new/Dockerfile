FROM debian:buster

RUN apt update -y && apt upgrade -y
RUN apt install build-essential libssl-dev libffi-dev libpq-dev python-dev -y
RUN apt install -y wget build-essential libssl-dev libffi-dev libsqlite3-dev zlib1g-dev -y
#RUN apt install python3.11 python3-pip -y
#RUN python3 -m pip install --upgrade pip
RUN cd /usr/src && wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz
RUN cd /usr/src && tar xzf Python-3.11.0.tgz
RUN cd /usr/src/Python-3.11.0 && ./configure --enable-optimizations && make altinstall

WORKDIR ./app
COPY . ./app
#RUN python3 -m pip install requests Pillow django daphne django-cors-headers django-allauth djangorestframework djangorestframework-simplejwt psycopg2-binary channels

RUN python3.11 -m ensurepip
RUN python3.11 -m pip install --upgrade pip
RUN python3.11 -m pip install -r ./app/requirement.txt

EXPOSE 8000

RUN chmod +x ./app/setup.sh

CMD ["sh", "./app/setup.sh"]
