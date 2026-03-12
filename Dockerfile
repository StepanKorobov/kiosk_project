#Использовалась версия python 3.12.6
FROM python:3.13.2-slim

RUN mkdir /app

COPY requirements.txt /app/

RUN python -m pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

ENTRYPOINT ["python", "main.py"]