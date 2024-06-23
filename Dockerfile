# Stage 1: Build dependencies
FROM python:3.11-alpine AS builder

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps build-base python3 py3-pip

RUN pip install -r requirements.txt

# Stage 2: Create final image with application
FROM alpine:latest

WORKDIR /app

COPY --from=builder /app/ .

COPY --from=builder /app/app.py /app/  # Copy only the application file

COPY --from=builder /app/*.py /app/  # Copy all Python files

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
