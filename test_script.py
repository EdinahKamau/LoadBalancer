import asyncio
import aiohttp

async def send_requests(url, num_requests):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)
        return responses

if __name__ == "__main__":
    # Define the URL and number of requests based on your target server
    url = 'http://localhost:5000/'
    num_requests = 10000
    
    # Run the asyncio event loop and the coroutine
    asyncio.run(send_requests(url, num_requests))
