
import hashlib
import bisect


class ConsistentHashMap:
    def _init_(self, num_slots, num_servers, num_virtual_servers):
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


# Example usage
if _name_ == "_main_":
    num_slots = 512
    num_servers = 3
    num_virtual_servers = 9

    consistent_hash_map = ConsistentHashMap(num_slots, num_servers, num_virtual_servers)

    # Adding servers
    for i in range(1, num_servers + 1):
        consistent_hash_map.add_server(f"S{i}")

    # Testing the hash map with some keys
    keys = ["key1", "key2", "key3", "key4", "key5"]
    for key in keys:
        server = consistent_hash_map.get_server(key)
        print(f"Key: {key} -> Server: {server}")

    # Removing a server
    consistent_hash_map.remove_server("S1")
    print("\nAfter removing S1:")
    for key in keys:
        server = consistent_hash_map.get_server(key)
        print(f"Key: {key} -> Server: {server}")