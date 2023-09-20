import json

# import requests
# def open_file(path):
#     with open(path) as file:
#         file_content = json.load(file)
#     return file_content

# def open_file(url):
#     response = requests.get(url)
#     response.raise_for_status()  # This will raise an error if the HTTP request resulted in an error code
#     return response.json()  # Parse JSON and return the content

import aiohttp
async def open_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise ValueError(f"Error {response.status}: {response.reason}")
            return await response.json()  # Parse JSON and return the content