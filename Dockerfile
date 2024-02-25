FROM python:3.11-alpine

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry==1.7.1

WORKDIR /app

COPY pyproject.toml poetry.lock ./


ARG ENVIRONMENT=Development
ENV ENVIRONMENT=${ENVIRONMENT}

RUN if [$ENVIRONMENT = "Development"]; \
        then poetry install; \
    else \
        poetry install --no-dev; \
    fi

COPY src ./src

CMD if [ $ENVIRONMENT = "Development" ]; then\
        poetry run reloadium run ./src/main.py; \ 
    else \
        poetry run python ./src/main.py; \
    fi