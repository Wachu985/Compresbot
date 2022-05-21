import asyncio
from pyrogram import Client , dispatcher,filters
import tgcrypto
import os
from shutil import rmtree
from compress import compresion, split, getBytes
from convopyro import Conversation 
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery
from pytube import YouTube,Playlist

api_id = 15091118
api_hash = "213e85670cd03dfdcfc4936c86d153a2"
bot_token  = '5336546424:AAEN7ioWpVTWjBTXAy2ZrTtLpDnqLF2IxOE'
bot = Client("LocoBot", api_id, api_hash,bot_token=bot_token)

yturls = []
Conversation(bot)
# def progress_func(current,total,falta):
#     print(f'{current * 100 / total:.1f}')

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

async def progressddl(current, total,message,bots):
    message.delete()
    await bots.send_message(message.chat.id,f"⏬Descargando\n{text_progres(current,total)}\n📊Porcentaje: {current * 100 / total:.1f}%\n🗓Total :{round(total/1000000,2)} MB \n📥Descargado: {round(current/1000000,2)}\n")

async def progressub(current, total,message,bots):
    message.delete()
    await bots.send_message(message.chat.id,f"⏫Subiendo \n{text_progres(current,total)}\n📊Porcentaje: {current * 100 / total:.1f}%\n🗓Total :{round(total/1000000,2)} MB \n📤Subido: {round(current/1000000,2)}\n")


