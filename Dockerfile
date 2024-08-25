FROM python:3.12.5-slim AS base

WORKDIR /src

COPY pyproject.toml .
COPY logging.conf .

RUN pip install poetry
RUN poetry config virtualenvs.create false

FROM base AS dependencies
RUN poetry install --no-dev

FROM base AS development
RUN poetry install
COPY . .

FROM dependencies AS production
RUN poetry install --no-dev
COPY src src

ARG BUILD_REF=latest
ENV DD_VERSION="${BUILD_REF}"
ENV DD_INTEGRATION_aws-sdk_ENABLED=true
ENV DD_INTEGRATIONS_ENABLED=true
ENV DD_LOGS_ENABLED=true

EXPOSE 8000
