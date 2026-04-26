# botvpn.py — обновлённый текст для кнопок оплаты
# Теперь бот не ждёт скриншоты, а отправляет клиента инструкцию — прислать скриншот админу

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    users = load_users()
    
