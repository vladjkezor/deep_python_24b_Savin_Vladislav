import asyncio
import argparse
import re
from collections import Counter
import aiohttp
from bs4 import BeautifulSoup


def read_urls(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]


async def fetch_url(url, session):
    try:
        async with session.get(url) as response:
            data = await response.text()
            soup = BeautifulSoup(data, 'html.parser')
            words = re.findall(r'\b\w+\b', soup.get_text().lower())
            top_words = dict(Counter(words).most_common(5))
            print(f'{url}, {top_words}')
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
    urls = read_urls(filename)
    que = asyncio.Queue()
    for url in urls:
        await que.put(url)
    await que.put(None)

    async with aiohttp.ClientSession() as session:
        tasks = [worker(que, session) for _ in range(n_workers)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', default=50, type=int)
    parser.add_argument('--filename', default='urls.txt', type=str)
    args = parser.parse_args()

    asyncio.run(fetch_batch_urls(args.workers, args.filename))
