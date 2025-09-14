FROM python:3.12-slim-bookworm

WORKDIR /app

COPY . .

RUN ["pip", "install", "uv"]

RUN ["uv", "add", "-r", "requirements.txt"]

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]