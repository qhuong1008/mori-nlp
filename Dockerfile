FROM python:3.11-slim AS builder

WORKDIR /app

COPY . .

FROM alpine

WORKDIR /app

COPY --from=builder /app/ .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
