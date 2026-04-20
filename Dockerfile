FROM ghcr.io/astral-sh/uv:0.9.2-python3.12-bookworm-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app
COPY README.md pyproject.toml ./
RUN uv sync

COPY . .
RUN touch /app/db.sqlite && chmod 666 /app/db.sqlite

CMD ["uv", "run", "python", "bot/main.py"]
