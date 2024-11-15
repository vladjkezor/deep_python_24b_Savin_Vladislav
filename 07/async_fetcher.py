import asyncio

import aiohttp
from time import time


def read_urls(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

async def fetch_url(url, session):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                # await asyncio.to_thread(BeautifulSoup(text, 'html.parser'))
                # words = re.findall(r'\b\w+\b', text.get_text().lower())
                # print(url)
            else:
                print(f"Failed to fetch {url} with status {response.status}")

    except Exception as e:
        print(f"Error fetching {url}: {e}")



async def worker(que):
    async with aiohttp.ClientSession() as session:
        while True:
            url = await que.get()
            if url is None:
                await que.put(None)
                break
            await fetch_url(url, session)


async def fetch_batch_urls(urls, n_workers):
    que = asyncio.Queue()
    for url in urls:
        await que.put(url)
    await que.put(None)

    tasks = [worker(que) for _ in range(n_workers)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    file_with_urls = 'urls_test.txt'
    test_urls = read_urls(file_with_urls)
    t0 = time()
    asyncio.run(fetch_batch_urls(test_urls, 30))
    print(time() - t0)

    t0 = time()
    asyncio.run(fetch_batch_urls(test_urls, 10))
    print(time() - t0)

    t0 = time()
    asyncio.run(fetch_batch_urls(test_urls, 100))
    print(time() - t0)
