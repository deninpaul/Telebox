import json
import io
from flask import Blueprint, Response, request
from utils import get_file_id
from pyrogram import Client
from prisma.models import File
from telegram import bot

fileBlueprint = Blueprint('file', __name__)

@fileBlueprint.route("/", methods=["POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        chatId = request.form.get("chatId")

        if not file:
            return Response(
                json.dumps({"error": True, "reason": "No file selected"}),
                mimetype="application/json",
                status=400
            )
        
        if not chatId:
            return Response(
                json.dumps({"error": True, "reason": "No chatId provided"}),
                mimetype="application/json",
                status=400
            )
        
        memory_file = io.BytesIO()
        memory_file.write(file.stream.read())
        memory_file.name = file.filename
        # file size limit is 2GB , 4GB for premium users
        sent = bot.send_document(
            chat_id=chatId,
            document=memory_file,
            force_document=True
        )
        return Response(
            json.dumps({
                "file_id": sent.document.file_id if sent.document else get_file_id(sent),
                "mime_type": sent.document.mime_type if sent.document else "application/zip",
                "message_id": sent.id
            }),
            mimetype="application/json",
            status=200
        )

    else:
        return Response(
            json.dumps({"error": True, "reason": "Invalid method"}),
            mimetype="application/json",
            status=400
        )

@fileBlueprint.route("/", methods=["GET"])
def get():
    if request.method == "GET":
        file_id = request.args.get("file_id")

    else:
        return Response(
            json.dumps({"error": True, "reason": "Invalid method"}),
            mimetype="application/json",
            status=400
        )

    if not file_id:
        return Response(
            json.dumps({"error": True, "reason": "file_id is required"}),
            mimetype="application/json",
            status=400
        )

    else:
        try:
            chunk = b""
            for _ in bot.stream_media(message=file_id):
                chunk+=_
            return Response(
                chunk,
                mimetype="application/octet-stream",
                status=200
            )
        except Exception as e:
            return Response(
                json.dumps({"error": True, "reason": str(e)}),
                mimetype="application/json",
                status=400
            )