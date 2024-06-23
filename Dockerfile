# Stage 1: Build dependencies
FROM python:3.9 AS builder

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Stage 2: Create final image with application
FROM alpine

WORKDIR /app

COPY --from=builder . .

ENTRYPOINT ["uvicorn", "main:app", "--reload"]