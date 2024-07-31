import hashlib
import bisect
from flask import Flask, jsonify

app = Flask(__name__)

class ConsistentHashMap:
    def __init__(self, num_slots, num_servers, num_virtual_servers):
        self.num_slots = num_slots
        self.num_servers = num_servers
        self.num_virtual_servers = num_virtual_servers
        self.slot_to_server = {}
        self.sorted_slots = []

    def add_server(self, server_id):
        virtual_servers = [f"{server_id}-v{v}" for v in range(self.num_virtual_servers)]
        for virtual_server in virtual_servers:
            slot = self._hash_function(virtual_server) % self.num_slots
            self.slot_to_server[slot] = virtual_server
            self.sorted_slots.append(slot)
        self.sorted_slots.sort()

    def remove_server(self, server_id):
        virtual_servers = [f"{server_id}-v{v}" for v in range(self.num_virtual_servers)]
        for virtual_server in virtual_servers:
            slot = self._hash_function(virtual_server) % self.num_slots
            del self.slot_to_server[slot]
            self.sorted_slots.remove(slot)

    def get_server(self, key):
        hashed_key = self._hash_function(key)
        idx = bisect.bisect_right(self.sorted_slots, hashed_key % self.num_slots)
        if idx == len(self.sorted_slots):
            return self.slot_to_server[self.sorted_slots[0]]
        else:
            return self.slot_to_server[self.sorted_slots[idx]]

    def _hash_function(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

consistent_hash_map = ConsistentHashMap(num_slots=512, num_servers=3, num_virtual_servers=9)

@app.route('/add_server/<server_id>', methods=['POST'])
def add_server(server_id):
    consistent_hash_map.add_server(server_id)
    return jsonify({"message": f"Server {server_id} added"})

@app.route('/remove_server/<server_id>', methods=['POST'])
def remove_server(server_id):
    consistent_hash_map.remove_server(server_id)
    return jsonify({"message": f"Server {server_id} removed"})

@app.route('/home', methods=['GET'])
def home():
    key = str(time.time())  # Use current time to generate a unique key
    server = consistent_hash_map.get_server(key)
    return jsonify({"server": server})

if __name__ == '__main__':
    for i in range(1, 4):  # Example initial servers
        consistent_hash_map.add_server(f"S{i}")
    app.run(host='0.0.0.0', port=5000)
