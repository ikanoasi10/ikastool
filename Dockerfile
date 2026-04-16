FROM ghcr.io/astral-sh/uv:0.9.2-python3.12-bookworm-slim

WORKDIR /app
COPY readme.md pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .
CMD ["uv", "run", "python", "bot/main.py"]