try:
    #Comando Start
    @bot.on_message(filters.command('start') & filters.private)
    async def welcome(client,message):
        await bot.send_message(message.chat.id,'✉️Bienvenido al Bot '+message.chat.first_name)
    
    @bot.on_message(filters.media & filters.private)
    async def archivos(client,message):
        try:
            save = './'+message.chat.username+'/'
            msg = await bot.send_message(message.chat.id,"📡Descargando Archivos",reply_to_message_id=message.id)
            # await bot.download_media(message,save,progress=progressddl,progress_args=(msg,bot))
            await bot.download_media(message,save)
            await bot.edit_message_text(msg.chat.id,msg.id,'✅Descargado Correctamente')
        except:
            await bot.edit_message_text(msg.chat.id,msg.id,'❌Error de Descarga❌')
    #Comando Zips
    @bot.on_message(filters.command('zips') & filters.private)
    async def compress(client,message):
        text = MESSAGE_COMPRIMIDO
        reply_botton = InlineKeyboardMarkup(MESSAGE_COMPRIMIDO_BOTTON)
        msg=await bot.send_message(chat_id=message.chat.id,text=text,reply_markup=reply_botton,reply_to_message_id=message.id)
    #Comando Eliminar Directorio
    @bot.on_message(filters.command('elimreg') & filters.private)
    async def delete(client,message):
        save = './'+message.chat.username+'/'
        if os.path.exists(save):
            rmtree(save)
            await bot.send_message(message.chat.id,'💢Eliminado el Directorio Correctamente💢')
        else:
            await bot.send_message(message.chat.id,'🚫No se Pudo Eliminar el Directorio Correctamente Por que no Existe🚫')
    #Comando Mostrar Directorio
    @bot.on_message(filters.command('elem') & filters.private)
    async def elem(client,message):
        save = './'+message.chat.username+'/'
        if os.path.exists(save):
            oslist = os.listdir(save)
            cont = 1
            msg ='🔡Archivos: \n'
            for f in oslist:
                msg += str(cont)+'-'+str(f)+'\n'
                cont +=1
            await bot.send_message(message.chat.id,msg)
        else:
            await bot.send_message(message.chat.id,'🚫No tienes ningun Elemento🚫')
    #Comando Descargar Video de Youtube
    @bot.on_message(filters.command('ytvid') & filters.private)
    async def ytdl(client,message):
        yt = YouTube(message.command[-1])
        formats = yt.streams.filter(file_extension='mp4')
        formats = formats.order_by('resolution')
        title = yt.title 
        for f in formats:
            global yturls
            yturls.append(str(str(f).split(sep=' ')[1].split(sep='"')[1]+':'+str(f).split(sep=' ')[3].split(sep='"')[1]))
        button_list = []
        for each in yturls:
            button_list.append(InlineKeyboardButton(each.split(sep=':')[-1], callback_data = each.split(sep=':')[0]))
        keyboard_group=InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
        text = 'Seleccione la Resolucion:👇'
        msg= await bot.send_message(chat_id=message.chat.id,text=text,reply_markup=keyboard_group,reply_to_message_id=message.id) 
    #Comando Descargar Lista de Youtube
    @bot.on_message(filters.command('ytlist') & filters.private)
    async def ytlist(client,message):
        playlist = message.command[1]
        zips = message.command[-1]+'MB'
        play = Playlist(playlist)
        title = play.title
        file = title+'.zip'
        save = './'+message.chat.username+'/'+title+'/'
        out = list()
        subidas = str(partes -1)
        for video in play.videos:
            out.append(video.streams.get_by_resolution('720p').download(save))
        comprimio,partes = split(compresion(file,save),'./',getBytes(zips))
        if comprimio:
            cont = 1
            up = await bot.send_message(message.chat.id,'⏫Subiendo '+subidas+' Partes')
            while cont < partes:
                # await bot.send_document(message.chat.id,'./'+file+'.'+str('%03d' % (cont)),progress=progressub,progress_args=(up,bot),thumb='./Imagen.png')  
                await bot.send_document(message.chat.id,'./'+file+'.'+str('%03d' % (cont)),thumb='./Imagen.png')
                os.remove('./'+file+'.'+str('%03d' % (cont)))
                cont += 1 

    #Llamadas al CallBack
    @bot.on_callback_query()
    async def callback_querry(client,CallbackQuery):
        #Llamadas de Compresion
        if CallbackQuery.data == 'z20':
            msg = CallbackQuery.message
            zips = '20MB'
            save = './'+msg.chat.username+'/'
            await msg.edit_text('🖌Escriba ahora el Nombre del Archivo:👇')
            try:
                name = await client.listen.Message(filters.chat(msg.chat.id), timeout = 50)
            except asyncio.TimeoutError:
                await msg.edit_text('🚫Tiempo de Espera Exedido🚫')
            file = name.text + '.zip'
            msg = await bot.send_message(msg.chat.id,'Comprimiendo Archivos')
            comprimio,partes = split(compresion(file,save),'./',getBytes(zips))
            subidas = str(partes -1)
            await msg.delete()
            if comprimio:
                cont = 1
                up = await bot.send_message(msg.chat.id,'⏫Subiendo '+subidas+' Partes')
                while cont < partes:
                    # await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),progress=progressub,progress_args=(up,bot),thumb='./Imagen.png')  
                    await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),thumb='./Imagen.png')
                    os.remove('./'+file+'.'+str('%03d' % (cont)))
                    cont += 1 
                await up.delete()
            await bot.send_message(msg.chat.id,'✅Subido Correctamente') 
        elif CallbackQuery.data == 'z50':
            msg = CallbackQuery.message
            zips = '50MB'
            save = './'+msg.chat.username+'/'
            await msg.edit_text('🖌Escriba ahora el Nombre del Archivo:👇')
            try:
                name = await client.listen.Message(filters.chat(msg.chat.id), timeout = 50)
            except asyncio.TimeoutError:
                await msg.edit_text('🚫Tiempo de Espera Exedido🚫')
                return
            file = name.text + '.zip'
            msg = await bot.send_message(msg.chat.id,'Comprimiendo Archivos')
            comprimio,partes = split(compresion(file,save),'./',getBytes(zips))
            subidas = str(partes -1)
            await msg.delete()
            if comprimio:
                cont = 1
                up = await bot.send_message(msg.chat.id,'⏫Subiendo '+subidas+' Partes')
                while cont < partes:
                    # await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),progress=progressub,progress_args=(up,bot),thumb='./Imagen.png')  
                    await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),thumb='./Imagen.png')
                    os.remove('./'+file+'.'+str('%03d' % (cont)))
                    cont += 1 
                await up.delete()
            await bot.send_message(msg.chat.id,'✅Subido Correctamente')  
        elif CallbackQuery.data == 'z100':
            msg = CallbackQuery.message
            zips = '100MB'
            save = './'+msg.chat.username+'/'
            await msg.edit_text('🖌Escriba ahora el Nombre del Archivo:👇')
            try:
                name = await client.listen.Message(filters.chat(msg.chat.id), timeout = 50)
            except asyncio.TimeoutError:
                await msg.edit_text('🚫Tiempo de Espera Exedido🚫')
                return
            file = name.text + '.zip'
            msg = await bot.send_message(msg.chat.id,'Comprimiendo Archivos')
            comprimio,partes = split(compresion(file,save),'./',getBytes(zips))
            await msg.delete()
            subidas = str(partes -1)
            if comprimio:
                cont = 1
                up = await bot.edit_message_text(msg.chat.id,msg.id,'⏫Subiendo '+subidas+' Partes')
                while cont < partes:
                    # await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),progress=progressub,progress_args=(up,bot),thumb='./Imagen.png')  
                    await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),thumb='./Imagen.png')
                    os.remove('./'+file+'.'+str('%03d' % (cont)))
                    cont += 1 
                await up.delete()
            await bot.send_message(msg.chat.id,'✅Subido Correctamente') 
        elif CallbackQuery.data == 'z200':
            msg = CallbackQuery.message
            zips = '200MB'
            save = './'+msg.chat.username+'/'
            await msg.edit_text('🖌Escriba ahora el Nombre del Archivo:👇')
            try:
                name = await client.listen.Message(filters.chat(msg.chat.id), timeout = 50)
            except asyncio.TimeoutError:
                await msg.edit_text('🚫Tiempo de Espera Exedido🚫')
                return
            file = name.text + '.zip'
            msg = await bot.send_message(msg.chat.id,'Comprimiendo Archivos')
            comprimio,partes = split(compresion(file,save),'./',getBytes(zips))
            subidas = str(partes -1)
            await msg.delete()
            if comprimio:
                cont = 1
                up = await bot.send_message(msg.chat.id,'⏫Subiendo '+subidas+' Partes')
                while cont < partes:
                    # await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),progress=progressub,progress_args=(up,bot),thumb='./Imagen.png')  
                    await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),thumb='./Imagen.png')
                    os.remove('./'+file+'.'+str('%03d' % (cont)))
                    cont += 1 
                await up.delete()
            await bot.send_message(msg.chat.id,'✅Subido Correctamente') 
        elif CallbackQuery.data == 'z500':
            msg = CallbackQuery.message
            zips = '500MB'
            save = './'+msg.chat.username+'/'
            await msg.edit_text('🖌Escriba ahora el Nombre del Archivo:👇')
            try:
                name = await client.listen.Message(filters.chat(msg.chat.id), timeout = 50)
            except asyncio.TimeoutError:
                await msg.edit_text('🚫Tiempo de Espera Exedido🚫')
                return
            file = name.text + '.zip'
            msg = await bot.send_message(msg.chat.id,'Comprimiendo Archivos')
            comprimio,partes = split(compresion(file,save),'./',getBytes(zips))
            subidas = str(partes -1)
            await msg.delete()
            if comprimio:
                cont = 1
                up = await bot.send_message(msg.chat.id,'⏫Subiendo '+subidas+' Partes')
                while cont < partes:
                    # await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),progress=progressub,progress_args=(up,bot),thumb='./Imagen.png')  
                    await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),thumb='./Imagen.png')
                    os.remove('./'+file+'.'+str('%03d' % (cont)))
                    cont += 1 
                await up.delete()
            await bot.send_message(msg.chat.id,'✅Subido Correctamente') 
        elif CallbackQuery.data == 'z1000':
            msg = CallbackQuery.message
            zips = '1000MB'
            save = './'+msg.chat.username+'/'
            await msg.edit_text('🖌Escriba ahora el Nombre del Archivo:👇')
            try:
                name = await client.listen.Message(filters.chat(msg.chat.id), timeout = 50)
            except asyncio.TimeoutError:
                await msg.edit_text('🚫Tiempo de Espera Exedido🚫')
                return
            file = name.text + '.zip'
            msg = await bot.send_message(msg.chat.id,'Comprimiendo Archivos')
            comprimio,partes = split(compresion(file,save),'./',getBytes(zips))
            subidas = str(partes -1)
            await msg.delete()
            if comprimio:
                cont = 1
                up = await bot.send_message(msg.chat.id,'⏫Subiendo '+subidas+' Partes')
                while cont < partes:
                    # await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),progress=progressub,progress_args=(up,bot),thumb='./Imagen.png')  
                    await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),thumb='./Imagen.png')
                    os.remove('./'+file+'.'+str('%03d' % (cont)))
                    cont += 1 
                await up.delete()
            await bot.send_message(msg.chat.id,'✅Subido Correctamente')  
        elif CallbackQuery.data == 'z1500':
            msg = CallbackQuery.message
            zips = '1500MB'
            save = './'+msg.chat.username+'/'
            await msg.edit_text('🖌Escriba ahora el Nombre del Archivo:👇')
            try:
                name = await client.listen.Message(filters.chat(msg.chat.id), timeout = 50)
            except asyncio.TimeoutError:
                await msg.edit_text('🚫Tiempo de Espera Exedido🚫')
                return
            file = name.text + '.zip'
            msg = await bot.send_message(msg.chat.id,'Comprimiendo Archivos')
            comprimio,partes = split(compresion(file,save),'./',getBytes(zips))
            subidas = str(partes -1)
            await msg.delete()
            if comprimio:
                cont = 1
                up = await bot.send_message(msg.chat.id,'⏫Subiendo '+subidas+' Partes')
                while cont < partes:
                    # await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),progress=progressub,progress_args=(up,bot),thumb='./Imagen.png')  
                    await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),thumb='./Imagen.png')
                    os.remove('./'+file+'.'+str('%03d' % (cont)))
                    cont += 1 
                await up.delete()
            await bot.send_message(msg.chat.id,'✅Subido Correctamente')  
        elif CallbackQuery.data == 'z2000':
            msg = CallbackQuery.message
            zips = '2000MB'
            save = './'+msg.chat.username+'/'
            await msg.edit_text('🖌Escriba ahora el Nombre del Archivo:👇')
            try:
                name = await client.listen.Message(filters.chat(msg.chat.id), timeout = 50)
            except asyncio.TimeoutError:
                await msg.edit_text('🚫Tiempo de Espera Exedido🚫')
                return
            file = name.text + '.zip'
            await bot.send_message(msg.chat.id,'📚Comprimiendo')
            msg = await bot.send_message(msg.chat.id,'Comprimiendo Archivos')
            comprimio,partes = split(compresion(file,save),'./',getBytes(zips))
            await msg.delete()
            subidas = str(partes -1)
            if comprimio:
                cont = 1
                up = await bot.send_message(msg.chat.id,'⏫Subiendo '+subidas+' Partes')
                while cont < partes:
                    # await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),progress=progressub,progress_args=(up,bot),thumb='./Imagen.png')  
                    await bot.send_document(msg.chat.id,'./'+file+'.'+str('%03d' % (cont)),thumb='./Imagen.png')
                    os.remove('./'+file+'.'+str('%03d' % (cont)))
                    cont += 1 
                await up.delete()
            await bot.send_message(msg.chat.id,'✅Subido Correctamente')  
        elif CallbackQuery.data =='stop':
            msg = CallbackQuery.message 
            await client.listen.Cancel(filters.user(msg.from_user.id))
            await msg.delete()
        #Llamada de Descarga de Videos
        global yturls
        for each in yturls:
            if CallbackQuery.data == each.split(sep=':')[0]:
                msg = CallbackQuery.message
                vidval = int(CallbackQuery.data)
                save = './'+msg.chat.username+'/'
                vid = CallbackQuery.message.reply_to_message.text.split(sep=' ')[-1]
                yt = YouTube(vid)
                stream = yt.streams.get_by_itag(vidval)
                await msg.delete()
                msg = await bot.send_message(msg.chat.id,'⏬Descargando...')
                file = stream.download(save)
                await msg.delete()
                msg = await bot.send_message(msg.chat.id,'✅Descargado Correctamente')
                await msg.delete()
                #await bot.send_video(msg.chat.id,file,progress=progressub,progress_args=(msg,bot))
                msg = await bot.send_message(msg.chat.id,'⏫Subiendo a Telegram')
                await bot.send_video(msg.chat.id,file,progress=progressub,progress_args=(msg,bot))
                await msg.delete()
                yturls = []
                break

except Exception as ex:
    print(ex)

print('Bot Iniciado')
asyncio.run(bot.run())