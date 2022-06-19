import asyncio
import os.path
import shutil

import aiofiles
import aiohttp
from tempfile import TemporaryDirectory
import sys
from urllib.parse import urlparse


async def get_content_length(url):
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as request:
            return request.content_length


def parts_generator(size, start=0, part_size=10 * 1024 ** 2):
    while size - start > part_size:
        yield start, start + part_size
        start += part_size
    yield start, size


async def download(url, headers, save_path):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as request:
            file = await aiofiles.open(save_path, 'wb')
            await file.write(await request.content.read())


async def process(url):
    filename = os.path.basename(urlparse(url).path)
    print(filename)
    tmp_dir = TemporaryDirectory(prefix=filename, dir=os.path.abspath('.'))
    size = await get_content_length(url)
    tasks = []
    file_parts = []
    for number, sizes in enumerate(parts_generator(size)):
        part_file_name = os.path.join(tmp_dir.name, f'{filename}.part{number}')
        file_parts.append(part_file_name)
        tasks.append(download(url, {'Range': f'bytes={sizes[0]}-{sizes[1]}'}, part_file_name))
    await asyncio.gather(*tasks)
    with open('./Wachu985/'+filename, 'wb') as wfd:
        for f in file_parts:
            with open(f, 'rb') as fd:
                shutil.copyfileobj(fd, wfd)
    print('Descarga Finalizada')