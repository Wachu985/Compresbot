import asyncio
from pyrogram import Client , dispatcher,filters
import tgcrypto
import os
from shutil import rmtree
from server import ejecute
from compress import compresion, split, getBytes,compressionone
from convopyro import Conversation 
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery
from youtubedl import download,info,downloadlist
import threading
import time
import math
from multiprocessing import Process
from aiohttp import web
import random
import nest_asyncio
nest_asyncio.apply()

print('Iniciando Bot...')
api_id = 15091118
api_hash = "213e85670cd03dfdcfc4936c86d153a2"
bot_token  = '5336546424:AAEN7ioWpVTWjBTXAy2ZrTtLpDnqLF2IxOE'
bot = Client("CompresionBot", api_id, api_hash,bot_token=bot_token)
new = 0
yturls = []
Conversation(bot)

def calculador_tamaño(fichero):
    tamaño_total = 0
    for rutas, directorios, archivos in os.walk(fichero):
        for archivo in archivos:
            subarchivo = os.path.join(fichero, archivo)
            if not os.path.islink(subarchivo):
                tamaño_total += os.path.getsize(subarchivo)

    return tamaño_total

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = []
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

MESSAGE_COMPRIMIDO = 'Seleccione el Tamaño Deseado:👇'
MESSAGE_COMPRIMIDO_BOTTON = [
    [InlineKeyboardButton('Tamaño: 20mb',callback_data='z20'),
     InlineKeyboardButton('Tamaño: 50mb',callback_data='z50')
    ],
    [InlineKeyboardButton('Tamaño: 100mb',callback_data='z100'),
     InlineKeyboardButton('Tamaño: 200mb',callback_data='z200')
    ],
    [InlineKeyboardButton('Tamaño: 500mb',callback_data='z500'),
     InlineKeyboardButton('Tamaño: 1gb',callback_data='z1000')
    ],
    [InlineKeyboardButton('Tamaño: 1.5gb',callback_data='z1500'),
     InlineKeyboardButton('Tamaño: 2gb',callback_data='z2000')
    ],
    [InlineKeyboardButton('CANCEL',callback_data='zstop')        
    ]
]

def randit():
    populaton = 'abcdefgh1jklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*_+,./;'
    contra = "".join(random.sample(populaton,10))
    return contra

def compresionbot(bot,msg,client,save,zips):
    try:
        msg = bot.send_message(msg.chat.id,'🖌Escriba ahora el Nombre del Archivo:👇 Tiene 8 seg...')
        try:
            name = asyncio.run(client.listen.Message(filters.chat(msg.chat.id), timeout = 8))
        except asyncio.TimeoutError:
            msg.edit_text('🚫Tiempo de Espera Exedido🚫')
            return
        file = name.text + '.zip'
        tama = getBytes(str(calculador_tamaño(save))+'MiB')
        tpart = getBytes(zips)
        part = math.ceil(tama/tpart)  
        msg = bot.send_message(msg.chat.id,f'📚Comprimiendo Archivos\nNombre: {file}\n🗂Tamaño Total: {tama}\n📂Tamaño de Partes: {tpart}\n💾Cantidad de Partes: {part}')
        comprimio,partes = split(compresion(file,save),'./',getBytes(zips))
        subidas = str(partes -1)
        msg.delete()
        if comprimio:
            cont = 1
            msg = bot.send_message(msg.chat.id,'⏫Subiendo '+subidas+' Partes')
            while cont < partes:
                filename = file+'.'+str('%03d' % (cont))
                start = time.time()
                bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),progress=progressub,progress_args=(msg,bot,filename,start),thumb='./Imagen.png')  
                # await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),thumb='./Imagen.png')
                os.remove('./'+file+'.'+str('%03d' % (cont)))
                cont += 1 
        msg.delete()
        bot.send_message(msg.chat.id,'✅Subido Correctamente')
    except Exception as e:
        msg.delete()
        bot.send_message(msg.chat.id,f'❌Error al Subir Comprimidos ❌ {e}')

def text_progres(index,max):
	try:
		if max<1:
			max += 1
		porcent = index / max
		porcent *= 100
		porcent = round(porcent)
		make_text = ''
		index_make = 1
		make_text += '\n['
		while(index_make<21):
			if porcent >= index_make * 5: make_text+='●'
			else: make_text+='○'
			index_make+=1
		make_text += ']\n'
		return make_text
	except Exception as ex:
			return ''

