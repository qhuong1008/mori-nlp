# Stage 1: Build dependencies
FROM python:3.9 AS builder

WORKDIR /app

COPY . .

# Create a virtual environment that can be copied into the next stage
RUN python -m venv /venv

RUN /venv/bin/pip install -r requirements.txt

# Stage 2: Second builder for small iamge size
FROM alpine AS builder2

WORKDIR /app

COPY --from=builder /venv/ /venv/

# Stage 3: Production stage (minimal image size reduce stage)
FROM alpine

WORKDIR /app

COPY --from=builder2 /venv/ /venv/

# Set environment variable for virtual environment path
ENV PATH=/venv/bin:$PATH

CMD ["uvicorn", "main:app", "--reload"]