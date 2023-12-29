import threading
from flask import Flask, Response
from prisma import Prisma, register
from pyrogram import idle
from routes import userBlueprint, fileBlueprint
from telegram import startBot

from utils import get_file_id
from dotenv import load_dotenv

db = Prisma()
db.connect()
register(db)
app = Flask(__name__)
load_dotenv()

app.register_blueprint(userBlueprint, url_prefix='/user')
app.register_blueprint(fileBlueprint, url_prefix='/file')

@app.route("/test")
def test():
    return Response(bot.get_me().__str__(), mimetype="application/json")


startBot()
threading.Thread(target=app.run, args=("0.0.0.0", 80,), daemon=True).start()
idle()
