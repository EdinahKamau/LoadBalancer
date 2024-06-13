# Customizable Load Balancer 
# Introduction
This project aims to implement a highly customizable load balancer system that efficiently distributes incoming requests among multiple server instances. The load balancer utilizes consistent hashing algorithms to ensure even distribution of load and high availability of services.

## Overview
In distributed systems, load balancers play a crucial role in managing and optimizing resource utilization by distributing incoming requests across multiple server instances. This project focuses on implementing a load balancer system that can be easily customized and deployed in various distributed application scenarios.

## Features
- Dynamic Scalability: The load balancer system supports dynamic scaling of server instances to handle varying levels of incoming traffic.
- Consistent Hashing: Utilizes consistent hashing algorithms to evenly distribute requests among server instances while minimizing request rerouting in case of server failures.
- Fault Tolerance: Ensures high availability of services by automatically spawning new server instances in case of server failures.
- Easy Deployment: Docker-based deployment allows for easy setup and management of the entire system in a containerized environment.
  
## Dependencies
- Ubuntu 20.04 LTS or above
- Docker: Version 20.10.23 or above
- Docker-compose: Version 1.29.2 or above
- Python: Version 3.7 or above (for server implementation)
- Flask: Version 2.0 or above (for server implementation)
- Werkzeug 2.0.2
- aiohttp (for testing) 

## Installations
- `sudo apt-get update `
- `sudo apt-get install -y python3 python3-pip `
- `pip3 install Flask==2.0 Werkzeug==2.0.2 aiohttp `
- `sudo apt-get remove docker docker-engine docker.io containerd runc`
- `sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release `
- `curl -fsSL https://get.docker.com -o get-docker.sh `
- `sudo systemctl enable docker`
- `sudo systemctl start docker`
- `sudo apt-get install -y docker-compose`
  
## Tasks
### Task 1: Server
This Flask application defines a simple web server with two endpoints. The /home endpoint responds to GET requests with a JSON message that includes a server identifier, which is fetched from an environment variable SERVER_ID. If the variable is not set, it defaults to 'Unknown'. The /heartbeat endpoint provides a health check by responding with a 200 OK status and an empty body. The application runs on host 0.0.0.0 and port 5000.

#### Testing Procedure:

- Start the server container: `docker-compose up server`
- Send HTTP GET requests to `/home` and `/heartbeat` endpoints:
-- `curl localhost:5000/home`
-- `curl localhost:5000/heartbeat`
 - Verify that the server returns the expected responses.

### Task 2: Consistent Hashing
The ConsistentHashing class implements a consistent hashing mechanism to distribute requests across multiple virtual server instances. The constructor initializes the class with the number of servers (N), number of slots (slots), and number of virtual nodes per server (K). The init_server_map method populates the server_map with virtual servers mapped to slots using a simple hash function. The get_server method determines the appropriate server for a given request by hashing the request ID and finding the corresponding slot in the server map, ensuring efficient and balanced request distribution.

#### Testing Procedure:

- Implement the consistent hash map data structure.
- Generate a set of client requests and map them to server instances using the consistent hash algorithm.
- Verify that the requests are evenly distributed among server instances.
  
### Task 3: Load Balancer
This Flask-based load balancer uses consistent hashing to distribute incoming requests across multiple server instances. It includes endpoints to view current replicas (/rep), add new servers (/add), remove servers (/rm), and route requests to the appropriate server (/). The consistent hashing ensures efficient and balanced distribution of the load among server instances.


#### Testing Procedure:

- Build and deploy the load balancer container: `docker-compose up load_balancer`
- Send HTTP requests to load balancer endpoints (/rep, /add, /rm, etc.): `curl localhost:5000/rep and curl -X POST -d '{"n": 2, "hostnames": ["S5", "S4"]}' localhost:5000/add`
- Verify that the load balancer routes requests to server replicas as expected.
- Test load balancing under varying load conditions.
  
### Task 4: Analysis
Task 4 involves testing and analyzing the performance of the load balancer implementation in various scenarios. We conduct experiments to evaluate load distribution among server containers and the system's ability to recover from server failures promptly.

#### Testing Procedure:
- Launch the server `docker-compose up server`
- Launch the Load Balancer `docker-compose up load_balancer`
- Launch the application using `python WebServer.py`
- Launch 10000 asynchronous requests on N = 3 server containers.
  `asyncio.run()`
  `docker run -d --name server1 -p 5001:5000 server-image`
  `docker run -d --name server2 -p 5002:5000 server-image`
  `docker run -d --name server3 -p 5003:5000 server-image`
- Increment N from 2 to 6 and launch 10000 requests on each increment.
  `docker run -d --name server4 -p 5004:5000 server-image`  
  `curl -X POST -H "Content-Type: application/json" -d '{"n": 1, "hostnames": ["server4"]}' http://localhost:5000/add`

- Test all endpoints of the load balancer and verify the system's behavior in case of server failure.
  `curl http://localhost:5000/rep`
  `curl -X POST -H "Content-Type: application/json" -d '{"n": 1, "hostnames": ["serverX"]}' http://localhost:5000/add`
  `curl -X DELETE -H "Content-Type: application/json" -d '{"n": 1, "hostnames": ["serverY"]}' http://localhost:5000/rm`

- Simulate server failures
  `docker stop server1`

- Analyze the behaviour then cleanup by removing the servers.
 `docker stop server1 server2 server3 server4 server5 server6`
 `docker rm server1 server2 server3 server4 server5 server6`


By following these steps, you can comprehensively test the performance and robustness of your load balancer implementation in various scenarios.


### Deployment Instruction
To get started with the Customizable Load Balancer project, follow these steps:
- Clone the project repository to your local Ubuntu machine.
- Install the required dependencies listed above.
- Follow the instructions provided in the individual task directories to implement and test each component.
- Refer to the README files in each task directory for detailed setup and testing instructions.
  
### Contribution
Contributions to the Customizable Load Balancer project are welcome! Feel free to fork the repository, make improvements, and submit pull requests. Please ensure that your code follows the project's coding guidelines and standards.

### Acknowledgments
Special thanks to the course instructors for providing the assignment specifications and guidance.
References to relevant research papers and documentation sources are provided in the project documentation.

