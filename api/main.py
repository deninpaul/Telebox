import json
import io
import threading
from pyrogram import Client, idle, filters
from pyrogram.types import Message
from flask import Flask, Response, request
from prisma import Prisma, register

API_ID = 27825333
API_HASH = "fef7b4762ce730e677ced740576003bf"
BOT_TOKEN = "6586074692:AAHm34l8MHOiRLZm_wlh9lst8cD0r-5kFpc"
CHAT_ID = "deninpaul"

db = Prisma()
db.connect()
register(db)
app = Flask(__name__)

bot = Client(
    "CDN", API_ID, API_HASH,
    bot_token=BOT_TOKEN,
    max_concurrent_transmissions=5,
    no_updates=False,
    in_memory=False
)

def get_file_id(message: Message):
    available_media = ("audio", "photo", "sticker", "animation", "video", "voice", "video_note")
    for kind in available_media:
            media = getattr(message, kind, None)
            if media is not None:
                return media.file_id

@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return Response(
                json.dumps({"error": True, "reason": "No file selected"}),
                mimetype="application/json",
                status=400
            )
        memory_file = io.BytesIO()
        memory_file.write(file.stream.read())
        memory_file.name = file.filename
        # file size limit is 2GB , 4GB for premium users
        sent = bot.send_document(
            chat_id=CHAT_ID,
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


@app.route("/get", methods=["POST", "GET"])
def get():
    if request.method == "POST":
        file_id = request.form.get("file_id")

    elif request.method == "GET":
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

@bot.on_message(filters.document | filters.photo | filters.video)
def user_upload( _ , message):
    file = json.dumps({
        "file_id": message.document.file_id if message.document else get_file_id(message),
        "mime_type": message.document.mime_type if message.document else "application/zip",
        "message_id": message.id
    })
    
    print(file)

@app.route("/test")
def test():
    return Response(bot.get_me().__str__(), mimetype="application/json")

bot.start()
# bot.log_out()
threading.Thread(target=app.run, args=("0.0.0.0", 80,), daemon=True).start()
idle()
