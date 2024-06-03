from dotenv import load_dotenv
import os

load_dotenv()

BOT_NAME = os.getenv('BOT_NAME')
WHISPER_API = os.getenv('WHISPER_API')
BOT_TOKEN = os.getenv('BOT_TOKEN')
PROXY_API = os.getenv('PROXY_API')
STICKER_CAT = os.getenv('STICKER_CAT')
STICKER_SUCCESS = os.getenv('STICKER_SUCCESS')
STICKER_HR = os.getenv('STICKER_HR')

params = ['AB12', 'CD34', 'EF56', 'GH78']