from flask import Flask, request, jsonify
import ssl
import os
import logging
import time
import signal
import sys
import jwt
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('auth-service')

app = Flask(__name__)

# Get JWT secret from environment or use default for development
JWT_SECRET = os.environ.get('JWT_SECRET', 'dev-secret-key-change-in-production')
JWT_EXPIRY_MINUTES = int(os.environ.get('JWT_EXPIRY_MINUTES', '60'))

# Mock user database - in production, use a real database
users = {
    "user1": {"password": "password1", "role": "user"},
    "user2": {"password": "password2", "role": "admin"}
}

# For graceful shutdown
should_exit = False

def signal_handler(sig, frame):
    global should_exit
    logger.info('Received shutdown signal, finishing requests...')
    should_exit = True

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

@app.route('/health', methods=['GET'])
def health_check():
    if should_exit:
        return jsonify({"status": "shutting_down"}), 503
    return jsonify({"status": "healthy"}), 200

@app.route('/readiness', methods=['GET'])
def readiness_check():
    return jsonify({"status": "ready"}), 200

@app.route('/auth', methods=['POST'])
def authenticate():
    start_time = time.time()
    
    if should_exit:
        return jsonify({"error": "Service shutting down"}), 503
        
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        logger.info(f"Authentication attempt for user: {username}")
        
        if not username or not password:
            return jsonify({"authenticated": False, "error": "Missing credentials"}), 400
        
        if username in users and users[username]["password"] == password:
            # Generate JWT token
            payload = {
                'user': username,
                'role': users[username]["role"],
                'exp': datetime.utcnow() + timedelta(minutes=JWT_EXPIRY_MINUTES)
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
            
            duration = time.time() - start_time
            logger.info(f"Authentication successful for {username}. Duration: {duration:.4f}s")
            
            return jsonify({
                "authenticated": True, 
                "user": username,
                "token": token
            }), 200
        
        logger.warning(f"Authentication failed for {username}")
        return jsonify({"authenticated": False, "error": "Invalid credentials"}), 401
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return jsonify({"authenticated": False, "error": "Authentication failed"}), 500

if __name__ == '__main__':
    logger.info('Starting auth service...')
    
    # Check for TLS certificates
    cert_path = os.environ.get('TLS_CERT_PATH', 'cert.pem')
    key_path = os.environ.get('TLS_KEY_PATH', 'key.pem')
    
    # Generate self-signed certificates if they don't exist
    if not (os.path.exists(cert_path) and os.path.exists(key_path)):
        logger.info('Generating self-signed certificates...')
        
        # Generate self-signed certificates using OpenSSL command-line tool
        import subprocess
        
        # Generate private key
        key_gen_cmd = ["openssl", "genrsa", "-out", key_path, "2048"]
        subprocess.run(key_gen_cmd, check=True)
        
        # Generate self-signed certificate
        cert_gen_cmd = [
            "openssl", "req", "-new", "-x509", "-key", key_path, 
            "-out", cert_path, "-days", "365", 
            "-subj", "/CN=auth-service"
        ]
        subprocess.run(cert_gen_cmd, check=True)
        
        logger.info(f"Generated self-signed certificates at {cert_path} and {key_path}")
    
    port = int(os.environ.get('PORT', '5000'))
    context = (cert_path, key_path)
    
    app.run(host='0.0.0.0', port=port, ssl_context=context)
