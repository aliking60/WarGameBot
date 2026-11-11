from robka import Robot
from robka.context import Message
from robka.button import InlineBuilder
import json
import os

# --- تنظیمات ---
BOT_TOKEN = "CJAJGF0KDELBLXKITJMCQUTQAXFIDHKYCIFBMSSPZOOFQPGZEDFQSUWUHGVPOOQN"

DB_FILE = "game_data.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

game_data = load_data()
bot = Robot(token=BOT_TOKEN)

def get_main_menu():
    builder = InlineBuilder()
    builder.row(
        builder.button_simple("buy_equip", "🛒 خرید تجهیزات"),
        builder.button_simple("send_manifesto", "📜 ارسال بیانیه")
    )
    builder.row(
        builder.button_simple("trade", "🤝 تجارت"),
        builder.button_simple("country_equip", "🎒 تجهیزات کشور")
    )
    builder.row(
        builder.button_simple("produce", "⚙️ تولید"),
        builder.button_simple("factories", "🏭 کارخانه‌ها")
    )
    builder.row(
        builder.button_simple("attack", "⚔️ حمله")
    )
    return builder.build()

@bot.on_message(commands=["start"])
def start(bot: Robot, message: Message):
    user_id = str(message.sender_id)
    
    if user_id not in game_data:
        game_data[user_id] = {
            "budget": 5000000,
            "equipment": 0,
            "factories": 1
        }
        save_data(game_data)
    
    budget = game_data[user_id]["budget"]
    
    text = (
        f"💰 بودجه: {budget:,} میلیون\n\n"
        "🌍 به بازی جنگ جهانی خوش آمدید.\n\n"
        "کشورت را مدیریت کن و وارد بازی شو."
    )
    
    message.reply(text, reply_markup=get_main_menu())

@bot.on_callback()
def button_handler(bot: Robot, message: Message):
    user_id = str(message.sender_id)
    data = message.data
    
    if user_id not in game_data:
        game_data[user_id] = {"budget": 5000000, "equipment": 0, "factories": 1}
    
    user_budget = game_data[user_id]["budget"]

    if data == "produce":
        factories = game_data[user_id]["factories"]
        income = factories * 100000
        game_data[user_id]["budget"] += income
        save_data(game_data)
        message.answer(f"⚙️ شما {income:,} سکه تولید کردید!", show_alert=True)
        
    elif data == "attack":
        if user_budget > 500000:
            game_data[user_id]["budget"] -= 500000
            save_data(game_data)
            message.answer("⚔️ حمله انجام شد! ۵۰۰ هزار سکه هزینه جنگ شد.", show_alert=True)
        else:
            message.answer("❌ بودجه کافی برای حمله نداری!", show_alert=True)
            
    elif data == "buy_equip":
        if user_budget >= 1000000:
            game_data[user_id]["budget"] -= 1000000
            game_data[user_id]["equipment"] += 1
            save_data(game_data)
            message.answer("🛒 یک تجهیزات جدید خریدید! (-۱ میلیون)", show_alert=True)
        else:
            message.answer("❌ بودجه کافی نداری!", show_alert=True)

    elif data == "country_equip":
        eq_count = game_data[user_id]["equipment"]
        message.answer(f"🎒 شما {eq_count} تجهیزات دارید.", show_alert=True)
        
    elif data == "factories":
        f_count = game_data[user_id]["factories"]
        message.answer(f"🏭 شما در حال حاضر {f_count} کارخانه دارید.", show_alert=True)
        
    else:
        message.answer("این بخش به زودی تکمیل می‌شود...", show_alert=True)

# --- اجرای ربات ---
print("ربات روشن شد...")
bot.run()
