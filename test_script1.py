import aiohttp
import asyncio
import time
import matplotlib.pyplot as plt
from collections import Counter

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    url = "http://localhost:5000/home"
    tasks = []

    async with aiohttp.ClientSession() as session:
        for _ in range(10000):
            task = asyncio.ensure_future(fetch(session, url))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
    
    servers = [response["server"] for response in responses]
    counter = Counter(servers)
    
    # Plot the results
    labels, values = zip(*counter.items())
    plt.bar(labels, values)
    plt.xlabel('Server')
    plt.ylabel('Number of Requests Handled')
    plt.title('Request Distribution Among Servers')
    plt.show()

if _name_ == '_main_':
    start_time = time.time()
    asyncio.run(main())
    print(f"Completed in {time.time() - start_time} seconds")