import asyncio
import aiohttp
import matplotlib.pyplot as plt
from collections import Counter

TOTAL_REQUESTS = 9000
LOAD_BALANCER_URL = "http://172.20.0.3:5000/router"

async def send_request(session):
    async with session.get(LOAD_BALANCER_URL) as response:
        result = await response.json()
        return result['server']

async def send_requests():
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session) for _ in range(TOTAL_REQUESTS)]
        responses = await asyncio.gather(*tasks)
        return responses

def plot_server_requests(server_counts):
    servers = list(server_counts.keys())
    counts = list(server_counts.values())

    plt.bar(servers, counts, color='skyblue')
    plt.xlabel('Server Name')
    plt.ylabel('Number of Requests Handled')
    plt.title('Request Distribution Across Servers')
    plt.savefig('analysis_images/A1.png')
    # plt.savefig('analysis_images/A4_A1.png')

async def main():
    responses = await send_requests()
    
    server_counts = Counter(responses)
    
    plot_server_requests(server_counts)

if __name__ == "__main__":
    asyncio.run(main())
