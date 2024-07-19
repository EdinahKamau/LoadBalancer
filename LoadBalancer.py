from flask import Flask, request, jsonify
import requests
import random
import string

app = Flask(_name_)
servers = ["Server 1", "Server 2", "Server 3"]

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({
        "message": {
            "N": len(servers),
            "replicas": servers
        },
        "status": "successful"
    })

@app.route('/add', methods=['POST'])
def add_servers():
    data = request.get_json()
    n = data.get("n")
    hostnames = data.get("hostnames", [])

    if len(hostnames) > n:
        return jsonify({"error": "Hostnames list is longer than the number of new instances."}), 400

    new_servers = hostnames + [f"Server {len(servers) + i + 1}" for i in range(n - len(hostnames))]
    servers.extend(new_servers)
    return jsonify({
        "message": {
            "N": len(servers),
            "replicas": servers
        },
        "status": "successful"
    })

@app.route('/rm', methods=['DELETE'])
def remove_servers():
    data = request.get_json()
    n = data.get("n")
    hostnames = data.get("hostnames", [])

    if len(hostnames) > n:
        return jsonify({"error": "Hostnames list is longer than the number of instances to be removed."}), 400

    if len(hostnames) == 0:
        to_remove = random.sample(servers, n)
    else:
        to_remove = hostnames

    for server in to_remove:
        if server in servers:
            servers.remove(server)

    return jsonify({
        "message": {
            "N": len(servers),
            "replicas": servers
        },
        "status": "successful"
    })

@app.route('/<path>', methods=['GET'])
def route_request(path):
    server = random.choice(servers)
    response = requests.get(f"http://{server}:5000/{path}")
    return response.json()

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000)
