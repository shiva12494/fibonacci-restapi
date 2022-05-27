FROM python:3.10.4 
#   chose 3.10.4 as it has the functions I need eg: LRU cache

WORKDIR /fibonacciapp
#   defining the working directory

COPY requirements.txt .
#   copying the requirements we froze for this container, all the versions of the dependencies

RUN pip install -r requirements.txt
#   installing all dependencies

COPY ./app ./app

CMD ["python", "/fibonacciapp/app/main.py"]
#   running main.py