FROM mcr.microsoft.com/devcontainers/python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-root