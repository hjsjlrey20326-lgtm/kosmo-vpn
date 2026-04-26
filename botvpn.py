# bot.py — Modeo VPN Telegram бот
import os
import telebot
import time
import hmac
import hashlib
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# === НАСТРОЙКИ (ЗАПОЛНЕНО) ===
TOKEN = "YOUR_BOT_TOKEN"           # Замени на токен от @BotFather
ADMIN_IDS = [8420222491, 8688518887]  # Список админов
WORKER_URL = "https://modeo-worker.workers.dev/sub"  # Без ?token=
SECRET_KEY = "ModeoVPN_2026_S3cr3t_K3y_xK9#2mP!qR7@vL8$wN5&tY4"
PRICE_DAY = 50
PRICE_MONTH = 300
PRICE_YEAR = 1500

CARD_NUMBER = "2202 2088 0504 7264"
SCREENSHOT_USERS = ["@Shef_Carry0", "@godSof"]

bot = telebot.TeleBot(TOKEN)

# === ГЕНЕРАЦИЯ ТОКЕНА ===
def generate_token(user_id, days):
    expires_ms = int((time.time() + days * 86400) * 1000)
    data = f"{user_id}_{expires_ms}"
    signature = hmac.new(SECRET_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()[:16]
    token = f"{user_id}_{expires_ms}_{signature}"
    return f"{WORKER_URL}?token={token}"

# === КНОПКИ ===
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📱 День (50₽)", callback_data="day"),
        InlineKeyboardButton("📱 Месяц (300₽)", callback_data="month"),
        InlineKeyboardButton("📱 Год (1500₽)", callback_data="year"),
        InlineKeyboardButton("📋 Моя подписка", callback_data="my"),
        InlineKeyboardButton("❓ Помощь", callback_data="help")
    )
    bot.send_message(message.chat.id, "💎 Modeo VPN\nВыбери тариф:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "day":
        bot.answer_callback_query(call.id, "Оплата 50₽")
        text = (f"Оплатите 50₽ на карту:\n`{CARD_NUMBER}`\n\n"
                f"После оплаты отправьте скриншот чека сюда или в личку:\n"
                + ", ".join(SCREENSHOT_USERS))
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif call.data == "month":
        bot.answer_callback_query(call.id, "Оплата 300₽")
        text = (f"Оплатите 300₽ на карту:\n`{CARD_NUMBER}`\n\n"
                f"После оплаты отправьте скриншот чека сюда или в личку:\n"
                + ", ".join(SCREENSHOT_USERS))
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif call.data == "year":
        bot.answer_callback_query(call.id, "Оплата 1500₽")
        text = (f"Оплатите 1500₽ на карту:\n`{CARD_NUMBER}`\n\n"
                f"После оплаты отправьте скриншот чека сюда или в личку:\n"
                + ", ".join(SCREENSHOT_USERS))
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif call.data == "my":
        bot.send_message(call.message.chat.id, "Напишите админу для проверки подписки")
    elif call.data == "help":
        help_text = ("📌 Инструкция:\n"
                     "1. Выберите тариф.\n"
                     "2. Переведите сумму на карту.\n"
                     "3. Отправьте скриншот чека @Shef_Carry0 или @godSof.\n"
                     "4. Админ подтвердит и выдаст ссылку.\n\n"
                     "Приложения: v2rayNG / NekoBox / Sing-Box / Shadowrocket\n"
                     "Добавьте полученную ссылку как подписку.")
        bot.send_message(call.message.chat.id, help_text)

# === АДМИН: ПОДТВЕРЖДЕНИЕ ОПЛАТЫ ===
@bot.message_handler(commands=['confirm'])
def confirm(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "Нет прав")
        return
    # Формат: /confirm user_id дни
    try:
        _, user_id_str, days_str = message.text.split()
        user_id = int(user_id_str)
        days = int(days_str)
        link = generate_token(user_id, days)
        bot.send_message(user_id, f"✅ Подписка Modeo VPN активирована на {days} дней!\nСсылка:\n`{link}`", parse_mode="Markdown")
        bot.reply_to(message, f"Пользователю {user_id} выдана ссылка на {days} дней")
    except:
        bot.reply_to(message, "Ошибка. Используй: /confirm user_id дни")

print("Modeo VPN бот запущен")
bot.infinity_polling()
