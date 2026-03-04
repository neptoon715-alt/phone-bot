import telebot
import random
import json
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = "players.json"

# База телефонов: название, цена продажи, редкость
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
    ]
}

RARITY_CHANCE = {
    "common": 60,
    "rare": 30,
    "legendary": 10
}

RARITY_EMOJI = {
    "common": "⚪",
    "rare": "🔵",
    "legendary": "🟡"
}

RARITY_NAME = {
    "common": "Обычный",
    "rare": "Редкий",
    "legendary": "Легендарный"
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
    if roll <= RARITY_CHANCE["legendary"]:
        rarity = "legendary"
    elif roll <= RARITY_CHANCE["legendary"] + RARITY_CHANCE["rare"]:
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
        f"*Команды:*\n"
        f"/card — получить случайный телефон\n"
        f"/sell — продать последний телефон\n"
        f"/inventory — посмотреть все телефоны\n"
        f"/balance — посмотреть баланс",
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

    phone = player["inventory"].pop()
    player["balance"] += phone["price"]
    update_player(message.from_user.id, player)

    emoji = RARITY_EMOJI[phone["rarity"]]

    bot.reply_to(message,
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

# Команда /iolpa_get - меню выбора телефона
@bot.message_handler(commands=["iolpa_get"])
def iolpa_get(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    all_phones = []
    for rarity, phones in PHONES.items():
        for phone in phones:
            all_phones.append((phone["name"], rarity))
    
    buttons = []
    for name, rarity in all_phones:
        emoji = RARITY_EMOJI[rarity]
        buttons.append(telebot.types.InlineKeyboardButton(
            f"{emoji} {name}",
            callback_data=f"get_{name}"
        ))
    
    keyboard.add(*buttons)
    bot.reply_to(message, "📱 *Выбери любой телефон:*", 
                 reply_markup=keyboard, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data.startswith("get_"))
def give_phone(call):
    phone_name = call.data[4:]
    player = get_player(call.from_user.id)
    
    # Найти телефон в базе
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
