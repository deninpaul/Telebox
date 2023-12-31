import os
from pyrogram import Client
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

bot = Client(
    "CDN", 
    os.getenv('API_ID'), 
    os.getenv('API_HASH'),
    bot_token=os.getenv('BOT_TOKEN'),
    no_updates=False,
    in_memory=True
)

def startBot():
    bot.start()

def stopBot():
    bot.log_out()