import telebot
import random
import json
import os
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = "players.json"
GITHUB_RAW = "https://raw.githubusercontent.com/neptoon715-alt/phone-bot/main/"
GIFT_COOLDOWN = 86400  # 24 часа в секундах

PHONES = {
    "common": [
        {"name": "Nokia 3310", "price": 63, "img": "Nokia3300.jpg"},
        {"name": "Nokia 1100", "price": 50, "img": "nokia1100.jpg"},
        {"name": "Motorola C115", "price": 56, "img": "Motorola_C115_life.jpg"},
        {"name": "Samsung E250", "price": 75, "img": "Samsung_E1200.jpg"},
        {"name": "Sony Ericsson K300", "price": 69, "img": "Sony_Ericsson_J100a.jpg"},
        {"name": "Alcatel OT-103", "price": 44, "img": "s-l400.jpg"},
        {"name": "LG C1100", "price": 63, "img": "LG_C1100.jpg"},
        {"name": "Siemens A60", "price": 50, "img": "Siemens_A60.jpg"},
        {"name": "Nokia 2600", "price": 56, "img": "nokia1100.jpg"},
        {"name": "Samsung E1200", "price": 53, "img": "Samsung_E1200.jpg"},
        {"name": "Sony Ericsson J100", "price": 45, "img": "Sony_Ericsson_J100a.jpg"},
        {"name": "Motorola W220", "price": 48, "img": "Motorola_C115_life.jpg"},
    ],
    "rare": [
        {"name": "iPhone 4", "price": 250, "img": "iphone-4.jpg"},
        {"name": "Samsung Galaxy S3", "price": 225, "img": "galaxy3.webp"},
        {"name": "HTC One M7", "price": 238, "img": "HTC-ONE-M7.jpg"},
        {"name": "Sony Xperia Z", "price": 219, "img": "SonyXperiaZ.webp"},
        {"name": "Nokia Lumia 920", "price": 200, "img": "nokia-lumia-920_1.jpg"},
        {"name": "BlackBerry Bold 9900", "price": 275, "img": "s-l1200.jpg"},
        {"name": "Motorola Razr V3", "price": 188, "img": "Motorola_C115_life.jpg"},
        {"name": "iPhone 3GS", "price": 213, "img": "Apple_iPhone_3GS.jpg"},
        {"name": "Samsung Galaxy Note 2", "price": 263, "img": "galaxynote2.webp"},
        {"name": "HTC Desire HD", "price": 206, "img": "30_p_DesireHD2.jpg"},
        {"name": "LG G2", "price": 231, "img": "LGG2.webp"},
        {"name": "Sony Xperia T", "price": 215, "img": "orig-sony-xperia-t-main.jpg"},
    ],
    "legendary": [
        {"name": "iPhone 15 Pro Max", "price": 1500, "img": "iphone15promax.webp"},
        {"name": "Samsung Galaxy S24 Ultra", "price": 1375, "img": "galaxys24ultra.webp"},
        {"name": "Google Pixel 8 Pro", "price": 1188, "img": "GooglePixel8Pro1.jpg"},
        {"name": "OnePlus 12", "price": 1000, "img": "OnePlusHasselblad.jpg"},
        {"name": "Xiaomi 14 Ultra", "price": 1125, "img": "xiaomi-14-ultra.jpg"},
        {"name": "iPhone 14 Pro", "price": 1250, "img": "iphone14pro.webp"},
        {"name": "Samsung Galaxy Z Fold 5", "price": 1875, "img": "SamsungGalaxyZFold 5.jpg"},
        {"name": "Sony Xperia 1 V", "price": 1063, "img": "p1.jpg"},
        {"name": "ASUS ROG Phone 7", "price": 1313, "img": "ASUS ROG Phone 7 Ultimate.jpg"},
        {"name": "Xiaomi Mix Fold 3", "price": 1625, "img": "XiaomiMixFold.jpg"},
    ],
    "mythic": [
        {"name": "iPhone 15 Pro Max Titanium", "price": 6250, "img": "iphone15promaxtitan.webp"},
        {"name": "Samsung Galaxy S24 Ultra Gold", "price": 6000, "img": "galaxys24ultragold.webp"},
        {"name": "Vertu Signature Touch", "price": 7500, "img": "s-l1200.jpg"},
        {"name": "Xiaomi 14 Ultra Photography", "price": 5625, "img": "Xiaomi_14_Ultra_Photography.jpg"},
        {"name": "Google Pixel 8 Pro Special", "price": 5250, "img": "GooglePixel8Pro1.jpg"},
        {"name": "OnePlus 12 Hasselblad Edition", "price": 5875, "img": "OnePlusHasselblad.jpg"},
    ],
    "secret": [
        {"name": "Nokia Morph", "price": 199999, "img": "nokiam.jpg"},
        {"name": "iPhone Proto 2007 (прототип)", "price": 62500, "img": None},
        {"name": "Nokia 7700 (отменён)", "price": 45000, "img": None},
        {"name": "Samsung Galaxy Fold Zero", "price": 75000, "img": None},
        {"name": "Apple Leonardo (засекречен)", "price": 124999, "img": None},
        {"name": "Google Pixel Ultra Secret", "price": 68750, "img": None},
    ]
}

