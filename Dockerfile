FROM python:3.8-slim-buster

RUN pip install poetry==1.1.8

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY . .

CMD ["poetry", "run", "python", "src/main.py"]
