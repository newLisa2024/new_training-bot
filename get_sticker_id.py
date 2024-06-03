@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    sticker_id = message.sticker.file_id
    bot.reply_to(message, f"ID вашего стикера: {sticker_id}")