import telebot
import random
import json
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = "players.json"

GITHUB_RAW = "https://raw.githubusercontent.com/neptoon715-alt/phone-bot/main/"

PHONES = {
    "common": [
        {"name": "Nokia 3310", "price": 50, "img": "Nokia3300.jpg"},
        {"name": "Nokia 1100", "price": 40, "img": "nokia1100.jpg"},
        {"name": "Motorola C115", "price": 45, "img": "Motorola_C115_life.jpg"},
        {"name": "Samsung E250", "price": 60, "img": "Samsung_E1200.jpg"},
        {"name": "Sony Ericsson K300", "price": 55, "img": "Sony_Ericsson_J100a.jpg"},
        {"name": "Alcatel OT-103", "price": 35, "img": "s-l400.jpg"},
        {"name": "LG C1100", "price": 50, "img": "LG_C1100.jpg"},
        {"name": "Siemens A60", "price": 40, "img": "Siemens_A60.jpg"},
        {"name": "Nokia 2600", "price": 45, "img": "nokia1100.jpg"},
        {"name": "Samsung E1200", "price": 42, "img": "Samsung_E1200.jpg"},
        {"name": "Sony Ericsson J100", "price": 36, "img": "Sony_Ericsson_J100a.jpg"},
        {"name": "Motorola W220", "price": 38, "img": "Motorola_C115_life.jpg"},
    ],
    "rare": [
        {"name": "iPhone 4", "price": 200, "img": "iphone-4.jpg"},
        {"name": "Samsung Galaxy S3", "price": 180, "img": "galaxy3.webp"},
        {"name": "HTC One M7", "price": 190, "img": "HTC-ONE-M7.jpg"},
        {"name": "Sony Xperia Z", "price": 175, "img": "SonyXperiaZ.webp"},
        {"name": "Nokia Lumia 920", "price": 160, "img": "nokia-lumia-920_1.jpg"},
        {"name": "BlackBerry Bold 9900", "price": 220, "img": "s-l1200.jpg"},
        {"name": "Motorola Razr V3", "price": 150, "img": "Motorola_C115_life.jpg"},
        {"name": "iPhone 3GS", "price": 170, "img": "Apple_iPhone_3GS.jpg"},
        {"name": "Samsung Galaxy Note 2", "price": 210, "img": "galaxynote2.webp"},
        {"name": "HTC Desire HD", "price": 165, "img": "30_p_DesireHD2.jpg"},
        {"name": "LG G2", "price": 185, "img": "LGG2.webp"},
        {"name": "Sony Xperia T", "price": 172, "img": "orig-sony-xperia-t-main.jpg"},
    ],
    "legendary": [
        {"name": "iPhone 15 Pro Max", "price": 1200, "img": "iphone15promax.webp"},
        {"name": "Samsung Galaxy S24 Ultra", "price": 1100, "img": "galaxys24ultra.webp"},
        {"name": "Google Pixel 8 Pro", "price": 950, "img": "GooglePixel8Pro1.jpg"},
        {"name": "OnePlus 12", "price": 800, "img": "OnePlusHasselblad.jpg"},
        {"name": "Xiaomi 14 Ultra", "price": 900, "img": "xiaomi-14-ultra.jpg"},
        {"name": "iPhone 14 Pro", "price": 1000, "img": "iphone14pro.webp"},
        {"name": "Samsung Galaxy Z Fold 5", "price": 1500, "img": "SamsungGalaxyZFold 5.jpg"},
        {"name": "Sony Xperia 1 V", "price": 850, "img": "p1.jpg"},
        {"name": "ASUS ROG Phone 7", "price": 1050, "img": "ASUS ROG Phone 7 Ultimate.jpg"},
        {"name": "Xiaomi Mix Fold 3", "price": 1300, "img": "XiaomiMixFold.jpg"},
    ],
    "mythic": [
        {"name": "iPhone 15 Pro Max Titanium", "price": 5000, "img": "iphone15promaxtitan.webp"},
        {"name": "Samsung Galaxy S24 Ultra Gold", "price": 4800, "img": "galaxys24ultragold.webp"},
        {"name": "Vertu Signature Touch", "price": 6000, "img": "s-l1200.jpg"},
        {"name": "Xiaomi 14 Ultra Photography", "price": 4500, "img": "Xiaomi_14_Ultra_Photography.jpg"},
        {"name": "Google Pixel 8 Pro Special", "price": 4200, "img": "GooglePixel8Pro1.jpg"},
        {"name": "OnePlus 12 Hasselblad Edition", "price": 4700, "img": "OnePlusHasselblad.jpg"},
    ],
    "secret": [
        {"name": "iPhone Proto 2007 (прототип)", "price": 50000, "img": None},
        {"name: "Nokiam (Мега Секрет)","price": 190000, "img": None},
        {"name": "Nokia 7700 (отменён)", "price": 45000, "img": None},
        {"name": "Samsung Galaxy Fold Zero", "price": 60000, "img": None},
        {"name": "Apple Leonardo (засекречен)", "price": 99999, "img": None},
        {"name": "Google Pixel Ultra Secret", "price": 55000, "img": None},
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
        caption = (
            f"{emoji} *{found_phone['name']}* добавлен в инвентарь!\n"
            f"💰 Цена продажи: {found_phone['price']} монет"
        )
        send_phone_card(call.message.chat.id, found_phone, caption)


print("🤖 Бот запущен!")
bot.polling(none_stop=True)