RARITY_CHANCE = {"common": 50, "rare": 28, "legendary": 15, "mythic": 6, "secret": 1}
RARITY_EMOJI = {"common": "⚪", "rare": "🔵", "legendary": "🟡", "mythic": "🔴", "secret": "🌟"}
RARITY_NAME = {"common": "Обычный", "rare": "Редкий", "legendary": "Легендарный", "mythic": "Мифический", "secret": "Секретный"}


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_player(user_id):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"balance": 500, "inventory": [], "notifications": True, "last_gift": 0}
        save_data(data)
    if "last_gift" not in data[uid]:
        data[uid]["last_gift"] = 0
        save_data(data)
    return data[uid]


def update_player(user_id, player):
    data = load_data()
    data[str(user_id)] = player
    save_data(data)


def roll_phone():
    roll = random.randint(1, 100)
    if roll <= RARITY_CHANCE["secret"]:
        rarity = "secret"
    elif roll <= RARITY_CHANCE["secret"] + RARITY_CHANCE["mythic"]:
        rarity = "mythic"
    elif roll <= RARITY_CHANCE["secret"] + RARITY_CHANCE["mythic"] + RARITY_CHANCE["legendary"]:
        rarity = "legendary"
    elif roll <= RARITY_CHANCE["secret"] + RARITY_CHANCE["mythic"] + RARITY_CHANCE["legendary"] + RARITY_CHANCE["rare"]:
        rarity = "rare"
    else:
        rarity = "common"
    phone = random.choice(PHONES[rarity]).copy()
    phone["rarity"] = rarity
    return phone


def send_phone_card(chat_id, phone, caption):
    img = phone.get("img")
    if img:
        url = GITHUB_RAW + img
        try:
            bot.send_photo(chat_id, url, caption=caption, parse_mode="Markdown")
            return
        except:
            pass
    bot.send_message(chat_id, caption, parse_mode="Markdown")


def get_shop_price(phone):
    return phone["price"] * 2


@bot.message_handler(commands=["start"])
def start(message):
    player = get_player(message.from_user.id)
    bot.reply_to(message,
        f"📱 *Добро пожаловать в Phone Simulator!*\n\n"
        f"💰 Твой стартовый баланс: *{player['balance']} монет*\n\n"
        f"*Редкости:*\n"
        f"⚪ Обычный — 50%\n"
        f"🔵 Редкий — 28%\n"
        f"🟡 Легендарный — 15%\n"
        f"🔴 Мифический — 6%\n"
        f"🌟 Секретный — 1%\n\n"
        f"*Команды:*\n"
        f"/card — получить случайный телефон\n"
        f"/sell — продать телефон\n"
        f"/inventory — посмотреть все телефоны\n"
        f"/balance — посмотреть баланс\n"
        f"/shop — магазин телефонов\n"
        f"/gift — ежедневный подарок\n"
        f"/top — топ 10 игроков\n"
        f"/vip — VIP статус\n"
        f"/settings — настройки\n"
        f"/info — информация о боте\n"
        f"/iolpa_get — получить любой телефон",
        parse_mode="Markdown"
    )


