import aiohttp
import asyncio
import time
import matplotlib.pyplot as plt
from collections import Counter

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            print(f"Fetching {url}, Status: {response.status}")
            if response.headers['Content-Type'] == 'application/json':
                return await response.json()
            else:
                return {"server": "unknown"}  # Handle unexpected content types
    except Exception as e:
        print(f"Error: {e}")
        return {"server": "error"}

async def main():
    url = "http://localhost:5000/home"
    tasks = []

    async with aiohttp.ClientSession() as session:
        for _ in range(10):  # Adjust the number of requests as needed
            task = asyncio.ensure_future(fetch(session, url))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
    
    servers = [response["server"] for response in responses if response.get("server") != "error"]
    counter = Counter(servers)
    
    if counter:
        # Plot the results
        labels, values = zip(*counter.items())
        plt.bar(labels, values)
        plt.xlabel('Server')
        plt.ylabel('Number of Requests Handled')
        plt.title('Request Distribution Among Servers')
        plt.show()
    else:
        print("No valid responses received.")

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print(f"Completed in {time.time() - start_time} seconds")
