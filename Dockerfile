FROM python:3.10.4

WORKDIR /fibonacciapp

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["python", "/fibonacciapp/app/main.py"]