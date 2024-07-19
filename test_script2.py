import aiohttp
import asyncio
import time
import matplotlib.pyplot as plt
from collections import Counter

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def test_load(n):
    # Adjust servers on the load balancer
    async with aiohttp.ClientSession() as session:
        await session.post("http://localhost:5000/add", json={"n": n})

    url = "http://localhost:5000/home"
    tasks = []

    async with aiohttp.ClientSession() as session:
        for _ in range(10000):
            task = asyncio.ensure_future(fetch(session, url))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

    servers = [response["server"] for response in responses]
    counter = Counter(servers)
    
    return sum(counter.values()) / len(counter)

async def main():
    ns = range(2, 7)
    avg_loads = []

    for n in ns:
        avg_load = await test_load(n)
        avg_loads.append(avg_load)

    # Plot the results
    plt.plot(ns, avg_loads, marker='o')
    plt.xlabel('Number of Servers (N)')
    plt.ylabel('Average Load per Server')
    plt.title('Scalability of Load Balancer')
    plt.show()

if _name_ == '_main_':
    start_time = time.time()
    asyncio.run(main())
    print(f"Completed in {time.time() - start_time} seconds")