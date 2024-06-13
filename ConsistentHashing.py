class ConsistentHashing:
    def __init__(self, N, slots, K):
        """
        Initialize the ConsistentHashing instance.
        
        Args:
        N (int): Number of servers.
        slots (int): Number of slots in the hash space.
        K (int): Number of virtual nodes per server.
        """
        self.N = N
        self.slots = slots
        self.K = K
        self.server_map = {}
        self.init_server_map()  # Initialize the server map with virtual nodes

    def init_server_map(self):
        """
        Populate the server_map with virtual nodes for each server.
        """
        for i in range(self.N):
            for j in range(self.K):
                # Create a unique identifier for each virtual server node
                virtual_server = f"Server_{i}_{j}"
                # Determine the slot for this virtual server using the hash function
                slot = self.hash_function(i + j + 2 * j + 25) % self.slots
                # Map the slot to the virtual server in the server_map
                self.server_map[slot] = virtual_server

    def hash_function(self, value):
        """
        Hash function to map a value to a slot in the hash space.
        
        Args:
        value (int): Value to be hashed.
        
        Returns:
        int: Hashed value.
        """
        return value

    def get_server(self, request_id):
        """
        Get the server for a given request based on the request ID.
        
        Args:
        request_id (int): Unique identifier for the request.
        
        Returns:
        str: The virtual server responsible for handling the request.
        """
        # Compute the initial slot for the request using the hash function
        slot = self.hash_function(request_id) % self.slots
        # Find the closest slot that has a server mapped to it
        while slot not in self.server_map:
            slot = (slot + 1) % self.slots  # Linear probing to find the next available slot
        return self.server_map[slot]  # Return the virtual server mapped to the slot

# Example usage
if __name__ == "__main__":
    # Initialize with 3 servers, 512 slots, and 9 virtual nodes per server
    ch = ConsistentHashing(N=3, slots=512, K=9)

    # Get the server for a specific request ID
    request_id = 123
    server = ch.get_server(request_id)
    print(f"Request ID {request_id} is routed to {server}")
