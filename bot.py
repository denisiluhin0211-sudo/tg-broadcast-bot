import telebot
import time
import json
import os

TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '0'))
bot = telebot.TeleBot(TOKEN)
DB_FILE = 'subscribers.json'

def load_subs():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return []

def save_subs(subs):
    with open(DB_FILE, 'w') as f:
        json.dump(subs, f)

@bot.message_handler(commands=['start'])
def start(message):
    subs = load_subs()
    if message.chat.id not in subs:
        subs.append(message.chat.id)
        save_subs(subs)
        bot.reply_to(message, "Вы подписаны на рассылку!")
    else:
        bot.reply_to(message, "Вы уже подписаны.")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.chat.id != ADMIN_ID:
        return
    text_to_send = message.text.replace('/broadcast ', '')
    if not text_to_send or text_to_send == '/broadcast':
        bot.reply_to(message, "Введите текст после команды.")
        return
    subs = load_subs()
    bot.reply_to(message, f"Начинаю рассылку для {len(subs)} подписчиков...")
    success = 0
    for chat_id in subs:
        try:
            bot.send_message(chat_id, text_to_send)
            success += 1
            time.sleep(0.05)
        except Exception as e:
            print(f"Ошибка для {chat_id}: {e}")
    bot.reply_to(message, f"Готово. Отправлено: {success}/{len(subs)}")

bot.polling(none_stop=True)