@bot.message_handler(commands=["gift"])
def gift(message):
    player = get_player(message.from_user.id)
    now = time.time()
    last = player.get("last_gift", 0)
    diff = now - last

    if diff < GIFT_COOLDOWN:
        remaining = GIFT_COOLDOWN - diff
        hours = int(remaining // 3600)
        minutes = int((remaining % 3600) // 60)
        bot.reply_to(message,
            f"⏳ *Подарок уже получен!*\n\n"
            f"Следующий подарок через: *{hours}ч {minutes}м*",
            parse_mode="Markdown"
        )
        return

    # Дать монеты (VIP получает вдвое больше)
    coins = 6000 if player.get("vip", False) else 3000
    player["balance"] += coins

    # Дать случайный редкий телефон
    phone = random.choice(PHONES["rare"]).copy()
    phone["rarity"] = "rare"
    player["inventory"].append(phone)
    player["last_gift"] = now
    update_player(message.from_user.id, player)

    emoji = RARITY_EMOJI["rare"]
    vip_bonus = " *(VIP x2)*" if player.get("vip", False) else ""
    caption = (
        f"🎁 *Ежедневный подарок!*\n\n"
        f"💰 +{coins} монет{vip_bonus}\n"
        f"{emoji} *{phone['name']}* добавлен в инвентарь!\n\n"
        f"💰 Твой баланс: *{player['balance']} монет*\n\n"
        f"_Возвращайся завтра за новым подарком!_"
    )
    send_phone_card(message.chat.id, phone, caption)


@bot.message_handler(commands=["obxod_gift"])
def obxod_gift(message):
    player = get_player(message.from_user.id)
    player["last_gift"] = 0
    update_player(message.from_user.id, player)
    bot.reply_to(message, "✅ *Таймер сброшен! Можешь получить подарок снова!*", parse_mode="Markdown")


@bot.message_handler(commands=["top"])
def top(message):
    data = load_data()
    if not data:
        bot.reply_to(message, "🏆 Пока нет игроков!", parse_mode="Markdown")
        return

    players_list = []
    for uid, player in data.items():
        name = f"id{uid}"
        try:
            chat = bot.get_chat(int(uid))
            name = chat.first_name or f"id{uid}"
            if chat.username:
                name = f"@{chat.username}"
        except:
            pass
        vip = "👑 " if player.get("vip", False) else ""
        players_list.append((player.get("balance", 0), vip, name))

    players_list.sort(reverse=True)
    top10 = players_list[:10]

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    lines = ["🏆 *Топ 10 игроков:*\n"]
    for i, (balance, vip, name) in enumerate(top10):
        lines.append(f"{medals[i]} {vip}{name} — *{balance} монет*")

    bot.reply_to(message, "\n".join(lines), parse_mode="Markdown")


@bot.message_handler(commands=["vip"])
def vip(message):
    player = get_player(message.from_user.id)
    balance = player["balance"]

    if player.get("vip", False):
        bot.reply_to(message,
            f"👑 *Ты уже VIP игрок!*\n\n"
            f"_Спасибо за поддержку!_ 🎉",
            parse_mode="Markdown"
        )
        return

    if balance >= 400000:
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            telebot.types.InlineKeyboardButton("✅ Купить за 400к монет", callback_data="vip_buy"),
            telebot.types.InlineKeyboardButton("❌ Отмена", callback_data="vip_cancel"),
        )
        bot.reply_to(message,
            f"👑 *VIP статус*\n\n"
            f"💰 Стоимость: *400 000 монет*\n"
            f"💳 Твой баланс: *{balance} монет*\n\n"
            f"*Преимущества VIP:*\n"
            f"⭐ Значок 👑 в профиле\n"
            f"🎁 Двойной ежедневный подарок\n"
            f"✨ Особый статус игрока",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    else:
        needed = 400000 - balance
        bot.reply_to(message,
            f"👑 *VIP статус*\n\n"
            f"Заработайте 400к монет или напишите @advecrd !\n\n"
            f"💰 Твой баланс: *{balance} монет*\n"
            f"📈 Осталось накопить: *{needed} монет*",
            parse_mode="Markdown"
        )


@bot.callback_query_handler(func=lambda call: call.data == "vip_buy")
def vip_buy(call):
    player = get_player(call.from_user.id)
    if player["balance"] < 400000:
        bot.answer_callback_query(call.id, "❌ Недостаточно монет!")
        return
    player["balance"] -= 400000
    player["vip"] = True
    update_player(call.from_user.id, player)
    bot.answer_callback_query(call.id, "👑 Добро пожаловать в VIP!")
    bot.edit_message_text(
        f"👑 *Поздравляем! Ты теперь VIP игрок!*\n\n"
        f"💰 Остаток баланса: *{player['balance']} монет*\n\n"
        f"_Спасибо за поддержку!_ 🎉",
        call.message.chat.id, call.message.message_id,
        parse_mode="Markdown"
    )


@bot.callback_query_handler(func=lambda call: call.data == "vip_cancel")
def vip_cancel(call):
    bot.answer_callback_query(call.id, "Отменено")
    bot.edit_message_text("❌ *Покупка VIP отменена*", call.message.chat.id, call.message.message_id, parse_mode="Markdown")


@bot.message_handler(commands=["info"])
def info(message):
    bot.reply_to(message,
        f"📱 *Phone Simulator*\n\n"
        f"👨‍💻 *Автор:* @advecrd\n"
        f"💻 *Код писал:* @advecrd\n"
        f"🎨 *Дизайнер и бета тестер:* @Rozetka468\n\n"
        f"📅 *Дата начала разработки:* 04.03.2026\n\n"
        f"_Спасибо что играешь!_ 🎉",
        parse_mode="Markdown"
    )


@bot.message_handler(commands=["settings"])
def settings(message):
    player = get_player(message.from_user.id)
    notif = "✅ Вкл" if player.get("notifications", True) else "❌ Выкл"

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        telebot.types.InlineKeyboardButton(f"🔔 Уведомления: {notif}", callback_data="set_notif"),
        telebot.types.InlineKeyboardButton("🗑 Очистить инвентарь", callback_data="set_clear"),
        telebot.types.InlineKeyboardButton("📊 Моя статистика", callback_data="set_stats"),
    )
    bot.reply_to(message,
        f"⚙️ *Настройки*\n\n"
        f"🔔 Уведомления: {notif}\n"
        f"💰 Баланс: {player['balance']} монет\n"
        f"📦 Телефонов: {len(player['inventory'])} шт.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


@bot.callback_query_handler(func=lambda call: call.data == "set_notif")
def toggle_notif(call):
    player = get_player(call.from_user.id)
    player["notifications"] = not player.get("notifications", True)
    update_player(call.from_user.id, player)
    notif = "✅ Вкл" if player["notifications"] else "❌ Выкл"
    bot.answer_callback_query(call.id, f"Уведомления: {notif}")
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        telebot.types.InlineKeyboardButton(f"🔔 Уведомления: {notif}", callback_data="set_notif"),
        telebot.types.InlineKeyboardButton("🗑 Очистить инвентарь", callback_data="set_clear"),
        telebot.types.InlineKeyboardButton("📊 Моя статистика", callback_data="set_stats"),
    )
    bot.edit_message_text(
        f"⚙️ *Настройки*\n\n"
        f"🔔 Уведомления: {notif}\n"
        f"💰 Баланс: {player['balance']} монет\n"
        f"📦 Телефонов: {len(player['inventory'])} шт.",
        call.message.chat.id, call.message.message_id,
        reply_markup=keyboard, parse_mode="Markdown"
    )


@bot.callback_query_handler(func=lambda call: call.data == "set_clear")
def clear_inventory(call):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        telebot.types.InlineKeyboardButton("✅ Да, очистить", callback_data="set_clear_yes"),
        telebot.types.InlineKeyboardButton("❌ Нет", callback_data="set_clear_no"),
    )
    bot.edit_message_text(
        "⚠️ *Ты уверен что хочешь очистить инвентарь?*\nВсе телефоны будут удалены!",
        call.message.chat.id, call.message.message_id,
        reply_markup=keyboard, parse_mode="Markdown"
    )


