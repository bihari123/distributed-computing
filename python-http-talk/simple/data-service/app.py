from flask import Flask, request, jsonify
import requests
import ssl
import json
import os

app = Flask(__name__)

# Mock data
data = {
    "user1": {"id": 1, "name": "User One", "email": "user1@example.com"},
    "user2": {"id": 2, "name": "User Two", "email": "user2@example.com"}
}

@app.route('/data', methods=['POST'])
def get_data():
    user_data = request.json

    # Call auth service to validate credentials
    auth_service = os.environ.get('AUTH_SERVICE_HOST', 'auth-service')
    auth_service_port = os.environ.get('AUTH_SERVICE_PORT', '5000')
    
    try:
        # In a real scenario, you would validate the certificate
        response = requests.post(
            f"https://{auth_service}:{auth_service_port}/auth",
            json=user_data,
            verify=False  # For demo only - in production, use proper cert validation
        )
        
        if response.status_code == 200 and response.json().get('authenticated'):
            username = response.json().get('user')
            if username in data:
                return jsonify(data[username]), 200
            return jsonify({"error": "User data not found"}), 404
        return jsonify({"error": "Authentication failed"}), 401
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error connecting to auth service: {str(e)}"}), 500

if __name__ == '__main__':
    context = ('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=5001, ssl_context=context)
