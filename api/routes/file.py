import json
import io
from flask import Blueprint, Response, request
from utils import get_file_id
from prisma.models import File
from telegram import bot
from utils import logger

fileBlueprint = Blueprint('file', __name__)

@fileBlueprint.route("/", methods=["GET"])
def listFiles():
    ownerId = request.args.get("ownerId")
    path = request.args.get("path")

    if (not ownerId) or (not path):
        return Response("path or ownerId not provided", status=400)

    try:
        files = File.prisma().find_many(where={
            'AND': {
                "ownerId": int(ownerId),
                "path": path
            }
        })
        return Response(
            json.dumps([file.model_dump(exclude=['createdAt']) for file in files]),
            mimetype="application/json",
            status=200
        )
    except Exception as e:
        logger(e)
        return Response("Error retrieving", status=500)

@fileBlueprint.route("/", methods=["POST"])
def upload():
    file = request.files.get("file")
    chatId = request.form.get("chatId")
    path = request.form.get("path")

    if (not file) or (not chatId) or (not path):
        return Response("file, path or chatId not provided", status=400)
    
    memory_file = io.BytesIO()
    memory_file.write(file.stream.read())
    memory_file.name = file.filename
    newFile = {}
    
    try:
        # file size limit is 2GB , 4GB for premium users
        sent = bot.send_document(
            chat_id=chatId,
            document=memory_file,
            force_document=True
        )
        newFile = {
            "id" : sent.document.file_id if sent.document else get_file_id(sent),
            "name" : sent.document.file_name,
            "size" : sent.document.file_size,
            "type" : sent.document.mime_type,
            "msgId" : sent.id,
            "thumbId" : sent.document.thumbs[-1].file_id if sent.document.thumbs else ""
        }
    except Exception as e:
        logger.error(str(e))
        return Response("Error sending to Telegram", status=500)

    try:
        res = File.prisma().create(data={
            "ownerId": int(chatId),
            "path": path,
            **newFile
        })
        logger.info("Added file: " + res.id + ". Type: " + res.type)
        return Response(
            json.dumps(res.model_dump(exclude=['createdAt'])),
            mimetype="application/json",
            status=200
        )
    except Exception as e:
        logger.error(str(e))
        return Response("Error adding to database", status=500)

@fileBlueprint.route("/download/<id>", methods=["GET"])
def get(id):
    try:
        chunk = b""
        for _ in bot.stream_media(message=id):
            chunk+=_
        return Response(
            chunk,
            mimetype="application/octet-stream",
            status=200
        )
    except Exception as e:
        return Response("Error downloading", status=500)