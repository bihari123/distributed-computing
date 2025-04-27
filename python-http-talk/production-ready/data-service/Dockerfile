FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Add non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5001

# Install dependencies including OpenSSL
RUN apt-get update && \
    apt-get install -y --no-install-recommends openssl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Generate certificates with proper permissions
RUN openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=data-service" && \
    chmod 644 cert.pem && \
    chmod 644 key.pem && \
    chown -R appuser:appuser /app

# Create data directory with proper permissions
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# Switch to non-root user
USER appuser

EXPOSE 5001

# Start app with Gunicorn (more robust than Flask's dev server)
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--certfile=cert.pem", "--keyfile=key.pem", "--workers", "2", "--threads", "4", "app:app"]
