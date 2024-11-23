import telebot
from config import TOKEN
from logic import get_class

API_TOKEN = '<api_token>'

bot = telebot.TeleBot(TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """
Привет!
                 Я бот с ИИ, который помогает классифицировать картинки! 
                 Отправь мне картинку, и я скажу, что на ней нарисовано 😄
""")

@bot.message_handler(content_types='photo')
def handle_photo(message):
    if not message.photo:
        return bot.send_message(message.chat.id, 'Вы забыли загрузить картинку :(')
    
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)

    with open(file_name, 'wb') as file:
        file.write(downloaded_file)

    result = get_class('keras_model.h5', 'labels.txt', file_name)
    bot.send_message(message.chat.id, result)
bot.infinity_polling()