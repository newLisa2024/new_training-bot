import telebot
import os
import subprocess
from openai import OpenAI
from config import BOT_TOKEN, WHISPER_API

# Ваш API ключ для OpenAI
OPENAI_API_KEY = WHISPER_API
client = OpenAI(api_key=OPENAI_API_KEY)

# Ваш токен для бота Telegram
TELEGRAM_BOT_TOKEN = BOT_TOKEN
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Укажите полный путь к ffmpeg.exe
FFMPEG_PATH = "C:\\Users\\buddy\\AppData\\Local\\ffmpeg\\bin\\ffmpeg.exe"


# Создание папки для аудиофайлов
audio_folder = os.path.join(os.path.dirname(__file__), "user_voice_messages")
os.makedirs(audio_folder, exist_ok=True)


# Функция для проверки доступности ffmpeg
# def check_ffmpeg():
#     result = subprocess.run([FFMPEG_PATH, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     if result.returncode != 0:
#         raise EnvironmentError(f"ffmpeg не найден или произошла ошибка при выполнении: {result.stderr}")
#     print("ffmpeg успешно найден.")
# check_ffmpeg()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне голосовое сообщение, и я его транскрибирую для тебя.")


@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = message.from_user.id

    try:
        # Скачиваем голосовое сообщение
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Сохраняем голосовое сообщение во временный файл
        ogg_file_path = os.path.join(audio_folder, f"voice_message_{user_id}.ogg")
        mp3_file_path = os.path.join(audio_folder, f"voice_message_{user_id}.mp3")

        with open(ogg_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Преобразуем формат файла из ogg в mp3
        subprocess.run([FFMPEG_PATH, "-i", ogg_file_path, mp3_file_path], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       text=True, timeout=30)

        # Открываем mp3 файл для транскрипции
        with open(mp3_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                prompt="The recorded message is in Russian, but it is "
                       "a response to interview questions for a Python "
                       "programmer position. It includes professional "
                       "terminology in English related to Python and HR "
                       "for Python programmer candidates. Transcribe this"
                       " terminology in English. All words that are not"
                       " terminology should be transcribed in Russian."
            )

        # Отправляем транскрибированный текст пользователю
        bot.reply_to(message, transcription.text)

    except Exception as e:
        # Обработка любых ошибок
        bot.reply_to(message, "Ошибка транскрибации. Попробуйте записать сообщение снова либо введите текст.")
        print(f"Произошла ошибка: {e}")

    finally:
        # Удаляем временные файлы
        if os.path.exists(ogg_file_path):
            os.remove(ogg_file_path)
        if os.path.exists(mp3_file_path):
            os.remove(mp3_file_path)


# Запуск бота
bot.polling(none_stop=True)