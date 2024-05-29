import telebot
import os
import subprocess
import openai
import speech_recognition as sr
from config import BOT_TOKEN, WHISPER_API

# Ваш API ключ для OpenAI
OPENAI_API_KEY = WHISPER_API
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Ваш токен для бота Telegram
TELEGRAM_BOT_TOKEN = BOT_TOKEN
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Укажите полный путь к ffmpeg.exe
FFMPEG_PATH = "C:\\Users\\buddy\\AppData\\Local\\ffmpeg\\bin\\ffmpeg.exe"

# Создание папки для аудиофайлов
audio_folder = os.path.join(os.path.dirname(__file__), "user_voice_messages")
os.makedirs(audio_folder, exist_ok=True)


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
        wav_file_path = os.path.join(audio_folder, f"voice_message_{user_id}.wav")

        with open(ogg_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Преобразуем формат файла из ogg в wav
        subprocess.run([FFMPEG_PATH, "-i", ogg_file_path, wav_file_path], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, text=True, timeout=30)

        print("Распознавание речи с использованием speech_recognition...")

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="ru-RU")

        print(f" {text}")
        bot.send_message(user_id, f"Распознанный текст: {text}")

    except Exception as e:
        bot.reply_to(message, "Ошибка транскрибации. Попробуйте записать сообщение снова либо введите текст.")
        print(f"Произошла ошибка: {e}")

    finally:
        # Удаляем временные файлы
        if os.path.exists(ogg_file_path):
            os.remove(ogg_file_path)
        if os.path.exists(wav_file_path):
            os.remove(wav_file_path)


# Запуск бота
bot.polling(none_stop=True)
