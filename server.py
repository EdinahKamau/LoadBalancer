from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def home():
    server_id = os.getenv('SERVER_ID', 'unknown')
    return jsonify({"message": "Hello from server", "server_id": server_id})

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
