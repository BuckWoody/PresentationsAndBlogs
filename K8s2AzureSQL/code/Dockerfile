# syntax=docker/dockerfile:1
FROM laudio/pyodbc
WORKDIR /flask2sql

RUN pip install Flask
RUN pip install configparser

COPY . .

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]