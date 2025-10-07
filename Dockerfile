FROM python:3.12

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

COPY pyproject.toml ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -e .

COPY ./src/ ./src
COPY ./fixtures ./fixtures

CMD ["python", "src/bot/main.py"]