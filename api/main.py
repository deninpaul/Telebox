import threading
from flask import Flask, Response
from prisma import Prisma, register
from pyrogram import idle
from routes import userBlueprint, fileBlueprint
from telegram import startBot

db = Prisma()
db.connect()
register(db)

app = Flask(__name__)

app.register_blueprint(userBlueprint, url_prefix='/user')
app.register_blueprint(fileBlueprint, url_prefix='/file')

@app.route("/")
def test():
    return Response("Telebox Server up and running", mimetype="application/json")

startBot()
threading.Thread(target=app.run, args=("0.0.0.0", 80,), daemon=True).start()
idle()
