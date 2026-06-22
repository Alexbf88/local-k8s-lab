# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Create a virtual environment and put it in the PATH
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install system dependencies needed for compiling psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages into the virtual environment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# STAGE 2: Final Runtime
# ==========================================
FROM python:3.11-slim

WORKDIR /app

# Install runtime database libraries (needed for psycopg2 to execute)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy the completely self-contained venv from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Ensure Python uses the venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy the Django application code
COPY . /app/

# Create a non-root user for security and give ownership of the app folder
RUN useradd -m portaria_user && chown -R portaria_user:portaria_user /app
USER portaria_user

EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