@bot.callback_query_handler(func=lambda call: call.data == "set_clear_yes")
def clear_yes(call):
    player = get_player(call.from_user.id)
    player["inventory"] = []
    update_player(call.from_user.id, player)
    bot.answer_callback_query(call.id, "✅ Инвентарь очищен!")
    bot.edit_message_text("🗑 *Инвентарь очищен!*", call.message.chat.id, call.message.message_id, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == "set_clear_no")
def clear_no(call):
    bot.answer_callback_query(call.id, "Отменено")
    player = get_player(call.from_user.id)
    notif = "✅ Вкл" if player.get("notifications", True) else "❌ Выкл"
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        telebot.types.InlineKeyboardButton(f"🔔 Уведомления: {notif}", callback_data="set_notif"),
        telebot.types.InlineKeyboardButton("🗑 Очистить инвентарь", callback_data="set_clear"),
        telebot.types.InlineKeyboardButton("📊 Моя статистика", callback_data="set_stats"),
    )
    bot.edit_message_text(
        f"⚙️ *Настройки*\n\n🔔 Уведомления: {notif}\n💰 Баланс: {player['balance']} монет\n📦 Телефонов: {len(player['inventory'])} шт.",
        call.message.chat.id, call.message.message_id,
        reply_markup=keyboard, parse_mode="Markdown"
    )


