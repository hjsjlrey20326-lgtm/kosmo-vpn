# botvpn.py — обновлённый текст для кнопок оплаты
# Теперь бот не ждёт скриншоты, а отправляет клиента инструкцию — прислать скриншот админу

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    users = load_users()
    
# botvpn.py — обновлённый текст для кнопок оплаты
# Теперь бот не ждёт скриншоты, а отправляет клиента инструкцию — прислать скриншот админу

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    users = load_users()
    
    if call.data == "buy_day":
        bot.answer_callback_query(call.id, "Оплата: 3₽")
        bot.send_message(
            user_id,
            "💎 **Оплата подписки KosmoVPN**\n\n"
            "1. Переведите **3₽** на карту: **2202 2088 0504 7264**\n"
            "2. В комментарии к переводу укажите свой **Telegram ID** (узнать через @userinfobot)\n"
            "3. Сделайте **скриншот чека** и отправьте его **сюда → @Shef_Carry0**\n\n"
            "После проверки вам придёт ссылка с подпиской."
        )
    
    elif call.data == "buy_month":
        bot.answer_callback_query(call.id, "Оплата: 50₽")
        bot.send_message(
            user_id,
            "💎 **Оплата подписки KosmoVPN**\n\n"
            "1. Переведите **50₽** на карту: **2202 2088 0504 7264**\n"
            "2. В комментарии к переводу укажите свой **Telegram ID** (узнать через @userinfobot)\n"
            "3. Сделайте **скриншот чека** и отправьте его **сюда → @Shef_Carry0**\n\n"
            "После проверки вам придёт ссылка с подпиской."
        )
    
    elif call.data == "buy_year":
        bot.answer_callback_query(call.id, "Оплата: 500₽")
        bot.send_message(
            user_id,
            "💎 **Оплата подписки KosmoVPN**\n\n"
            "1. Переведите **500₽** на карту: **2202 2088 0504 7264**\n"
            "2. В комментарии к переводу укажите свой **Telegram ID** (узнать через @userinfobot)\n"
            "3. Сделайте **скриншот чека** и отправьте его **сюда → @Shef_Carry0**\n\n"
            "После проверки вам придёт ссылка с подпиской."
        )
