FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Generate self-signed certificates for HTTPS
RUN apt-get update && apt-get install -y openssl && \
    openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=auth-service"

EXPOSE 5000

CMD ["python", "app.py"]
