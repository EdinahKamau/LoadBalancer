from collections import defaultdict
import requests
import random

class ConsistentHashMap:
    def __init__(self, num_servers, num_slots, num_virtual_servers):
        print(f"Initializing ConsistentHashMap with {num_servers} servers, {num_slots} slots, and {num_virtual_servers} virtual servers per server")
        self.num_slots = num_slots
        self.num_virtual_servers = num_virtual_servers
        self.num_servers = num_servers
        self.servers = {}  
        self.name_to_id = {} 
        self.virtual_server_slots = defaultdict(list)
        self.request_to_server = {}
        self.server_to_virtual_slots = defaultdict(list)

        errors = []        
        for i in range(num_servers):
            server_id = random.randint(100000, 999999)
            server_name = f"Server{i + 1}"
            self.add_server(server_id, server_name)

            command = (
                f'docker run --name {server_name} '
                f'--network loadbalancer_custom_network --network-alias {server_name} -d app_server'
            )

            args = shlex.split(command)
            result = subprocess.run(args, text=True, capture_output=True)
            if result.returncode != 0:
                errors.append(f"Error creating container {server_name}: {result.stderr}")
                print(errors)
                
        print(f"Initial servers created successfully.")
        

    def hash_request(self, rid):
        return (rid + 2 * rid + 17) % self.num_slots
        # return hash(rid) % self.num_slots

    def hash_virtual_server(self, server_id, virtual_id):
        return (server_id + virtual_id * 17) % self.num_slots
        # return (hash(server_id) + virtual_id) % self.num_slots

    def add_server(self, server_id, server_name):
        if server_name in self.name_to_id:
            raise ValueError(f"Server name {server_name} already exists.")
        
        if server_id in self.servers:
            raise ValueError(f"Server ID {server_id} already exists.")

        self.name_to_id[server_name] = server_id
        
        for v in range(self.num_virtual_servers):
            base_slot = self.hash_virtual_server(server_id, v)
            slot = base_slot
            initial_slot = base_slot
            
            # Linear probing to find an empty slot
            while slot in self.virtual_server_slots and len(self.virtual_server_slots[slot]) > 0:
                slot = (initial_slot + 1) % self.num_slots
                if slot == initial_slot:  
                    raise Exception("No available slots left")
            
            self.virtual_server_slots[slot].append(server_id)
            self.server_to_virtual_slots[server_id].append(slot)

        self.servers[server_id] = (server_name, len(self.server_to_virtual_slots[server_id]))

    def remove_server(self, server_id=None, server_name=None):
        if server_name:
            if server_name not in self.name_to_id:
                raise ValueError(f"Server name {server_name} does not exist.")
            server_id = self.name_to_id[server_name]
        if server_id:
            if server_id not in self.servers:
                raise ValueError(f"Server ID {server_id} does not exist.")
            for slot in self.server_to_virtual_slots[server_id]:
                if slot in self.virtual_server_slots:
                    self.virtual_server_slots[slot].remove(server_id)
                    if not self.virtual_server_slots[slot]:
                        del self.virtual_server_slots[slot]
            del self.servers[server_id]
            del self.server_to_virtual_slots[server_id]
            if server_id in self.name_to_id.values():
                server_name = [name for name, id in self.name_to_id.items() if id == server_id]
                if server_name:
                    del self.name_to_id[server_name[0]]

    def get_server(self, rid):
        request_slot = self.hash_request(rid)
        sorted_slots = sorted(self.virtual_server_slots.keys())
        for slot in sorted_slots:
            if slot >= request_slot:
                server_list = self.virtual_server_slots[slot]
                server_id = server_list[0] if server_list else None
                if server_id:
                    return self.servers[server_id][0] 
        if sorted_slots:
            server_id = self.virtual_server_slots[sorted_slots[0]][0]
            return self.servers[server_id][0] 
        return None

    def assign_request(self, rid):
        server_name = self.get_server(rid)
        self.request_to_server[rid] = server_name
        return server_name

    def get_server_by_name(self, server_name):
        return self.name_to_id.get(server_name, None)

    def get_server_name(self, server_id):
        return self.servers.get(server_id, (None,))[0]

    def check_heartbeat(self, server_name):
        try:
            response = requests.get(f"http://{server_name}:5000/heartbeat")
            return response.status_code == 200
        except requests.RequestException:
            return False

    def __str__(self):
        server_info = {sid: name for sid, (name, _) in self.servers.items()}
        return f"Servers: {server_info}, Virtual Server Slots: {self.virtual_server_slots}, Requests: {self.request_to_server}"

