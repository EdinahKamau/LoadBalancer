from flask import Flask, jsonify, request
from ConsistentHashing import ConsistentHashing  # Import the ConsistentHashing class

app = Flask(__name__)

N = 3
slots = 512
K = 9

consistent_hashing = ConsistentHashing(N, slots, K)  # Create an instance of ConsistentHashing

# Define endpoints for the load balancer
@app.route('/rep', methods=['GET'])
def replicas():
    return jsonify({
        "message": {
            "N": N,
            "replicas": list(consistent_hashing.server_map.values())
        },
        "status": "successful"
    }), 200

# Implement /add endpoint to add new server instances
@app.route('/add', methods=['POST'])
def add_server():
    data = request.json
    n = data.get('n')
    hostnames = data.get('hostnames')

    # Add new servers to consistent hashing
    # Implementation omitted for brevity

    return jsonify({
        "message": {
            "N": N + n,
            "replicas": list(consistent_hashing.server_map.values())
        },
        "status": "successful"
    }), 200

# Implement /rm endpoint to remove server instances
@app.route('/rm', methods=['DELETE'])
def remove_server():
    data = request.json
    n = data.get('n')
    hostnames = data.get('hostnames')

    # Remove servers from consistent hashing
    # Implementation omitted for brevity

    return jsonify({
        "message": {
            "N": N - n,
            "replicas": list(consistent_hashing.server_map.values())
        },
        "status": "successful"
    }), 200

# Implement routing of requests to server instances
@app.route('/')
def route_request():
    server = consistent_hashing.get_server(hash(request.path))
    # Forward request to the selected server
    # You need to implement the logic for forwarding the request here
    return "Request forwarded to server: " + server

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
