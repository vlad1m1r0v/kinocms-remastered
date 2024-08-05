FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system packages
RUN apt-get update \
    && apt-get install -y curl build-essential libpq-dev gcc\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY pyproject.toml poetry.lock /code/
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Copy project
COPY src /code/src
COPY static /code/static
COPY templates /code/templates
COPY locale /code/locale
COPY images /code/images
COPY Makefile /code/Makefile

# Copy entrypoint
COPY config/web/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
