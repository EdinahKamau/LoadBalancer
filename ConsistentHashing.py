class ConsistentHashing:
    def __init__(self, N, slots, K):
        self.N = N
        self.slots = slots
        self.K = K
        self.server_map = {}
        self.init_server_map()

    def init_server_map(self):
        for i in range(self.N):
            for j in range(self.K):
                virtual_server = f"Server_{i}_{j}"
                slot = self.hash_function(i + j + 2*j + 25) % self.slots
                self.server_map[slot] = virtual_server

    def hash_function(self, value):
        return value

    def get_server(self, request_id):
        slot = self.hash_function(request_id) % self.slots
        while slot not in self.server_map:
            slot = (slot + 1) % self.slots
        return self.server_map[slot]