def progressddl(current, total,message,bots,filename,start,):
    porcent = int(current * 100 / total)
    act = time.time() - start
    velo = round((round(current/1000000,2)/act),2)
    if porcent % 8 == 0:
        try:
            bots.edit_message_text(message.chat.id,message.id,f"⏬Descargando\n💾Nombre: {filename} \n{text_progres(current,total)}\n📊Porcentaje: {current * 100 / total:.1f}%\n🗓Total :{round(total/1000000,2)} MB \n📥Descargado: {round(current/1000000,2)}\n📥Velocidad: {velo} MiB/S\n") 
        except:
            pass
def progressub(current, total,message,bots,filename,start):
    porcent = int(current * 100 / total)
    act = time.time() - start
    velo = round((round(current/1000000,2)/act),2)
    if porcent % 20 == 0:
        try:
            bots.edit_message_text(message.chat.id,message.id,f"⏫Subiendo\n💾Nombre: {filename} \n{text_progres(current,total)}\n📊Porcentaje: {current * 100 / total:.1f}%\n🗓Total :{round(total/1000000,2)} MB \n📤Subido: {round(current/1000000,2)}\n📥Velocidad: {velo} MiB/S\n")
        except:
            pass

try:
    #Comando Start
    @bot.on_message(filters.command('start') & filters.private)
    def welcome(client,message):
        bot.send_message(message.chat.id,'✉️Bienvenido al Bot '+message.chat.first_name)
    @bot.on_message(filters.command('server') & filters.private)
    def welcome(client,message):
        bot.send_message(message.chat.id,'✉️Bienvenido al Bot '+message.chat.first_name)
        ejecute()
    #Descargar Media de Telegram
    @bot.on_message(filters.media & filters.private)
    def archivos(client,message):
        try:
            save = './'+message.chat.username+'/'
            if message.video:
                try:
                    filename = message.video.file_name
                except:
                    filename = message.video.file_id
            elif message.sticker:
                try:
                    filename = message.sticker.file_name
                except:
                    filename = message.sticker.file_id
            elif message.photo:
                try:
                    filename = message.photo.file_name
                except:
                    filename = message.photo.file_id
            elif message.audio:
                try:
                    filename = message.audio.file_name
                except:
                    filename = message.audio.file_id
            elif message.document:
                try:
                    filename = message.document.file_name
                except:
                    filename = message.document.file_id
            elif message.voice:
                try:
                    filename = message.voice.file_name
                except:
                    filename = message.voice.file_id 

            msg = bot.send_message(message.chat.id,"📡Descargando Archivos... Por Favor Espere",reply_to_message_id=message.id)
            start = time.time() 
            bot.download_media(message,save,progress=progressddl,progress_args=(msg,bot,filename,start))
            # await bot.download_media(message,save)
            msg.delete()
            msg = bot.send_message(msg.chat.id,'✅Descargado Correctamente',reply_to_message_id=message.id)
        except Exception as e:
            msg.delete()
            bot.send_message(msg.chat.id,f'❌Error de Descarga❌ {e}')
    
    #Comando Zips
    @bot.on_message(filters.command('zips') & filters.private)
    def compress(client,message):
        text = MESSAGE_COMPRIMIDO
        reply_botton = InlineKeyboardMarkup(MESSAGE_COMPRIMIDO_BOTTON)
        msg=bot.send_message(chat_id=message.chat.id,text=text,reply_markup=reply_botton,reply_to_message_id=message.id)
    
    #Comando Eliminar Directorio
    @bot.on_message(filters.command('elimreg') & filters.private)
    def delete(client,message):
        save = './'+message.chat.username+'/'
        if os.path.exists(save):
            rmtree(save)
            bot.send_message(message.chat.id,'💢Eliminado el Directorio Correctamente💢')
        else:
            bot.send_message(message.chat.id,'🚫No se Pudo Eliminar el Directorio Correctamente Por que no Existe🚫')
    
    #Comando Mostrar Directorio
    @bot.on_message(filters.command('ls') & filters.private)
    def elem(client,message):
        save = './'+message.chat.username+'/'
        # save = '/app'
        if os.path.exists(save):
            oslist = os.listdir(save)
            cont = 1
            msg ='🔡Archivos: \n'
            for f in oslist:
                msg += str(cont)+'-'+str(f)+'\n'
                cont +=1
            bot.send_message(message.chat.id,msg)
        else:
            bot.send_message(message.chat.id,'🚫No tienes ningun Elemento🚫')
    
    
    #Comando Descargar Video de Youtube
    @bot.on_message(filters.command('ytvid') & filters.private)
    def ytdl(client,message):
        global yturls
        yturls = []
        try:
            yt = info(message.command[-1])
            for f in yt:
                yturls.append(f.split(sep=':'))
            button_list = []
            for each in yturls:
                button_list.append(InlineKeyboardButton(each[1], callback_data = each[0]))
            keyboard_group=InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
            text = 'Seleccione la Resolucion:👇'
            msg= bot.send_message(chat_id=message.chat.id,text=text,reply_markup=keyboard_group,reply_to_message_id=message.id) 
        except Exception as e:
            bot.send_message(message.chat.id,f'❌Error al Analizar el Video❌-> {e}')
    
    
    #Comando Descargar Lista de Youtube
    @bot.on_message(filters.command('ytlist') & filters.private)
    def ytlist(client,message):
        playlist = message.command[1]
        zips = message.command[-1]+'MB'
        res = message.command[2]
        username = message.chat.username
        try:
            msg = bot.send_message(message.chat.id,'⏫Descargando Videos... Por Favor Espere')
            save,title = downloadlist(playlist,res,username)
            file = title+'.zip'
            msg.delete()
            msg = bot.send_message(message.chat.id,'📚Comprimiendo Archivos')
            comprimio,partes = split(compresion(file,save),'./',getBytes(zips))
            subidas = str(partes -1)
            msg.delete()
            if comprimio:
                cont = 1
                up = bot.send_message(message.chat.id,'⏫Subiendo '+subidas+' Partes...')
                while cont < partes:
                    filename = file+'.'+str('%03d' % (cont))
                    start = time.time()
                    bot.send_document(message.chat.id,'./'+file+'.'+str('%03d' % (cont)),progress=progressub,progress_args=(up,bot,filename,start),thumb='./Imagen.png')  
                    # await bot.send_document(message.chat.id,'./'+file+'.'+str('%03d' % (cont)),thumb='./Imagen.png')
                    os.remove('./'+file+'.'+str('%03d' % (cont)))
                    cont += 1 
                up.delete()
                bot.send_message(message.chat.id,'✅Subido Correctamente')
        except Exception as e:
            msg.delete()
            bot.send_message(message.chat.id,f'❌Error al Descargar la Lista❌ {e}')

    #Llamadas al CallBack
    @bot.on_callback_query()
    def callback_querry(client,CallbackQuery):
        #Llamadas de Compresion
        if CallbackQuery.data == 'z20':
            msg = CallbackQuery.message
            zips = '20MiB'
            save = './'+msg.chat.username+'/'
            msg.delete()
            compresionbot(bot,msg,client,save,zips)
        elif CallbackQuery.data == 'z50':
            msg = CallbackQuery.message
            zips = '50MiB'
            save = './'+msg.chat.username+'/'
            msg.delete()
            compresionbot(bot,msg,client,save,zips)
        elif CallbackQuery.data == 'z100':
            msg = CallbackQuery.message
            zips = '100MiB'
            save = './'+msg.chat.username+'/'
            msg.delete()
            compresionbot(bot,msg,client,save,zips)
        elif CallbackQuery.data == 'z200':
            msg = CallbackQuery.message
            zips = '200MiB'
            save = './'+msg.chat.username+'/'
            msg.delete()
            compresionbot(bot,msg,client,save,zips)
        elif CallbackQuery.data == 'z500':
            msg = CallbackQuery.message
            zips = '500MiB'
            save = './'+msg.chat.username+'/'
            msg.delete()
            compresionbot(bot,msg,client,save,zips)
        elif CallbackQuery.data == 'z1000':
            msg = CallbackQuery.message
            zips = '1000MiB'
            save = './'+msg.chat.username+'/'
            msg.delete()
            compresionbot(bot,msg,client,save,zips)  
        elif CallbackQuery.data == 'z1500':
            msg = CallbackQuery.message
            zips = '1500MiB'
            save = './'+msg.chat.username+'/'
            msg.delete()
            compresionbot(bot,msg,client,save,zips) 
        elif CallbackQuery.data == 'z2000':
            msg = CallbackQuery.message
            zips = '2000MiB'
            save = './'+msg.chat.username+'/'
            msg.delete()
            compresionbot(bot,msg,client,save,zips)
        elif CallbackQuery.data =='stop':
            msg = CallbackQuery.message 
            client.listen.Cancel(filters.user(msg.from_user.id))
            msg.delete()
        
        #Llamada de Descarga de Videos
        global yturls
        for each in yturls:
            if CallbackQuery.data == each[0]:
                msg = CallbackQuery.message
                format = each[0]
                ext = each[-1]
                username = msg.chat.username
                url = CallbackQuery.message.reply_to_message.text.split(sep=' ')[-1]
                msg.delete()
                msg = bot.send_message(msg.chat.id,'⏬Descargando... Por favor Espere...')
                try:
                    print(format)
                    file,duration = download(url,username,format)
                    msg.delete()
                    # file += '.'+ext
                    msg = bot.send_message(msg.chat.id,'✅Descargado Correctamente')
                    msg.delete()
                    print(file)
                except Exception as e:
                    msg.delete()
                    bot.send_message(msg.chat.id,f'❌Error al Descargar de Youtube❌ {e}')
                if os.path.exists(file):
                    if os.path.getsize(file) < 1572864000:
                        try:
                            #await bot.send_video(msg.chat.id,file,progress=progressub,progress_args=(msg,bot))
                            msg = bot.send_message(msg.chat.id,'⏫Subiendo a Telegram... Por Favor Espere')
                            # await bot.send_video(msg.chat.id,file,thumb='./Imagen.png',duration=duration)
                            filename = file.split('/')[-1]
                            start = time.time()
                            bot.send_video(msg.chat.id,file,progress=progressub,progress_args=(msg,bot,filename,start),thumb='./Imagen.png',duration=duration)
                            msg.delete()
                            yturls = []
                            break
                        except Exception as e:
                            msg.delete()
                            bot.send_message(msg.chat.id,f'❌Error al Subir a Telegram❌ {e}')
                    elif os.path.getsize(file) > 1572864000:
                        try:
                            string = file.split(sep='/')[:-1]
                            sub = str(file.split(sep='/')[-1].split(sep='.')[0])+'.zip'
                            dir = ''
                            for f in string:
                                dir += f+'/'
                            msg = bot.send_message(msg.chat.id,'📚Comprimiendo Archivos')
                            comprimio,partes = split(compressionone(sub,file),'./',getBytes('1500MiB'))
                            msg.delete()
                            subidas = str(partes -1)
                            if comprimio:
                                cont = 1
                                msg = bot.send_message(msg.chat.id,'⏫Subiendo '+subidas+' Partes')
                                while cont < partes:
                                    filename = sub.split(sep='.')[0]+'.zip.'+str('%03d' % (cont))
                                    start = time.time()
                                    bot.send_document(msg.chat.id,'./'+sub.split(sep='.')[0]+'.zip.'+str('%03d' % (cont)),progress=progressub,progress_args=(msg,bot,filename,start),thumb='./Imagen.png')  
                                    # await bot.send_document(msg.chat.id,'./'+sub.split(sep='.')[0]+'.zip.'+str('%03d' % (cont)),thumb='./Imagen.png')
                                    os.remove('./'+sub.split(sep='.')[0]+'.zip.'+str('%03d' % (cont)))
                                    cont += 1 
                                msg.delete()
                            bot.send_message(msg.chat.id,'✅Subido Correctamente')
                        except Exception as e:
                            msg.delete()
                            bot.send_message(msg.chat.id,f'❌Error al Subir a Telegram❌ {e}')
                else:
                    bot.send_message(msg.chat.id,'❌El Archivo no se Descargó Correctamente❌') 
                
                    

except Exception as ex:
    print(ex)
    yturls = []

if __name__=='__main__':
    try:
        print('Bot Iniciado')
        bot.run()  
    except:
        bot.run()
    
    


    
    