@bot.callback_query_handler(func=lambda call: call.data == "set_stats")
def show_stats(call):
    player = get_player(call.from_user.id)
    total = sum(p["price"] for p in player["inventory"])
    rarities = {}
    for phone in player["inventory"]:
        r = phone.get("rarity", "common")
        rarities[r] = rarities.get(r, 0) + 1
    lines = ["📊 *Твоя статистика:*\n"]
    lines.append(f"💰 Баланс: *{player['balance']} монет*")
    lines.append(f"📦 Телефонов: *{len(player['inventory'])} шт.*")
    lines.append(f"💵 Стоимость коллекции: *{total} монет*")
    if rarities:
        lines.append("\n*По редкостям:*")
        for rarity, count in rarities.items():
            emoji = RARITY_EMOJI.get(rarity, "⚪")
            lines.append(f"{emoji} {RARITY_NAME.get(rarity, rarity)}: {count} шт.")
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("◀️ Назад", callback_data="set_back"))
    bot.edit_message_text("\n".join(lines), call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == "set_back")
def set_back(call):
    player = get_player(call.from_user.id)
    notif = "✅ Вкл" if player.get("notifications", True) else "❌ Выкл"
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        telebot.types.InlineKeyboardButton(f"🔔 Уведомления: {notif}", callback_data="set_notif"),
        telebot.types.InlineKeyboardButton("🗑 Очистить инвентарь", callback_data="set_clear"),
        telebot.types.InlineKeyboardButton("📊 Моя статистика", callback_data="set_stats"),
    )
    bot.edit_message_text(
        f"⚙️ *Настройки*\n\n🔔 Уведомления: {notif}\n💰 Баланс: {player['balance']} монет\n📦 Телефонов: {len(player['inventory'])} шт.",
        call.message.chat.id, call.message.message_id,
        reply_markup=keyboard, parse_mode="Markdown"
    )


@bot.message_handler(commands=["balance"])
def balance(message):
    player = get_player(message.from_user.id)
    bot.reply_to(message, f"💰 Твой баланс: *{player['balance']} монет*", parse_mode="Markdown")


