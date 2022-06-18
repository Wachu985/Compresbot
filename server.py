import asyncio
import os

from aiohttp import web
from aiohttp import streamer


@streamer
def file_sender(writer, file_path=None):
    with open(file_path, 'rb') as f:
        chunk = f.read(2 ** 16)
        while chunk:
            writer.write(chunk)
            chunk = f.read(2 ** 16)


def download_file(request):
    file_name = request.match_info['file_name']  
    route =  request.match_info['route']
    headers = {
        "Content-disposition": "attachment; filename={file_name}".format(file_name=file_name)
    }

    file_path = os.path.join(route, file_name)

    if not os.path.exists(file_path):
        return web.Response(
            body='El Archivo  <{file_name}> No Existe'.format(file_name=file_name),
            status=404
        )

    return web.Response(
        body=file_sender(file_path=file_path),
        headers=headers
    )



def ejecute():
    app = web.Application(client_max_size=30000000)
    app.router.add_get('/file/{route}/{file_name}', download_file)
    print('RUN')
    web.run_app(app, host='0.0.0.0', port=os.getenv('PORT'))


