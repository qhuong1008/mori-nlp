# Stage 1: Build dependencies
FROM python:3.9-alpine AS builder

WORKDIR /app

COPY . .

RUN pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

RUN pip install -r requirements.txt

# Stage 2: Create final image with application
FROM python:3.9-alpine

WORKDIR /app

COPY --from=builder /app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
