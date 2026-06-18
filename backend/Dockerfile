# Use an official stable Python slim image to minimize footprint
FROM python:3.11-slim AS base

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required for compilation and PostgreSQL connectivity
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# Create a non-privileged user for enhanced container security (Pod Security Standards)
RUN useradd -u 8888 appuser && chown -R appuser:appuser /app
USER appuser

# Expose the default internal port used by Gunicorn/Django
EXPOSE 8000

# Default command to start the application with Gunicorn production server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
