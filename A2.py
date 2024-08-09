import asyncio
import aiohttp
import matplotlib.pyplot as plt
from collections import Counter

REQUESTS_PER_RUN = 70
NUM_RUNS = 10
LOAD_BALANCER_URL = "http://localhost:5000/router"

async def send_request(session):
    async with session.get(LOAD_BALANCER_URL) as response:
        result = await response.json()
        return result['server']

async def send_requests():
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session) for _ in range(REQUESTS_PER_RUN)]
        responses = await asyncio.gather(*tasks)
        return responses

def compute_average_load(responses):
    server_counts = Counter(responses)
    total_requests = sum(server_counts.values())
    average_load = {server: count / total_requests for server, count in server_counts.items()}
    return average_load

def plot_average_loads(average_loads):
    runs = list(range(1, NUM_RUNS + 1))
    server_names = set(name for load in average_loads for name in load.keys())
    
    for server_name in server_names:
        loads = [load.get(server_name, 0) for load in average_loads]
        plt.plot(runs, loads, label=server_name, marker='o')

    plt.xlabel('Run Number')
    plt.ylabel('Average Load')
    plt.title('Average Load of Servers Over Multiple Runs')
    plt.legend()
    
    plt.savefig('analysis_images/A2.png')
    # plt.savefig('analysis_images/A4_A2.png')
   

async def main():
    average_loads = []
    
    for run in range(NUM_RUNS):
        print(f"Starting run {run + 1}/{NUM_RUNS}")
        responses = await send_requests()
        average_load = compute_average_load(responses)
        average_loads.append(average_load)

    plot_average_loads(average_loads)

if __name__ == "__main__":
    asyncio.run(main())
