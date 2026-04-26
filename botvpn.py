# botvpn.py — Telegram бот с токенами (без exposed общей подписки)
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import time
import hmac
import hashlib

# === КОНФИГУРАЦИЯ ===
TOKEN = "8756799246:AAFUKXPb-SFoycVdMbLc4E0hbOW_MdC9clE"
ADMIN_ID = 8688518887
WORKER_URL = "https://raspy-resonance-c3cf.hjsjlrey20326.workers.dev/sub"  # без ?token=
SECRET_KEY = "KosmoVPN_2025_7xH9!mQ2@wR4"  # ЛЮБАЯ ДЛИННАЯ СТРОКА (не потеряй)
PRICE_DAY = 3
PRICE_MONTH = 50
PRICE_YEAR = 500

bot = telebot.TeleBot(TOKEN)
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
        bot.send_message(user_id, "Переведите 3₽ на карту 2202 2088 0504 7264, затем /confirm с фото чека")
    elif call.data == "buy_month":
        bot.answer_callback_query(call.id, "Оплата: 50₽")
        bot.send_message(user_id, "Переведите 50₽ на карту 2202 2088 0504 7264")
    elif call.data == "buy_year":
        bot.answer_callback_query(call.id, "Оплата: 500₽")
        bot.send_message(user_id, "Переведите 500₽ на карту 2202 2088 0504 7264")
    elif call.data == "my_sub":
        users = load_users()
        expires = users.get(str(user_id), {}).get("expires", 0)
        if expires > time.time():
            days_left = int((expires - time.time()) / 86400)
            # Показываем ссылку с токеном (она уже есть в users? но лучше генерировать на лету)
            token_link = generate_token(user_id, max(1, days_left))
            bot.send_message(user_id, f"📋 Ваша подписка\nСсылка: `{token_link}`\nДней осталось: {days_left}\n\nДобавьте эту ссылку в приложение как подписку.", parse_mode="Markdown")
        else:
            bot.send_message(user_id, "❌ Нет активной подписки. /start")
    elif call.data == "help":
        bot.send_message(user_id, "❓ Помощь\n1. Выбери тариф\n2. Оплати\n3. Пришли скриншот\n4. Админ подтвердит", parse_mode="Markdown")

@bot.message_handler(commands=['confirm'])
def confirm_payment(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Нет доступа")
        return
    try:
        _, user_id_str, days_str = message.text.split()
        user_id = int(user_id_str)
        days = int(days_str)
        users = load_users()
        if str(user_id) not in users:
            users[str(user_id)] = {}
        new_expires = time.time() + days * 86400
        users[str(user_id)]["expires"] = new_expires
        save_users(users)
        link = generate_token(user_id, days)
        bot.send_message(user_id, f"✅ Подписка активирована на {days} дней!\nВаша ссылка:\n`{link}`\nДобавьте её в приложение.", parse_mode="Markdown")
        bot.reply_to(message, f"✅ Пользователю {user_id} выдано {days} дней")
    except:
        bot.reply_to(message, "❌ Формат: /confirm user_id дни")

if __name__ == "__main__":
    print("Бот с токенами запущен")
    bot.infinity_polling()
