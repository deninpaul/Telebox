import json
import os
from pyrogram import Client, filters
from utils import get_file_id

bot = Client(
    "CDN", 
    os.getenv('API_ID'), 
    os.getenv('API_HASH'),
    bot_token=os.getenv('BOT_TOKEN'),
    max_concurrent_transmissions=5,
    no_updates=False,
    in_memory=False
)

@bot.on_message(filters.document | filters.photo | filters.video)
def user_upload( _ , message):
    file = json.dumps({
        "file_id": message.document.file_id if message.document else get_file_id(message),
        "mime_type": message.document.mime_type if message.document else "application/zip",
        "message_id": message.id
    })

    print(file)

def startBot():
    bot.start()

def stopBot():
    bot.log_out()