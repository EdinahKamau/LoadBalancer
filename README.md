# Customizable Load Balancer 
# Introduction
Welcome to the Customizable Load Balancer project! This project aims to implement a highly customizable load balancer system that efficiently distributes incoming requests among multiple server instances. The load balancer utilizes consistent hashing algorithms to ensure even distribution of load and high availability of services.

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
- Python: Version 3.6 or above (for server implementation)
- Flask: Version 2.0 or above (for server implementation)
- Other dependencies as specified requirements.txt
  
## Tasks
### Task 1: Server
In Task 1, we implement a simple web server that exposes two endpoints: /home and /heartbeat. The /home endpoint returns a unique identifier to distinguish among replicated server containers, while the /heartbeat endpoint sends heartbeat responses upon request.

#### Testing Procedure:

- Start the server container: `docker-compose up server`
- Send HTTP GET requests to `/home` and `/heartbeat` endpoints:
-- `curl localhost:5000/home`
-- `curl localhost:5000/heartbeat`
 - Verify that the server returns the expected responses.

### Task 2: Consistent Hashing
Task 2 involves implementing a consistent hash map using an array, linked list, or any other suitable data structure. The consistent hash map efficiently maps client requests to server instances, ensuring even distribution of load across the system.

#### Testing Procedure:

- Implement the consistent hash map data structure.
- Generate a set of client requests and map them to server instances using the consistent hash algorithm.
- Verify that the requests are evenly distributed among server instances.
  
### Task 3: Load Balancer
Task 3 focuses on building a load balancer container that utilizes the consistent hashing data structure from Task 2 to manage a set of web server containers. The load balancer container provides HTTP endpoints to modify configurations and check the status of managed web server replicas.

#### Testing Procedure:

- Build and deploy the load balancer container: docker-compose up load_balancer
- Send HTTP requests to load balancer endpoints (/rep, /add, /rm, etc.): curl localhost:5000/rep and curl -X POST -d '{"n": 2, "hostnames": ["S5", "S4"]}' localhost:5000/add
- Verify that the load balancer routes requests to server replicas as expected.
- Test load balancing under varying load conditions.
  
### Task 4: Analysis
Task 4 involves testing and analyzing the performance of the load balancer implementation in various scenarios. We conduct experiments to evaluate load distribution among server containers and the system's ability to recover from server failures promptly.

#### Testing Procedure:

- Launch 10000 asynchronous requests on N = 3 server containers.
- Increment N from 2 to 6 and launch 10000 requests on each increment.
- Test all endpoints of the load balancer and verify the system's behavior in case of server failure.

### Getting Started
To get started with the Customizable Load Balancer project, follow these steps:
- Clone the project repository to your local Ubuntu machine.
- Install the required dependencies listed above.
- Follow the instructions provided in the individual task directories to implement and test each component.
- Refer to the README files in each task directory for detailed setup and testing instructions.
  
### Contributing
Contributions to the Customizable Load Balancer project are welcome! Feel free to fork the repository, make improvements, and submit pull requests. Please ensure that your code follows the project's coding guidelines and standards.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgments
Special thanks to the course instructors for providing the assignment specifications and guidance.
References to relevant research papers and documentation sources are provided in the project documentation.

