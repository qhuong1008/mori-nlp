# Stage 1: Build dependencies
FROM python:3.9 AS builder

WORKDIR /app

COPY . .

# Create a virtual environment that can be copied into the next stage
RUN python -m venv /venv

RUN /venv/bin/pip install -r requirements.txt

# Stage 2: Create final image with application
FROM alpine

COPY --from=builder /venv/ /venv/

ENV PATH=/venv/bin:$PATH

CMD ["uvicorn", "main:app", "--reload"]