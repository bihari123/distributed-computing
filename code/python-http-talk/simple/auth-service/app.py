from flask import Flask, request, jsonify
import ssl

app = Flask(__name__)

# Mock user database
users = {
    "user1": "password1",
    "user2": "password2"
}

@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username in users and users[username] == password:
        return jsonify({"authenticated": True, "user": username}), 200
    return jsonify({"authenticated": False}), 401

if __name__ == '__main__':
    context = ('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=5000, ssl_context=context)