@bot.message_handler(commands=["card"])
def card(message):
    player = get_player(message.from_user.id)
    phone = roll_phone()
    player["inventory"].append(phone)
    update_player(message.from_user.id, player)
    emoji = RARITY_EMOJI[phone["rarity"]]
    rarity_name = RARITY_NAME[phone["rarity"]]
    caption = (
        f"🎰 *Выпал телефон!*\n\n"
        f"{emoji} *{phone['name']}*\n"
        f"Редкость: {rarity_name}\n"
        f"Цена продажи: *{phone['price']} монет*\n\n"
        f"Используй /sell чтобы продать его!"
    )
    send_phone_card(message.chat.id, phone, caption)


@bot.message_handler(commands=["sell"])
def sell(message):
    player = get_player(message.from_user.id)
    if not player["inventory"]:
        bot.reply_to(message, "❌ У тебя нет телефонов! Используй /card чтобы получить телефон.")
        return
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    for i, phone in enumerate(player["inventory"]):
        emoji = RARITY_EMOJI[phone["rarity"]]
        keyboard.add(telebot.types.InlineKeyboardButton(
            f"{emoji} {phone['name']} — {phone['price']} монет",
            callback_data=f"sell_{i}"
        ))
    bot.reply_to(message, "💵 *Выбери телефон для продажи:*", reply_markup=keyboard, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data.startswith("sell_"))
def do_sell(call):
    index = int(call.data[5:])
    player = get_player(call.from_user.id)
    if index >= len(player["inventory"]):
        bot.answer_callback_query(call.id, "❌ Телефон не найден!")
        return
    phone = player["inventory"].pop(index)
    player["balance"] += phone["price"]
    update_player(call.from_user.id, player)
    emoji = RARITY_EMOJI[phone["rarity"]]
    bot.answer_callback_query(call.id, f"✅ Продано за {phone['price']} монет!")
    bot.send_message(call.message.chat.id,
        f"✅ *Продано!*\n\n{emoji} *{phone['name']}* продан за *{phone['price']} монет*\n💰 Твой баланс: *{player['balance']} монет*",
        parse_mode="Markdown"
    )


@bot.message_handler(commands=["inventory"])
def inventory(message):
    player = get_player(message.from_user.id)
    if not player["inventory"]:
        bot.reply_to(message, "📦 Твой инвентарь пуст. Используй /card!")
        return
    lines = [f"📦 *Твои телефоны ({len(player['inventory'])} шт.):*\n"]
    for i, phone in enumerate(player["inventory"], 1):
        emoji = RARITY_EMOJI[phone["rarity"]]
        lines.append(f"{i}. {emoji} {phone['name']} — {phone['price']} монет")
    total = sum(p["price"] for p in player["inventory"])
    lines.append(f"\n💵 Общая стоимость: *{total} монет*")
    lines.append(f"💰 Баланс: *{player['balance']} монет*")
    bot.reply_to(message, "\n".join(lines), parse_mode="Markdown")


