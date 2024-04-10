FROM python:3.10

WORKDIR /jiosaavanbot

COPY . /jiosaavanbot

RUN pip install -r requirements.txt

CMD [ "python3", "telegrambot.py" ]