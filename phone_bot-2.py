import telebot
import random
import json
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = "players.json"

PHONES = {
    "common": [
        {"name": "Nokia 3310", "price": 50},
        {"name": "Nokia 1100", "price": 40},
        {"name": "Motorola C115", "price": 45},
        {"name": "Samsung E250", "price": 60},
        {"name": "Sony Ericsson K300", "price": 55},
        {"name": "Alcatel OT-103", "price": 35},
        {"name": "LG C1100", "price": 50},
        {"name": "Siemens A60", "price": 40},
        {"name": "Nokia 2600", "price": 45},
        {"name": "Motorola W220", "price": 38},
        {"name": "Samsung E1200", "price": 42},
        {"name": "Sony Ericsson J100", "price": 36},
    ],
    "rare": [
        {"name": "iPhone 4", "price": 200},
        {"name": "Samsung Galaxy S3", "price": 180},
        {"name": "HTC One M7", "price": 190},
        {"name": "Sony Xperia Z", "price": 175},
        {"name": "Nokia Lumia 920", "price": 160},
        {"name": "BlackBerry Bold 9900", "price": 220},
        {"name": "Motorola Razr V3", "price": 150},
        {"name": "iPhone 3GS", "price": 170},
        {"name": "Samsung Galaxy Note 2", "price": 210},
        {"name": "HTC Desire HD", "price": 165},
        {"name": "LG G2", "price": 185},
        {"name": "Sony Xperia T", "price": 172},
    ],
    "legendary": [
        {"name": "iPhone 15 Pro Max", "price": 1200},
        {"name": "Samsung Galaxy S24 Ultra", "price": 1100},
        {"name": "Google Pixel 8 Pro", "price": 950},
        {"name": "OnePlus 12", "price": 800},
        {"name": "Xiaomi 14 Ultra", "price": 900},
        {"name": "iPhone 14 Pro", "price": 1000},
        {"name": "Samsung Galaxy Z Fold 5", "price": 1500},
        {"name": "Sony Xperia 1 V", "price": 850},
        {"name": "ASUS ROG Phone 7", "price": 1050},
        {"name": "Xiaomi Mix Fold 3", "price": 1300},
    ],
    "mythic": [
        {"name": "iPhone 15 Pro Max Titanium", "price": 5000},
        {"name": "Samsung Galaxy S24 Ultra Gold", "price": 4800},
        {"name": "Vertu Signature Touch", "price": 6000},
        {"name": "Xiaomi 14 Ultra Photography", "price": 4500},
        {"name": "Google Pixel 8 Pro Special", "price": 4200},
        {"name": "OnePlus 12 Hasselblad Edition", "price": 4700},
    ],
    "secret": [
        {"name": "iPhone Proto 2007 (прототип)", "price": 50000},
        {"name": "Nokia 7700 (отменён)", "price": 45000},
        {"name": "Samsung Galaxy Fold Zero", "price": 60000},
        {"name": "Apple Leonardo (засекречен)", "price": 99999},
        {"name": "Google Pixel Ultra Secret", "price": 55000},
    ]
}

RARITY_CHANCE = {
    "common": 50,
    "rare": 28,
    "legendary": 15,
    "mythic": 6,
    "secret": 1
}

RARITY_EMOJI = {
    "common": "⚪",
    "rare": "🔵",
    "legendary": "🟡",
    "mythic": "🔴",
    "secret": "🌟"
}

RARITY_NAME = {
    "common": "Обычный",
    "rare": "Редкий",
    "legendary": "Легендарный",
    "mythic": "Мифический",
    "secret": "Секретный"
}


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
        data[uid] = {"balance": 500, "inventory": []}
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
        f"/iolpa_get — получить любой телефон",
        parse_mode="Markdown"
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

    bot.reply_to(message,
        f"🎰 *Выпал телефон!*\n\n"
        f"{emoji} *{phone['name']}*\n"
        f"Редкость: {rarity_name}\n"
        f"Цена продажи: *{phone['price']} монет*\n\n"
        f"Используй /sell чтобы продать его!",
        parse_mode="Markdown"
    )


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

    bot.reply_to(message, "💵 *Выбери телефон для продажи:*",
                 reply_markup=keyboard, parse_mode="Markdown")


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
        f"✅ *Продано!*\n\n"
        f"{emoji} *{phone['name']}* продан за *{phone['price']} монет*\n"
        f"💰 Твой баланс: *{player['balance']} монет*",
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


@bot.message_handler(commands=["iolpa_get"])
def iolpa_get(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)

    for rarity in ["common", "rare", "legendary", "mythic", "secret"]:
        emoji = RARITY_EMOJI[rarity]
        rarity_name = RARITY_NAME[rarity]
        keyboard.add(telebot.types.InlineKeyboardButton(
            f"{emoji} {rarity_name}",
            callback_data=f"menu_{rarity}"
        ))

    bot.reply_to(message, "📱 *Выбери редкость:*",
                 reply_markup=keyboard, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data.startswith("menu_"))
def show_rarity_phones(call):
    rarity = call.data[5:]
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

    for phone in PHONES[rarity]:
        emoji = RARITY_EMOJI[rarity]
        keyboard.add(telebot.types.InlineKeyboardButton(
            f"{emoji} {phone['name']} — {phone['price']} монет",
            callback_data=f"get_{phone['name']}"
        ))

    keyboard.add(telebot.types.InlineKeyboardButton("◀️ Назад", callback_data="back_menu"))
    bot.edit_message_text(
        f"📱 *Телефоны — {RARITY_NAME[rarity]}:*",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


@bot.callback_query_handler(func=lambda call: call.data == "back_menu")
def back_menu(call):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    for rarity in ["common", "rare", "legendary", "mythic", "secret"]:
        emoji = RARITY_EMOJI[rarity]
        rarity_name = RARITY_NAME[rarity]
        keyboard.add(telebot.types.InlineKeyboardButton(
            f"{emoji} {rarity_name}",
            callback_data=f"menu_{rarity}"
        ))
    bot.edit_message_text(
        "📱 *Выбери редкость:*",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


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
        bot.send_message(call.message.chat.id,
            f"{emoji} *{found_phone['name']}* добавлен в инвентарь!\n"
            f"💰 Цена продажи: {found_phone['price']} монет",
            parse_mode="Markdown"
        )


print("🤖 Бот запущен!")
bot.polling(none_stop=True)
