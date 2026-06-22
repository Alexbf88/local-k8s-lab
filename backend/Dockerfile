# ==========================================
# STAGE 1: The Builder (Compiles heavy dependencies)
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a virtual environment and put it securely in the system PATH
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install system dependencies needed for compiling psycopg2 (and other C-extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them directly into the isolated virtual environment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# STAGE 2: The Runner (Secure, lightweight final image)
# ==========================================
FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install ONLY the runtime database libraries (needed for psycopg2 to execute, no compilers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy the completely self-contained virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Ensure the system uses the virtual environment binaries
