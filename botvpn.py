# botvpn.py — Telegram бот для KosmoVPN (2 админа, новая карта)
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import time
import hmac
import hashlib
import threading
from flask import Flask

# === КОНФИГУРАЦИЯ ===
TOKEN = "8756799246:AAFUKXPb-SFoycVdMbLc4E0hbOW_MdC9clE"
ADMIN_IDS = [8420222491, 8688518887]  # Два админа
WORKER_URL = "https://raspy-resonance-c3cf.hjsjlrey20326.workers.dev/sub"
SECRET_KEY = "KosmoVPN_2025_7xH9!mQ2@wR4"
CARD_NUMBER = "2202 2088 0504 7264"

PRICE_DAY = 3
PRICE_MONTH = 50
PRICE_YEAR = 500

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

DB_FILE = "users.json"

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DB_FILE, 'w') as f:
        json.dump(users, f)

def generate_token(user_id, days):
    expires_ms = int((time.time() + days * 86400) * 1000)
    data = f"{user_id}_{expires_ms}"
    signature = hmac.new(SECRET_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()[:16]
    token = f"{user_id}_{expires_ms}_{signature}"
    return f"{WORKER_URL}?token={token}"

@app.route('/')
def index():
    return "Bot is running", 200

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {"expires": 0}
        save_users(users)

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📱 День (3₽)", callback_data="buy_day"),
        InlineKeyboardButton("📱 Месяц (50₽)", callback_data="buy_month"),
        InlineKeyboardButton("📱 Год (500₽)", callback_data="buy_year"),
        InlineKeyboardButton("📋 Моя подписка", callback_data="my_sub"),
        InlineKeyboardButton("❓ Помощь", callback_data="help")
    )
    bot.send_message(user_id, "💎 **KosmoVPN**\nМеньше ms — лучше, n/a — не работает.\n\nВыбери тариф:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    if call.data == "buy_day":
        bot.answer_callback_query(call.id, "Оплата: 3₽")
        bot.send_message(
            user_id,
            f"💎 **Оплата подписки KosmoVPN**\n\n"
            f"1. Переведите **3₽** на карту: `{CARD_NUMBER}`\n"
            f"2. В комментарии к переводу укажите свой **Telegram ID** (узнать через @userinfobot)\n"
            f"3. Сделайте скриншот чека и отправьте админу.\n\n"
            f"После проверки вам активируют подписку."
        )
    elif call.data == "buy_month":
        bot.answer_callback_query(call.id, "Оплата: 50₽")
        bot.send_message(
            user_id,
            f"💎 **Оплата подписки KosmoVPN**\n\n"
            f"1. Переведите **50₽** на карту: `{CARD_NUMBER}`\n"
            f"2. В комментарии к переводу укажите свой **Telegram ID** (узнать через @userinfobot)\n"
            f"3. Сделайте скриншот чека и отправьте админу.\n\n"
            f"После проверки вам активируют подписку."
        )
    elif call.data == "buy_year":
        bot.answer_callback_query(call.id, "Оплата: 500₽")
        bot.send_message(
            user_id,
            f"💎 **Оплата подписки KosmoVPN**\n\n"
            f"1. Переведите **500₽** на карту: `{CARD_NUMBER}`\n"
            f"2. В комментарии к переводу укажите свой **Telegram ID** (узнать через @userinfobot)\n"
            f"3. Сделайте скриншот чека и отправьте админу.\n\n"
            f"После проверки вам активируют подписку."
        )
    elif call.data == "my_sub":
        users = load_users()
        expires = users.get(str(user_id), {}).get("expires", 0)
        if expires > time.time():
            days_left = int((expires - time.time()) / 86400)
            token_link = generate_token(user_id, max(1, days_left))
            bot.send_message(
                user_id,
                f"📋 **Ваша подписка**\nСсылка: `{token_link}`\nДней осталось: {days_left}\n\nДобавьте эту ссылку в приложение как подписку.",
                parse_mode="Markdown"
            )
        else:
            bot.send_message(user_id, "❌ Нет активной подписки. /start")
    elif call.data == "help":
        bot.send_message(
            user_id,
            "❓ **Помощь**\n\n"
            "1. Выберите тариф\n"
            "2. Оплатите на карту\n"
            "3. Отправьте скриншот чека админу\n"
            "4. Администратор подтвердит и вам придёт ссылка\n\n"
            f"**Карта для оплаты:** `{CARD_NUMBER}`\n\n"
            "**Приложения:**\n"
            "- Android: v2rayNG, NekoBox\n"
            "- iOS: Sing-Box, Shadowrocket\n"
            "- Windows: v2rayN\n\n"
            "**Подписка активируется после проверки оплаты.**",
            parse_mode="Markdown"
        )

@bot.message_handler(commands=['confirm'])
def confirm_payment(message):
    # Проверяем, что отправитель — один из админов
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "❌ Нет доступа")
        return
    
    try:
        _, user_id_str, days_str = message.text.split()
        user_id = int(user_id_str)
        days = int(days_str)
        
        users = load_users()
        if str(user_id) not in users:
            users[str(user_id)] = {}
        
        current_expires = users[str(user_id)].get("expires", 0)
        new_expires = max(current_expires, time.time()) + days * 86400
        users[str(user_id)]["expires"] = new_expires
        save_users(users)
        
        link = generate_token(user_id, days)
        bot.send_message(
            user_id,
            f"✅ Подписка активирована на {days} дней!\nВаша ссылка:\n`{link}`\nДобавьте её в приложение.",
            parse_mode="Markdown"
        )
        bot.reply_to(message, f"✅ Пользователю {user_id} активировано {days} дней")
    except:
        bot.reply_to(message, "❌ Формат: /confirm user_id дни")

@bot.message_handler(commands=['id'])
def get_id(message):
    bot.reply_to(message, f"Ваш Telegram ID: `{message.from_user.id}`", parse_mode="Markdown")

def run_bot():
    print("Бот запущен")
    bot.infinity_polling()

if __name__ == "__main__":
    thread = threading.Thread(target=run_bot)
    thread.start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
