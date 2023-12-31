import os
import requests
import mimetypes
from prisma.models import File
from utils import logger
from telegram import bot
from pyrogram import filters
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

@bot.on_message(filters.document | filters.photo | filters.video | filters.animation)
def user_upload( _ , message):
    file = {}
    if (message.document):
        file = {
            "id": message.document.file_id,
            "name": message.document.file_name,
            "size": message.document.file_size,
            "type": message.document.mime_type,
            "msgId": str(message.id),
            "thumbId": message.document.thumbs[-1].file_id if message.document.thumbs else ""
        }
    elif (message.photo):
        response = requests.get("https://api.telegram.org/bot" + os.getenv('BOT_TOKEN') + "/getFile", params={"file_id" : message.photo.file_id})
        file_name = response.json()["result"]["file_path"].split('/')[-1] if response.status_code == 200 else ("P00" + str(message.id) + ".jpg")
        file = {
            "id": message.photo.file_id,
            "name": file_name ,
            "size": message.photo.file_size,
            "type": mimetypes.guess_type(file_name)[0],
            "msgId": str(message.id),
            "thumbId": message.photo.thumbs[-1].file_id
        }
    elif (message.video):
        file = {
            "id": message.video.file_id,
            "name": message.video.file_name,
            "size": message.video.file_size,
            "type": message.video.mime_type,
            "msgId": message.id,
            "thumbId": message.video.thumbs[-1].file_id
        }

    try:
        res = File.prisma().create(data={
            "ownerId": message.from_user.id,
            "path": "/",
            **file
        })
        logger.info("Added file: " + res.id + ". Type: " + res.type)
    except Exception as e:
        logger.error(e)