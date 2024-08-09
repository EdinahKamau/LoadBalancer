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

- Create the Docker Image : `docker build -t simple-server .`

- Run a Docker container named simple-server-instance, maps port 5000 on the host to port 5000 in the container, sets an environment variable SERVER_ID to "1", and uses the image simple-server.
 ` docker run -p 5000:5000 --name simple-server-instance -e SERVER_ID="1" simple-server`

![image](https://github.com/user-attachments/assets/30142404-db07-44ef-b54d-f8b467bd6e8a)

- Test the End Points are working: `http://localhost:5000/home` in the browser.

![image](https://github.com/user-attachments/assets/1be52dc1-422f-400f-8c9e-302e6796ea40)

### Flow of commands in Docker without CLI

- Build the docker image: `docker build -t simple-server .`
- Confirm that the image is created:  `docker images`
- Run the docker container: `docker run -p 5000:5000 --name simple-server-instance -e SERVER_ID="1" simple-server`
- Confirm the docker container is running:  `docker ps`
- Test the end point on the browser: `http://localhost:5000/home`


### Task 2: Consistent Hashing
The ConsistentHashing class implements a consistent hashing mechanism to distribute requests across multiple virtual server instances. The constructor initializes the class with the number of servers (N), number of slots (slots), and number of virtual nodes per server (K). The init_server_map method populates the server_map with virtual servers mapped to slots using a simple hash function. The get_server method determines the appropriate server for a given request by hashing the request ID and finding the corresponding slot in the server map, ensuring efficient and balanced request distribution.

#### Testing Procedure:

- Starts the service defined in the docker-compose.yml file and scale the service named server to run 3 instances (or replicas) of it:  `docker-compose up --scale server=3`

  ![image](https://github.com/user-attachments/assets/506102f5-fc3a-4453-9209-6bd183265eda)

- Confirm that through the endpoint. `curl http://172.27.0.5:5000/rep`

![image](https://github.com/user-attachments/assets/e5f4472b-3d0e-468e-ad80-a3a504cf218b)

#### Flow of commands

-  Scale the service named server to run 3 instance:   `docker-compose up --scale server=3`
-  Confirm they are running: `docker-compose ps`
-  Test the endpoint on the browser: `curl http://172.27.0.5:5000/rep`

  
### Task 3: Load Balancer
This Flask-based load balancer uses consistent hashing to distribute incoming requests across multiple server instances. It includes endpoints to view current replicas (/rep), add new servers (/add), remove servers (/rm), and route requests to the appropriate server (/). The consistent hashing ensures efficient and balanced distribution of the load among server instances.


#### Testing Procedure:
- Send HTTP requests to load balancer endpoints (/rep, /add, /rm, etc.):  

For /add, the command add 2 more servers, 4 and 5: `curl -X POST -H "Content-Type: application/json" -d '{"n": 2, "hostnames": ["S5", "S4"]}' http://172.27.0.5:5000/add`

![alt text](image-1.png)

 - To remove server 5 use ` curl -X DELETE -H "Content-Type: application/json" -d '{"n": 2, "hostnames": ["S5"]}' http://172.27.0.5:5000/rm`

![alt text](image-2.png)

  
### Task 4: Analysis
Task 4 involves testing and analyzing the performance of the load balancer implementation in various scenarios. We conduct experiments to evaluate load distribution among server containers and the system's ability to recover from server failures promptly.

##### A-1: Launch 10,000 Asynchronous Requests on 3 Server Containers
- Run the A1.py.

![image](https://github.com/user-attachments/assets/f1509574-09de-4937-9d8e-472de83014e9)

- The bar graph illustrates the distribution of requests across three servers: Server1, Server2, and Server3. Server1 has handled the most requests, followed by Server3, while Server2 has handled significantly fewer requests.

##### A-2: Launch 10,000 Asynchronous Requests on 6 Server Containers
- Run the A2.py to increase the number of server to 3 and redestribute the requests

![image](https://github.com/user-attachments/assets/53f36f19-7d21-47cc-beb1-45cfc0c5e24c)

The line graph shows the average load across multiple servers (Server1 through Server6) over a series of 10 runs. The y-axis represents the average load, while the x-axis indicates the run number. Each line corresponds to a different server, with varying colors to distinguish them.
  - Server6 (purple) and Server4 (green) exhibit the most fluctuation in load, with significant spikes and drops across the runs.
  - Server1 (brown) and Server3 (orange) have relatively stable loads, with some variations but generally lower values compared to other servers.
  - Server5 (blue) maintains a more consistent load throughout the runs, with minor fluctuations.
  - Server2 (red) consistently shows a low load across all runs, indicating it was less utilized.

Overall, this graph indicates that load distribution across the servers is uneven and varies considerably from one run to the next. Some servers experience high loads at certain points, while others remain underutilized. This could be indicative of an unbalanced load-balancing algorithm or other factors affecting server utilization.

##### A-3 Test all endpoints of the load balancer 
- Stop and remove the server1 using `docker stop server1 $$ docker rm server1`

![image](https://github.com/user-attachments/assets/5b740a7c-5e0d-461b-900f-8cb1c252328f)


##### A-4: Modify Hash Functions

After modifying the hash functions used in our load balancer, we observed significant changes in how requests were distributed among server instances. The adjustments led to a noticeable shift in load balancing effectiveness, with some servers handling more requests than previously, while others received fewer. This variability directly impacted the overall efficiency of our load balancer in evenly distributing the workload across all servers. The quality of the new hash functions played a crucial role here: well-designed functions helped maintain stable performance even when servers were added or removed, whereas less effective functions struggled to balance the load consistently. These observations underscore the importance of choosing and refining hash functions carefully to optimize load balancing efficiency and maintain system stability under varying operational conditions.  

![image](https://github.com/user-attachments/assets/37d62d66-2fba-4649-a575-8fc115e71cc2)

The first chart is a bar chart titled "Request Distribution Across Servers." It shows the number of requests handled by six different servers (Server1 through Server6). Server2 and Server3 have handled the most requests, each with a count of around 2,500, indicating they are likely the primary servers handling the load. Server4 also handles a significant number of requests, though less than Server2 and Server3. The remaining servers (Server1, Server5, and Server6) handle fewer requests, with Server1 and Server5 having the lowest numbers, indicating they may be used as backup servers or for less critical tasks.

![image](https://github.com/user-attachments/assets/dd7616ed-22de-4910-a275-87d2bb7d6da6)

The second chart is a line graph titled "Average Load of Servers Over Multiple Runs." It tracks the average load on each server across ten different runs. The graph shows significant variability in the load distribution across different servers and runs. Server3 consistently experiences the highest average load, staying around 0.5 across the runs, indicating it is heavily utilized or central to the operations. The other servers (Server1, Server2, Server4, Server5, and Server6) show lower and more fluctuating loads, suggesting they handle more variable or less consistent tasks. This chart highlights the dynamic nature of load distribution among the servers.


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

