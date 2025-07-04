from os.path import exists
from sqlite3 import connect

from aiohttp import ClientSession
from pyrogram import Client
from Python_ARQ import ARQ

SESSION_NAME = "Zainu"
DB_NAME = "db.sqlite3"
API_ID = 6
API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
ARQ_API_URL = "https://arq.hamker.dev"

if exists("config.py"):
    from config import *
else:
    from sample_config import *

session = ClientSession()

Zainu = ARQ(ARQ_API_URL, ARQ_API_KEY, session)

conn = connect(DB_NAME)

Zainu = Client(
    SESSION_NAME,
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)
with Zainu:
    bot = Zainu.get_me()
    BOT_ID = bot.id
    BOT_USERNAME = bot.username
