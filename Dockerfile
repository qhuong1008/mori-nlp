# Stage 1: Build dependencies
FROM python:3.11 AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Stage 2: Create final image with application
FROM python:3.11-alpine

WORKDIR /app

COPY --from=builder /app /app

# Copy FastAPI app code
COPY . .

CMD [ "poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
