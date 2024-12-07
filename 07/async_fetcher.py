import asyncio
import argparse
import re
from collections import Counter
import aiohttp
from bs4 import BeautifulSoup


async def read_urls(filename, que):
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            if url:
                await que.put(url)
        await que.put(None)


async def fetch_url(url, session):
    try:
        async with session.get(url) as response:
            data = await response.text()
            soup = BeautifulSoup(data, 'html.parser')
            words = re.findall(r'\b\w+\b', soup.get_text().lower())
            top_words = dict(Counter(words).most_common(5))
            print(f'{url}, {top_words}')
    except asyncio.TimeoutError:
        print(f'Timeout while fetching {url}')
    except Exception as e:
        print(f'Failed to fetch {url}, error: {e}')


async def worker(que, session):
    while True:
        url = await que.get()
        if url is None:
            await que.put(None)
            break

        await fetch_url(url, session)


async def fetch_batch_urls(n_workers, filename):
    que = asyncio.Queue(maxsize=n_workers * 2)

    timeout = aiohttp.ClientTimeout(
        total=10,
        connect=5,
        sock_connect=5,
        sock_read=5
    )
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [worker(que, session) for _ in range(n_workers)]

        await asyncio.gather(*tasks, read_urls(filename, que))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', default=10, type=int)
    parser.add_argument('--filename', default='urls.txt', type=str)
    args = parser.parse_args()

    asyncio.run(fetch_batch_urls(args.workers, args.filename))
