FROM python:3.8.3-slim-buster

ENV LD_LIBRARY_PATH /usr/local/lib

WORKDIR /github-telegram

COPY . /github-telegram

RUN pip3 install -r requirements.txt --no-cache-dir

CMD [ "python3", "./app.py" ]