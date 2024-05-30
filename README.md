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