@bot.message_handler(commands=["shop"])
def shop(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    for rarity in ["common", "rare", "legendary", "mythic", "secret"]:
        emoji = RARITY_EMOJI[rarity]
        keyboard.add(telebot.types.InlineKeyboardButton(f"{emoji} {RARITY_NAME[rarity]}", callback_data=f"shop_{rarity}"))
    bot.reply_to(message, "🛒 *Магазин телефонов!*\nВыбери категорию:", reply_markup=keyboard, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data.startswith("shop_") and not call.data.startswith("shop_buy_") and call.data != "shop_back")
def show_shop_rarity(call):
    rarity = call.data[5:]
    player = get_player(call.from_user.id)
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    for phone in PHONES[rarity]:
        emoji = RARITY_EMOJI[rarity]
        shop_price = get_shop_price(phone)
        keyboard.add(telebot.types.InlineKeyboardButton(f"{emoji} {phone['name']} — {shop_price} монет", callback_data=f"shop_buy_{phone['name']}"))
    keyboard.add(telebot.types.InlineKeyboardButton("◀️ Назад", callback_data="shop_back"))
    bot.edit_message_text(
        f"🛒 *Магазин — {RARITY_NAME[rarity]}:*\n💰 Твой баланс: *{player['balance']} монет*",
        call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode="Markdown"
    )


@bot.callback_query_handler(func=lambda call: call.data == "shop_back")
def shop_back(call):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    for rarity in ["common", "rare", "legendary", "mythic", "secret"]:
        emoji = RARITY_EMOJI[rarity]
        keyboard.add(telebot.types.InlineKeyboardButton(f"{emoji} {RARITY_NAME[rarity]}", callback_data=f"shop_{rarity}"))
    bot.edit_message_text("🛒 *Магазин телефонов!*\nВыбери категорию:", call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data.startswith("shop_buy_"))
def buy_phone(call):
    phone_name = call.data[9:]
    player = get_player(call.from_user.id)
    found_phone = None
    for rarity, phones in PHONES.items():
        for phone in phones:
            if phone["name"] == phone_name:
                found_phone = phone.copy()
                found_phone["rarity"] = rarity
                break
    if found_phone:
        shop_price = get_shop_price(found_phone)
        if player["balance"] < shop_price:
            bot.answer_callback_query(call.id, f"❌ Недостаточно монет! Нужно {shop_price} монет")
            return
        player["balance"] -= shop_price
        player["inventory"].append(found_phone)
        update_player(call.from_user.id, player)
        emoji = RARITY_EMOJI[found_phone["rarity"]]
        bot.answer_callback_query(call.id, f"✅ Куплено за {shop_price} монет!")
        caption = f"🛒 *Куплено!*\n\n{emoji} *{found_phone['name']}*\n💸 Потрачено: *{shop_price} монет*\n💰 Остаток: *{player['balance']} монет*"
        send_phone_card(call.message.chat.id, found_phone, caption)


@bot.message_handler(commands=["iolpa_get"])
def iolpa_get(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    for rarity in ["common", "rare", "legendary", "mythic", "secret"]:
        emoji = RARITY_EMOJI[rarity]
        keyboard.add(telebot.types.InlineKeyboardButton(f"{emoji} {RARITY_NAME[rarity]}", callback_data=f"menu_{rarity}"))
    bot.reply_to(message, "📱 *Выбери редкость:*", reply_markup=keyboard, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data.startswith("menu_"))
def show_rarity_phones(call):
    rarity = call.data[5:]
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    for phone in PHONES[rarity]:
        emoji = RARITY_EMOJI[rarity]
        keyboard.add(telebot.types.InlineKeyboardButton(f"{emoji} {phone['name']} — {phone['price']} монет", callback_data=f"get_{phone['name']}"))
    keyboard.add(telebot.types.InlineKeyboardButton("◀️ Назад", callback_data="back_menu"))
    bot.edit_message_text(f"📱 *Телефоны — {RARITY_NAME[rarity]}:*", call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == "back_menu")
def back_menu(call):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    for rarity in ["common", "rare", "legendary", "mythic", "secret"]:
        emoji = RARITY_EMOJI[rarity]
        keyboard.add(telebot.types.InlineKeyboardButton(f"{emoji} {RARITY_NAME[rarity]}", callback_data=f"menu_{rarity}"))
    bot.edit_message_text("📱 *Выбери редкость:*", call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data.startswith("get_"))
def give_phone(call):
    phone_name = call.data[4:]
    player = get_player(call.from_user.id)
    found_phone = None
    for rarity, phones in PHONES.items():
        for phone in phones:
            if phone["name"] == phone_name:
                found_phone = phone.copy()
                found_phone["rarity"] = rarity
                break
    if found_phone:
        player["inventory"].append(found_phone)
        update_player(call.from_user.id, player)
        emoji = RARITY_EMOJI[found_phone["rarity"]]
        bot.answer_callback_query(call.id, f"✅ {found_phone['name']} добавлен!")
        caption = f"{emoji} *{found_phone['name']}* добавлен в инвентарь!\n💰 Цена продажи: {found_phone['price']} монет"
        send_phone_card(call.message.chat.id, found_phone, caption)


print("🤖 Бот запущен!")
bot.polling(none_stop=True)
