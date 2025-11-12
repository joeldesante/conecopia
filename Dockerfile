# Use official Python runtime as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

# Copy project files
COPY . .

# Change to the Django project directory
WORKDIR /app/order

# Skip collectstatic during build - we'll do it after deployment with env vars
# RUN python manage.py collectstatic --noinput

# Create a non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Make sure we're in the order directory
WORKDIR /app/order

# Run gunicorn (adjust 'order.wsgi' to match your wsgi module path)
CMD gunicorn --bind 0.0.0.0:$PORT --workers 3 --timeout 120 order.wsgi:application