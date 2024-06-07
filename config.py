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
UNIVERSITY_OPEN_API = os.getenv('UNIVERSITY_OPEN_API')
STICKER_THUMBS_UP_CAT = os.getenv('STICKER_THUMBS_UP_CAT')
WINDOWS_FFMPEG_PATH = os.getenv('WINDOWS_FFMPEG_PATH')
LINUX_FFMPEG_PATH = os.getenv('LINUX_FFMPEG_PATH')
PROMPT_CHAT = os.getenv('PROMPT_CHAT')
PROMPT_CHAT_GET_ANSWER = os.getenv('PROMPT_CHAT_GET_ANSWER')


params = ['AB12', 'CD34', 'EF56', 'GH78']
