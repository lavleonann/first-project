import telebot
import os
import json
import time
from shutil import rmtree
#from pytube import YouTube
import yt_dlp
dirname = os.path.dirname(__file__)
filename_config = os.path.join(dirname, 'configbot.json')
with open(filename_config) as archive:
    botInfo = json.load(archive)

import yadisk



dp = telebot.TeleBot(botInfo["TOKEN"], parse_mode='HTML')

filePath = 'tmp'#os.getcwd() + '/data/user/'

user = {} # dictionary

ydl_opts = {
        'format': 'm4a/bestaudio/best',
        #'ffmpeg-location': r"D:\PYTHON\AUDIO\ffmpeg.exe",
        'ffmpeg-location': r'/usr/lib/x86_64-linux-gnu',
        'Paths': '/root/tg_audio',
        'outtmpl': 'rutube1.%(ext)s',
        'noplaylist': False,
        'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a'}]
        'ignoreerrors': True,
        'verbose': True}

@dp.message_handler(commands=['start'])
def sendWelcome(message):
    dp.send_message(message.chat.id, 'Этот бот может выгрузить аудиодорожку видео ютуб размером до 50 мб')

@dp.message_handler(content_types=['text'])
def recieveLink(message):
    user[message.chat.id] = {} # identificador
    user[message.chat.id]['url'] = message.text # guarda el message.text (url) en una palabra clave

    
    ydl_opts = {
        'format': 'bestaudio/best',
        #'ffmpeg-location': r"D:\PYTHON\AUDIO\ffmpeg.exe",
        'ffmpeg-location': r'/usr/lib/x86_64-linux-gnu',
        'Paths': '/root/tg_audio',
        'outtmpl': 'rutube1.%(ext)s',
        'noplaylist': False,
        'postprocessors': [{'key': 'FFmpegExtractAudio'}],
        'ignoreerrors': True,
        'verbose': True}

    try:
        #yt = YouTube(user[message.chat.id]['url'])



        content = os.path.join(filePath, str(message.chat.id)+'/')
        content = os.path.abspath(content)
        os.makedirs(content, exist_ok=True) # determina la ruta
        urlVideo = user[message.chat.id]['url']
        
        with yt_dlp.YoutubeDL(ydl_opts) as ytdl: 
            #os.chdir(content) # ira a la ruta que se le ha asignado para procesar la descarga
            ytdl.download(urlVideo) # descargara el audio 
            y = yadisk.YaDisk(token='y0_AgAAAAAByhYjAAquaQAAAADvfFbEAlSqoL2_RG2loU8MYV2Kf7Semvw')
            y.upload('/root/tg_audio/rutube1.m4a', "/Оптимизация.m4a", overwrite=True)
            y.get_download_link("/Оптимизация.m4a") 
            msg = dp.send_message(message.chat.id, y.get_download_link("/Оптимизация.m4a"))


        
        #with os.scandir() as fileAudio:
        #    fileAudio = [file for file in fileAudio if file.is_file()]
        #with open(fileAudio[0], 'rb') as audio:
        #    dp.send_chat_action(message.chat.id, 'upload_audio')
        #    dp.edit_message_text(text=f'Посмотрим что здесь 1',
         #                        chat_id= message.chat.id,
        #                         message_id= msg.message_id)
        #    dp.send_audio(message.chat.id, audio)
        #    dp.edit_message_text(text=f'Посмотрим что здесь 2',
        #                         chat_id = message.chat.id,
        #                         message_id=msg.message_id)
            
            #time.sleep(5)
            #os.system('clear')
            #rmtree(content) # eliminara la carpeta que fue asignada
    except: 
        try: rmtree(content) # si aun se mantiene, lo eliminara
        except: pass
        dp.edit_message_text(text='что-то пошло не так',
                             chat_id= message.chat.id,
                             message_id= msg.message_id)
        
if __name__ == '__main__':
    #print('the bot is listening!')
    dp.infinity_polling()