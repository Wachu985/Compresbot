import yt_dlp
from pyrogram import Client , dispatcher,filters
import tgcrypto
import asyncio


def my_hook(d):
    if d['status'] == 'downloading':
        current = d['downloaded_bytes']
        total = d['total_bytes']
        speed = d['speed']
        print(f'Descargando {current * 100 / total:.1f} --- {speed}')
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def info(url):
    ydl_opts = {
        'restrict_filenames':True
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            url, download=False)

    formats = meta['formats']
    locura = {}
    id = []
    ext = []
    formato = []
    for format in formats:
        if 'DASH' in str(format['format']):
            continue
        elif 'mp4' == str(format['ext']):    
            id.append(format['format_id'])
            ext.append(format['ext'])
            formato.append(format['format'].split(sep='-')[-1])
    cont = 0
    guardar = []
    for val1,val2,val3 in zip(id,ext,formato): 
        guardar.append(val1 +':'+val3 + ':'+val2)
    return guardar   

def download(url,username,format):
    file = './'+username+'/%(title)s.%(ext)s'
    opcions = {
        'format': format,
        'outtmpl': file,
        'restrict_filenames':True
    }

    with yt_dlp.YoutubeDL(opcions) as ydl:
        ydl.download([url])
        meta = ydl.extract_info(url, download=False)
        name = './'+username+'/'+str(meta['title'])+'.mp4'
        duration = int(meta['duration'])
    return name,duration

def downloadlist(urls,res,username):
    file = './'+username+'/%(playlist)s/%(title)s.%(ext)s'
    ydl_opts = {
        'format': f'best[height<={res}]',
        'outtmpl': file,
        'restrict_filenames':True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([urls])
        meta = ydl.extract_info(urls, download=False)
        dir = './'+username+'/'+str(meta['title'])+'/'
        name = str(meta['title'])
        return dir,name
    