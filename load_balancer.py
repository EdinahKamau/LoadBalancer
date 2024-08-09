import subprocess
from flask import Flask, request, jsonify
import random
from collections import defaultdict
import requests
import shlex
import threading
import time
from consistentHashing.py import ConsistenHashMap


app = Flask(__name__)
chm = ConsistentHashMap(3, 512, 9)
# chm = ConsistentHashMap(6, 512, 9)

@app.route('/rep', methods=['GET'])
def get_replicas():
    replicas = [name for _, (name, _) in chm.servers.items()]

    response = {
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }
    
    return jsonify(response), 200

@app.route('/add', methods=['POST'])
def add_servers():
    data = request.get_json()
    n = data.get("n")
    hostnames = data.get("hostnames", [])

    if len(hostnames) > n:
        return jsonify({"error": "Hostnames list is longer than the number of new instances."}), 400

    errors = []
    new_servers = []

    def generate_unique_server_name():
        while True:
            server_name = f"S{random.randint(1, 999)}"
            if chm.get_server_by_name(server_name) is None and server_name not in new_servers:
                return server_name

    for i in range(n):
        if i < len(hostnames):
            server_name = hostnames[i]
            # Check if the hostname already exists
            if chm.get_server_by_name(server_name) is not None:
                errors.append(f"Hostname {server_name} already exists.")
                continue
        else:
            server_name = generate_unique_server_name()

        # Generate a unique server ID
        while True:
            server_id = random.randint(100000, 999999)
            if server_id not in chm.servers.keys():
                break

        try:
            chm.add_server(server_id, server_name)
            new_servers.append(server_name)

            command = (
                f'docker run --name {server_name} '
                f'--network loadbalancer_custom_network --network-alias {server_name} -d app_server'
            )

            args = shlex.split(command)
            result = subprocess.run(args, text=True, capture_output=True)
            if result.returncode != 0:
                errors.append(f"Error creating container {server_name}: {result.stderr}")
                #rollback
                chm.remove_server(server_id=server_id)
            else:
                print(f"Container {server_name} created successfully.")

        except ValueError as e:
            errors.append(str(e))

    if errors:
        return jsonify({"status": "failed", "errors": errors}), 500

    return jsonify({
        "message": {
            "N": len(chm.servers),
            "replicas": list(chm.servers.values())
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
        to_remove = random.sample(list(chm.servers.values()), n)
        to_remove = [name for name, _ in to_remove]
    else:
        to_remove = hostnames

    errors = []
    removed_servers = []

    for server_name in to_remove:
        server_id = chm.get_server_by_name(server_name)
        if server_id is not None:
            try:
                # Remove server from Consistent Hash Map
                chm.remove_server(server_id=server_id)
                removed_servers.append(server_name)

                # Docker command to remove the server container
                command = f'docker rm -f {server_name}'
                args = shlex.split(command)
                result = subprocess.run(args, text=True, capture_output=True)

                if result.returncode != 0:
                    errors.append(f"Error removing container {server_name}: {result.stderr}")
                    # Rollback
                    chm.add_server(server_id, server_name)
                else:
                    print(f"Container {server_name} removed successfully.")

            except ValueError as e:
                errors.append(str(e))

    # Check the number of remaining servers
    current_num_servers = len(chm.servers)
    if current_num_servers < chm.num_servers:  
        servers_to_add = chm.num_servers - current_num_servers

        new_hostnames = []
        while len(new_hostnames) < servers_to_add:
            new_hostname = f"S{random.randint(1, 999)}"
            if chm.get_server_by_name(new_hostname) is None and new_hostname not in new_hostnames:
                new_hostnames.append(new_hostname)

        try:
            add_response = requests.post(
                "http://172.20.0.3:5000/add",
                json={"n": servers_to_add, "hostnames": new_hostnames}
            )
            if add_response.status_code != 200:
                errors.append(f"Error adding servers: {add_response.text}")
            else:
                print(f"Added {servers_to_add} new servers to maintain balance.")
        except requests.RequestException as e:
            errors.append(f"Failed to send request to add servers: {str(e)}")

    if errors:
        return jsonify({"status": "failed", "errors": errors}), 500

    return jsonify({
        "message": {
            "N": len(chm.servers),
            "removed_replicas": removed_servers,
            "remaining_replicas": list(chm.servers.values())
        },
        "status": "successful"
    })

@app.route('/router', methods=['GET'])
def router():
    rid = random.randint(100000, 999999)

    server_name = chm.assign_request(rid)
    if not server_name:
        return jsonify({"error": "No server available for the request."}), 500

    command = f"docker inspect -f '{{{{range .NetworkSettings.Networks}}}}{{{{.IPAddress}}}}{{{{end}}}}' {server_name}"
    args = shlex.split(command)
    result = subprocess.run(args, text=True, capture_output=True)
    
    if result.returncode != 0:
        return jsonify({"error": f"Error finding IP address of container {server_name}: {result.stderr}"}), 500

    ip_address = result.stdout.strip()
    if not ip_address:
        return jsonify({"error": "No IP address found for the server container."}), 500

    try:
        response = requests.get(f"http://{ip_address}:5000/home")
        if response.status_code == 200:
            return jsonify({"status": "success", "response": f'Hello from server {server_name}',  "server": f'{server_name}'}), 200
        else:
            return jsonify({"error": f"Error response from server {server_name}: {response.text}"}), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": f"Request failed {ip_address}: {str(e)}"}), 500

def heartbeat_check():
    while True:
        time.sleep(60)  
        for server_id, (server_name, _) in list(chm.servers.items()):
            if not chm.check_heartbeat(server_name):
                print(f"Server {server_name} failed heartbeat check. Removing...")
                chm.remove_server(server_id=server_id)

                data = {"n": 1, "hostnames": [f"S{random.randint(1, 999)}"]}
                try:
                    add_response = requests.post("http://172.20.0.3:5000/add", json=data)
                    if add_response.status_code != 200:
                        print(f"Error adding new server: {add_response.text}")
                except requests.RequestException as e:
                    print(f"Failed to send request to add server: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=heartbeat_check, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
