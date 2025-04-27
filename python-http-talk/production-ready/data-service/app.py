from flask import Flask, request, jsonify
import requests
import ssl
import json
import os
import time
import logging
import signal
import sys
import jwt
import traceback

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG level for more information
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('data-service')

app = Flask(__name__)

# Get JWT secret from environment or use default for development
JWT_SECRET = os.environ.get('JWT_SECRET', 'dev-secret-key-change-in-production')
logger.debug(f"Using JWT_SECRET: {JWT_SECRET}")

# Mock data - in production, use a real database
data = {
    "user1": {"id": 1, "name": "User One", "email": "user1@example.com"},
    "user2": {"id": 2, "name": "User Two", "email": "user2@example.com"}
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
    # Check auth service availability
    auth_service = os.environ.get('AUTH_SERVICE_HOST', 'auth-service')
    auth_service_port = os.environ.get('AUTH_SERVICE_PORT', '5000')
    
    try:
        # In production, validate certificates properly
        response = requests.get(
            f"https://{auth_service}:{auth_service_port}/health",
            verify=False,  # For demo only - use proper cert validation in production
            timeout=2
        )
        if response.status_code != 200:
            return jsonify({"status": "auth_service_unavailable"}), 503
    except requests.exceptions.RequestException:
        return jsonify({"status": "auth_service_unavailable"}), 503
    
    return jsonify({"status": "ready"}), 200

@app.route('/data', methods=['POST'])
def get_data():
    start_time = time.time()
    
    if should_exit:
        return jsonify({"error": "Service shutting down"}), 503
        
    try:
        # Debug request info
        logger.debug(f"Request headers: {request.headers}")
        logger.debug(f"Request data: {request.data}")
        
        # Check if request has JSON data
        if not request.is_json:
            logger.warning("Request is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400
            
        request_data = request.json
        logger.debug(f"Parsed JSON data: {request_data}")
        
        # JWT token authentication
        auth_header = request.headers.get('Authorization')
        logger.debug(f"Auth header: {auth_header}")
        
        username = None
        
        if not auth_header or not auth_header.startswith('Bearer '):
            # Fall back to username/password if no JWT provided
            logger.debug("No Bearer token, falling back to username/password")
            
            if 'username' not in request_data or 'password' not in request_data:
                logger.warning("No authentication credentials provided")
                return jsonify({"error": "Authentication required"}), 401
                
            # Call auth service to validate credentials
            auth_service = os.environ.get('AUTH_SERVICE_HOST', 'auth-service')
            auth_service_port = os.environ.get('AUTH_SERVICE_PORT', '5000')
            
            try:
                logger.info(f"Authenticating user {request_data.get('username')} with auth service at {auth_service}:{auth_service_port}")
                response = requests.post(
                    f"https://{auth_service}:{auth_service_port}/auth",
                    json=request_data,
                    verify=False,  # For demo only - use proper cert validation in production
                    timeout=5
                )
                
                logger.debug(f"Auth service response status: {response.status_code}")
                logger.debug(f"Auth service response body: {response.text}")
                
                if response.status_code != 200 or not response.json().get('authenticated'):
                    logger.warning(f"Authentication failed for {request_data.get('username')}")
                    return jsonify({"error": "Authentication failed"}), 401
                
                username = response.json().get('user')
                logger.info(f"Authentication successful for {username}")
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error connecting to auth service: {str(e)}")
                return jsonify({"error": f"Error connecting to auth service: {str(e)}"}), 500
        else:
            # Validate JWT token
            token = auth_header.split(' ')[1]
            try:
                logger.debug(f"Validating JWT token: {token}")
                payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
                username = payload['user']
                logger.info(f"Authenticated via JWT: {username}")
            except jwt.InvalidTokenError as e:
                logger.warning(f"Invalid JWT token: {str(e)}")
                return jsonify({"error": f"Invalid token: {str(e)}"}), 401
            except Exception as e:
                logger.error(f"JWT validation error: {str(e)}")
                logger.error(traceback.format_exc())
                return jsonify({"error": f"Token validation error: {str(e)}"}), 500
        
        logger.debug(f"Username after authentication: {username}")
        
        # Retrieve user data
        if username in data:
            user_data = data[username]
            
            # In production, record metrics, etc.
            duration = time.time() - start_time
            logger.info(f"Data request successful for {username}. Duration: {duration:.4f}s")
            
            # Store retrieval in data directory if it exists
            data_dir = os.environ.get('DATA_DIR', '/app/data')
            if os.path.isdir(data_dir):
                log_file = os.path.join(data_dir, 'access_log.txt')
                try:
                    with open(log_file, 'a') as f:
                        f.write(f"{time.time()},{username},{duration:.4f}\n")
                except Exception as e:
                    logger.warning(f"Could not write to access log: {str(e)}")
            
            return jsonify(user_data), 200
            
        logger.warning(f"User data not found for {username}")
        return jsonify({"error": "User data not found"}), 404
        
    except Exception as e:
        logger.error(f"Error processing data request: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Could not process data request"}), 500

if __name__ == '__main__':
    logger.info('Starting data service...')
    
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
            "-subj", "/CN=data-service"
        ]
        subprocess.run(cert_gen_cmd, check=True)
        
        logger.info(f"Generated self-signed certificates at {cert_path} and {key_path}")
    
    port = int(os.environ.get('PORT', '5001'))
    context = (cert_path, key_path)
    
    app.run(host='0.0.0.0', port=port, ssl_context=context)
