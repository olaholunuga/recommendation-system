# STAGE 1: Builder
FROM python:3.10-slim AS builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1

# Install system build dependencies
RUN apt-get update && apt-get install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and install Python packages
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# STAGE 2: Production Runner
FROM python:3.10-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
# Copy only the compiled virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY..

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]