import asyncio
import os

from aiohttp import web
from aiohttp import streamer


@streamer
async def file_sender(writer, file_path=None):
    """
    This function will read large file chunk by chunk and send it through HTTP
    without reading them into memory
    """
    with open(file_path, 'rb') as f:
        chunk = f.read(2 ** 16)
        while chunk:
            await writer.write(chunk)
            chunk = f.read(2 ** 16)


async def download_file(request):
    file_name = request.match_info['file_name']  # Could be a HUGE file
    route =  request.match_info['route']
    headers = {
        "Content-disposition": "attachment; filename={file_name}".format(file_name=file_name)
    }

    file_path = os.path.join(route, file_name)

    if not os.path.exists(file_path):
        return web.Response(
            body='File <{file_name}> does not exist'.format(file_name=file_name),
            status=404
        )

    return web.Response(
        body=file_sender(file_path=file_path),
        headers=headers
    )


def ejecute():
    loop = asyncio.get_event_loop()

    app = web.Application()
    app.router.add_get('/file/{route}/{file_name}', download_file)
    print('RUN')
    web.run_app(app, host='0.0.0.0', port=8000)

    loop.close()