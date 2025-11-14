# syntax=docker/dockerfile:1.7

ARG PYTHON_IMAGE=python:3.11-slim

FROM ${PYTHON_IMAGE} AS builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /src

RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

COPY requirements-dev.txt requirements-dev.txt
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

COPY . .
RUN pytest -q

FROM ${PYTHON_IMAGE} AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /srv/app

RUN addgroup --system app && adduser --system --ingroup app --home /srv/app app

COPY --from=builder /wheels /tmp/wheels
COPY requirements.txt requirements.txt

RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install \
        --no-cache-dir \
        --no-warn-script-location \
        --find-links=/tmp/wheels \
        -r requirements.txt \
    && rm -rf /tmp/wheels

ENV PATH="/opt/venv/bin:$PATH"

COPY --chown=app:app app ./app
COPY --chown=app:app alembic ./alembic
COPY --chown=app:app alembic.ini .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["python", "-c", "import sys, urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health');"]

USER app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
