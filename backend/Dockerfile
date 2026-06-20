# --- STAGE 1: Compile Dependencies ---
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Install dependencies into a localized folder inside /root/.local
RUN pip install --no-cache-dir --user -r requirements.txt


# --- STAGE 2: Secure Final Runtime ---
FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# We only need the runtime library for postgres, not the development headers or compiler
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy the compiled dependencies from the builder stage
COPY --from=builder /root/.local /root/.local
COPY . .

# Ensure the system path finds our copied user binaries (like gunicorn)
ENV PATH=/root/.local/bin:$PATH

# Your excellent secure user configuration
RUN useradd -u 8888 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
